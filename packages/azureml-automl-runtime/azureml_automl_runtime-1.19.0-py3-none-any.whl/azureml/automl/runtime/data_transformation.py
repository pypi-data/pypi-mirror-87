# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Holding the featurization functions."""
import json
import logging
import os
from typing import cast, Dict, Optional, Any, Tuple, Union, List

import numpy as np
import pandas as pd
import scipy
from azureml._common._error_definition import AzureMLError
from azureml._common._error_definition.user_error import ArgumentBlankOrEmpty
from azureml._tracing._tracer_factory import get_tracer
from azureml.automl.core._experiment_observer import ExperimentStatus, ExperimentObserver, NullExperimentObserver
from azureml.automl.core.constants import FeatureType, SweepingMode
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.shared import constants, logging_utilities, utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    AutoMLInternal,
    InvalidArgumentType,
    TimeseriesLeadingNans,
    TimeseriesLaggingNans,
    InputDatasetEmpty)
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared._diagnostics.validation import Validation
from azureml.automl.core.shared.constants import TimeSeries, Transformers, TimeSeriesInternal
from azureml.automl.core.shared.exceptions import ClientException, ConfigException, DataException, ValidationException
from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.runtime import data_cleaning
from azureml.automl.runtime import frequency_fixer
from azureml.automl.runtime.column_purpose_detection import StatsAndColumnPurposeType
import azureml.automl.runtime._ml_engine as ml_engine
from azureml.automl.runtime.featurizer.transformer import (LaggingTransformer,
                                                           TimeSeriesPipelineType,
                                                           TimeSeriesTransformer)
from azureml.automl.runtime.featurizer.transformer.featurization_utilities import skip_featurization
from azureml.automl.runtime.shared import memory_utilities, utilities as runtime_utilities
from azureml.automl.runtime.shared._cv_splits import _CVSplits, FeaturizedCVSplit, FeaturizedTrainValidTestSplit
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.types import DataInputType, DataSingleColumnInputType
from azureml.dataprep import Dataflow
from scipy import sparse
from sklearn import preprocessing
from sklearn.utils.class_weight import compute_class_weight

from ._data_transformation_utilities import (convert_data_to_sparse,
                                             get_cache_key_from_index,
                                             count_nans_in_data,
                                             load_and_update_from_sweeping,
                                             pull_fitted_featurizers_from_cache,
                                             should_convert_data_to_sparse)
from ._feature_sweeped_state_container import FeatureSweepedStateContainer
from .data_context import RawDataContext, TransformedDataContext
from .distributed.utilities import is_master_process
from .faults_verifier import VerifierManager, VerifierResults
from .featurization import DataTransformer, StreamingFeaturizer
from .featurization._featurizer_container import FeaturizerContainer
from .stats_computation import RawFeatureStats
from .streaming_data_context import StreamingTransformedDataContext
from azureml.automl.runtime.faults_verifier import VerifiedFaultsTypes

logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)
_DUMMY_VALUES_FOR_TYPE = {
    "bytes": "example_value",
    "bool": False,
    "datetime": "2000-1-1",
    "float": 0.0,
    "int": 0,
    "object": "example_value",
    "str": "example_value",
    "timedelta": "1000"
}

_DUMMY_VALUES_FOR_FEATURE = {
    FeatureType.Numeric: _DUMMY_VALUES_FOR_TYPE["int"],
    FeatureType.DateTime: _DUMMY_VALUES_FOR_TYPE["datetime"]
}


def _sweep_featurizers(X: DataInputType,
                       y: Optional[DataInputType],
                       task_type: str,
                       experiment_observer: ExperimentObserver,
                       is_onnx_compatible: bool = False,
                       enable_feature_sweeping: bool = False,
                       enable_dnn: bool = True,
                       force_text_dnn: bool = False,
                       featurization: Optional[FeaturizationConfig] = None,
                       is_cross_validation: bool = False,
                       feature_sweeping_config: Dict[str, Any] = {},
                       working_dir: Optional[str] = None) -> DataTransformer:
    """
    Sweep featurizers and return the corresponding data transformer.
    """
    with tracer.start_as_current_span(
            constants.TelemetryConstants.SPAN_FORMATTING.format(
                constants.TelemetryConstants.COMPONENT_NAME, constants.TelemetryConstants.FEATURIZATION_STRATEGY
            ),
            user_facing_name=constants.TelemetryConstants.FEATURIZATION_STRATEGY_USER_FACING
    ):
        dt = DataTransformer(task=task_type,
                             is_onnx_compatible=is_onnx_compatible,
                             enable_feature_sweeping=enable_feature_sweeping,
                             enable_dnn=enable_dnn,
                             force_text_dnn=force_text_dnn,
                             observer=experiment_observer,
                             featurization_config=featurization,
                             is_cross_validation=is_cross_validation,
                             feature_sweeping_config=feature_sweeping_config,
                             working_dir=working_dir)

        dt.configure_featurizers(X, y)
        return dt


def _fit_transform(
    x: DataInputType,
    y: DataInputType,
    dt: DataTransformer,
    logger: Optional[logging.Logger] = None
) -> Union[pd.DataFrame, np.ndarray, sparse.spmatrix]:
    return dt.fit_transform_with_logger(x, y, logger)


def build_feature_sweeped_state_container(
    raw_data_context: RawDataContext,
    cache_store: CacheStore,
    is_onnx_compatible: bool,
    experiment_observer: ExperimentObserver,
    enable_feature_sweeping: bool,
    feature_sweeping_config: Dict[str, Any],
    enable_dnn: bool,
    force_text_dnn: bool,
    featurizer_container: FeaturizerContainer
) -> FeatureSweepedStateContainer:
    """
    Builds a feature sweeped state container.

    :param raw_data_context: The raw input data.
    :param cache_store: The object that should be used to cache featurized data.
    :param is_onnx_compatible: If works in onnx compatible mode.
    :param experiment_observer: The experiment observer.
    :param enable_feature_sweeping: Enable or disable feature sweeping.
    :param feature_sweeping_config: Config used for feature sweeping.
    :param enable_dnn: Flag to enable neural networks for forecasting and natural language processing.
    :param force_text_dnn: Flag to force add neural networks for natural language processing in feature sweeping.
    :param featurizer_container: The featurizer container.
    :return: The feature sweeped state container to use for featurization.
    """
    transformed_data_context, y_transformer, X, y = create_transformed_data_context_no_streaming(
        raw_data_context, cache_store)
    transformed_data_context.X = _add_raw_column_names_to_X(
        raw_data_context.x_raw_column_names, transformed_data_context.X)

    featurization_config = raw_data_context.featurization if isinstance(raw_data_context.featurization,
                                                                        FeaturizationConfig) else None
    data_transformer = DataTransformer(
        task=raw_data_context.task_type,
        is_onnx_compatible=is_onnx_compatible,
        enable_feature_sweeping=enable_feature_sweeping,
        enable_dnn=enable_dnn,
        force_text_dnn=force_text_dnn,
        observer=experiment_observer,
        featurization_config=featurization_config,
        is_cross_validation=transformed_data_context._is_cross_validation_scenario(),
        feature_sweeping_config=feature_sweeping_config
    )
    # This is a separate featurization run, so we need to restore the data_transformer.
    load_and_update_from_sweeping(data_transformer, transformed_data_context.X)
    data_transformer.set_cached_featurizers(pull_fitted_featurizers_from_cache(
        cache_store, featurizer_container))
    data_transformer._featurizer_container = featurizer_container

    return FeatureSweepedStateContainer(
        data_transformer, transformed_data_context, y_transformer, X, y)


def create_transformed_data_context_no_streaming(raw_data_context: RawDataContext,
                                                 cache_store: CacheStore,
                                                 verifier: Optional[VerifierManager] = None) \
        -> Tuple[TransformedDataContext, Optional[preprocessing.LabelEncoder], DataInputType, np.ndarray]:
    """
    Helper function for transforming input raw data from JOS to a transformed data context for further processing.
    We have already checked to ensure that streaming is not turned on.

    :param raw_data_context: The raw input data.
    :param cache_store: The object that should be used to cache featurized data.
    :param verifier: The verifier to check input data quality.
    :return: Transformed data context.
    """
    logger.info("Pre-processing user data")
    logger.info("The size of the raw data is: " + str(raw_data_context._get_memory_size()))

    y_df = raw_data_context.y
    Validation.validate_value(y_df, "y", reference_code=ReferenceCodes._DATA_TRANSFORMATION_INVALID_Y)

    if not isinstance(y_df, pd.DataFrame):
        try:
            y_df = pd.DataFrame(y_df)
        except ValueError as ve:
            raise ValidationException._with_error(
                AzureMLError.create(InvalidArgumentType, target="y", argument="y", actual_type=type(y_df),
                                    expected_types="pandas.DataFrame"),
                inner_exception=ve
            ) from ve

    y_raw_stats = RawFeatureStats(y_df.iloc[:, 0])
    utilities._log_raw_data_stat(
        y_raw_stats,
        prefix_message="[YCol]"
    )

    x_is_sparse = scipy.sparse.issparse(raw_data_context.X)
    if skip_featurization(raw_data_context.featurization) or x_is_sparse:
        # log the data characteristics as it won't be going into featurization.
        if x_is_sparse:
            logger.info("The sparse matrix is not supported for getting col characteristics.")
        else:
            x_df = raw_data_context.X
            if not isinstance(x_df, pd.DataFrame):
                x_df = pd.DataFrame(raw_data_context.X)
            for column in x_df.columns:
                raw_stats = RawFeatureStats(x_df[column])
                utilities._log_raw_data_stat(
                    raw_stats,
                    prefix_message="[XColNum:{}]".format(x_df.columns.get_loc(column))
                )

    _log_data_info('X_raw', raw_data_context.X)
    _log_data_info('X_valid_raw', raw_data_context.X_valid)
    _log_data_info('y_raw', raw_data_context.y)
    _log_data_info('y_valid_raw', raw_data_context.y_valid)

    # Fix validation_size y-aware transformer leakeage issue, see 519483 and 518786
    # TODO: remove the below if block and
    # refactor validation_size and cv logic to overcome leakage in y-aware transformers
    if raw_data_context.validation_size is not None \
            and raw_data_context.validation_size > 0.0 \
            and raw_data_context.X_valid is None \
            and raw_data_context.y_valid is None \
            and raw_data_context.cv_splits_indices is None \
            and not raw_data_context.timeseries \
            and raw_data_context.num_cv_folds is None:
        _create_train_valid_data(raw_data_context)

    X, y, sample_weight = data_cleaning._remove_nan_rows_in_X_y(
        raw_data_context.X, raw_data_context.y,
        sample_weight=raw_data_context.sample_weight,
        logger=logger,
        is_timeseries=raw_data_context.timeseries,
        target_column=raw_data_context.label_column_name,
        featurization_config=raw_data_context.featurization
    )

    X_valid, y_valid, sample_weight_valid = data_cleaning._remove_nan_rows_in_X_y(
        raw_data_context.X_valid, raw_data_context.y_valid,
        sample_weight=raw_data_context.sample_weight_valid,
        logger=logger,
        is_timeseries=raw_data_context.timeseries,
        target_column=raw_data_context.label_column_name,
        featurization_config=raw_data_context.featurization
    )

    # Save off raw cleaned data to be cached
    X_raw_cleaned = X
    y_raw_cleaned = y
    X_valid_raw_cleaned = X_valid
    y_valid_raw_cleaned = y_valid

    # After NaNs are handled from data_cleaning._remove_nan_rows_in_X_y(),
    # if featurization is turned off (which means AutoML is not handling missing value)
    # and data is sparse (data contains 50 percent or more NaNs),
    # we need to convert it to scipy.sparse.spmatrix so that Miro can suggest pipelines that are sparse-compatible.
    if skip_featurization(raw_data_context.featurization, raw_data_context.timeseries):
        count_nans = count_nans_in_data(X)
        if count_nans > 0:
            if should_convert_data_to_sparse(X, count_nans):
                logger.info("Data detected as sparse with more than 50 percent NaNs, "
                            "but featurization is turned off and is omitting imputation. "
                            "Converting the data into sparse matrix.")
                X = convert_data_to_sparse(X)
                X_valid = convert_data_to_sparse(X_valid)
            else:
                logger.info("Data contains NaN but is detected as dense since it contains less than 50 percent NaNs. "
                            "Featurization is turned off and is omitting imputation. "
                            "If NaNs are not expected, consider turning on featurization or cleaning up data.")
            if verifier is not None:
                verifier.update_data_verifier_for_missing_values(verifier_result=VerifierResults.ALERTED)

    y_transformer, y, y_valid = _y_transform(y, y_valid, raw_data_context.task_type)

    enable_class_balancing = False
    class_balancing_fixed = False
    if raw_data_context.task_type == constants.Tasks.CLASSIFICATION and verifier is not None:
        enable_class_balancing, size_of_smallest_class, name_of_smallest_class = \
            _class_balancing_check(y, y_transformer)
        verifier.update_data_verifier_for_class_balancing_validation(enable_class_balancing,
                                                                     class_balancing_fixed,
                                                                     size_of_smallest_class,
                                                                     name_of_smallest_class, y.shape[0])

    transformed_data_context = TransformedDataContext(X=X,
                                                      y=y,
                                                      X_valid=X_valid,
                                                      y_valid=y_valid,
                                                      sample_weight=sample_weight,
                                                      sample_weight_valid=sample_weight_valid,
                                                      x_raw_column_names=raw_data_context.x_raw_column_names,
                                                      cv_splits_indices=raw_data_context.cv_splits_indices,
                                                      num_cv_folds=raw_data_context.num_cv_folds,
                                                      validation_size=raw_data_context.validation_size,
                                                      timeseries=raw_data_context.timeseries,
                                                      timeseries_param_dict=raw_data_context.timeseries_param_dict,
                                                      cache_store=cache_store,
                                                      logger=logger,
                                                      task_type=raw_data_context.task_type,
                                                      X_raw_cleaned=X_raw_cleaned,
                                                      y_raw_cleaned=y_raw_cleaned,
                                                      X_valid_raw_cleaned=X_valid_raw_cleaned,
                                                      y_valid_raw_cleaned=y_valid_raw_cleaned)

    _log_data_info('X', transformed_data_context.X)
    _log_data_info('X_valid', transformed_data_context.X_valid)
    _log_data_info('y', transformed_data_context.y)
    _log_data_info('y_valid', transformed_data_context.y_valid)

    return transformed_data_context, y_transformer, X, y


def get_transformers_for_full_featurization(raw_data_context: RawDataContext,
                                            cache_store: CacheStore,
                                            is_onnx_compatible: bool = False,
                                            logger: Optional[logging.Logger] = None,
                                            experiment_observer: Optional[ExperimentObserver] = None,
                                            enable_feature_sweeping: bool = False,
                                            verifier: Optional[VerifierManager] = None,
                                            enable_streaming: bool = False,
                                            feature_sweeping_config: Dict[str, Any] = {},
                                            enable_dnn: bool = False,
                                            force_text_dnn: bool = False,
                                            working_dir: Optional[str] = None) \
        -> Optional[FeatureSweepedStateContainer]:
    """
    Performs the feature sweeping part of data transformation for all standard code paths.

    :param raw_data_context: The raw input data.
    :param cache_store: The object that should be used to cache featurized data.
    :param is_onnx_compatible: If works in onnx compatible mode.
    :param logger: The logger.
    :param experiment_observer: The experiment observer.
    :param enable_feature_sweeping: Enable or disable feature sweeping.
    :param verifier: The verifier to check input data quality.
    :param enable_streaming: Enable or disable streaming.
    :param feature_sweeping_config: Config used for feature sweeping.
    :param enable_dnn: Flag to enable neural networks for forecasting and natural language processing.
    :param force_text_dnn: Flag to force add neural networks for natural language processing in feature sweeping.
    :param working_dir: Working directory to use for featurization/training.
    :return: Container for objects generated by feature sweeping that will be needed in full featurization.
    """
    logger = logger or logging_utilities.NULL_LOGGER
    if enable_streaming or raw_data_context.timeseries or \
            skip_featurization(raw_data_context.featurization, raw_data_context.timeseries):
        scenario_types_for_logging = []
        if enable_streaming:
            scenario_types_for_logging.append("streaming")
        if raw_data_context.timeseries:
            scenario_types_for_logging.append("timeseries")
        if skip_featurization(raw_data_context.featurization, raw_data_context.timeseries):
            scenario_types_for_logging.append("skip featurization")
        logger.info("Skipping mainstream sweeping logic. Detected {} scenario.".format(
            " + ".join(scenario_types_for_logging)))
        return None

    transformed_data_context, y_transformer, X, y = \
        create_transformed_data_context_no_streaming(raw_data_context,
                                                     cache_store,
                                                     verifier)
    if not scipy.sparse.issparse(transformed_data_context.X):
        transformed_data_context.X = _add_raw_column_names_to_X(raw_data_context.x_raw_column_names,
                                                                transformed_data_context.X)
        featurization = None
        if isinstance(raw_data_context.featurization, FeaturizationConfig):
            featurization = raw_data_context.featurization
        is_cross_validation = transformed_data_context._is_cross_validation_scenario()
        with logging_utilities.log_activity(logger=logger, activity_name="Beginning feature sweeping."):
            data_transformer = _sweep_featurizers(X=transformed_data_context.X,
                                                  y=transformed_data_context.y,
                                                  task_type=raw_data_context.task_type,
                                                  experiment_observer=experiment_observer or NullExperimentObserver(),
                                                  is_onnx_compatible=is_onnx_compatible,
                                                  enable_feature_sweeping=enable_feature_sweeping,
                                                  enable_dnn=enable_dnn,
                                                  force_text_dnn=force_text_dnn,
                                                  feature_sweeping_config=feature_sweeping_config,
                                                  featurization=featurization,
                                                  is_cross_validation=is_cross_validation,
                                                  working_dir=working_dir)
        if verifier is not None:
            verifier.update_data_verifier_for_missing_values(data_transformer)
            verifier.update_data_verifier_for_text_class_validation(data_transformer.stats_and_column_purposes)

        return FeatureSweepedStateContainer(data_transformer=data_transformer,
                                            transformed_data_context=transformed_data_context,
                                            y_transformer=y_transformer,
                                            x=X,
                                            y=y)
    return None


def complete_featurization(raw_data_context: RawDataContext,
                           working_dir: str,
                           cache_store: CacheStore,
                           experiment_observer: Optional[ExperimentObserver] = None,
                           verifier: Optional[VerifierManager] = None,
                           enable_streaming: bool = False,
                           feature_sweeping_config: Dict[str, Any] = {},
                           feature_sweeped_state_container: Optional[FeatureSweepedStateContainer] = None) \
        -> Union[TransformedDataContext, StreamingTransformedDataContext]:
    """
    Finishes data transformation by running full featurization on the transformers
    identified in the feature sweeping stage.

    :param raw_data_context: The raw input data.
    :param working_dir: Working directory to use for featurization/training.
    :param cache_store: The object that should be used to cache featurized data.
    :param experiment_observer: The experiment observer.
    :param verifier: The verifier to check input data quality.
    :param enable_streaming: Enable or disable streaming.
    :param feature_sweeping_config: Config used for feature sweeping.
    :param feature_sweeped_state_container: Object holding information generated in feature sweeping.
    :return: Transformed data context.
    """
    # TODO: break down featurization span more
    with tracer.start_as_current_span(
            constants.TelemetryConstants.SPAN_FORMATTING.format(
                constants.TelemetryConstants.COMPONENT_NAME, constants.TelemetryConstants.FEATURIZATION
            ),
            user_facing_name=constants.TelemetryConstants.FEATURIZATION_USER_FACING
    ):
        if enable_streaming:
            return transform_data_streaming(raw_data_context, experiment_observer)

        if feature_sweeped_state_container is None:
            # this is a scenario in which we have not yet initialized a transformed data context
            # or data_transformer (e.g. new featurization run, timeseries, or skip featurization).
            transformed_data_context, y_transformer, X, y = \
                create_transformed_data_context_no_streaming(raw_data_context, cache_store, verifier)
        else:
            # likely local, native, or adb code path
            data_transformer = feature_sweeped_state_container.data_transformer
            transformed_data_context = feature_sweeped_state_container.transformed_data_context
            y_transformer = feature_sweeped_state_container.y_transformer
            X = feature_sweeped_state_container.X
            y = feature_sweeped_state_container.y
        sample_weight = transformed_data_context.sample_weight
        x_is_sparse = scipy.sparse.issparse(transformed_data_context.X)
        transformer, lag_transformer, ts_transformer = None, None, None
        data_snapshot_str = None

        if experiment_observer is None:
            experiment_observer = NullExperimentObserver()

        # we only call this function if enable_streaming is False, so no need to retest this
        enable_class_balancing = False
        if raw_data_context.task_type == constants.Tasks.CLASSIFICATION:
            enable_class_balancing, size_of_smallest_class, name_of_smallest_class = \
                _class_balancing_check(y, y_transformer)

        if skip_featurization(raw_data_context.featurization, raw_data_context.timeseries) or x_is_sparse:
            logger.info("Skipping featurization step")
            data_snapshot_str = _get_data_snapshot(transformed_data_context.X)
        elif not skip_featurization(raw_data_context.featurization) and not raw_data_context.timeseries:
            transformed_data_context.X = _add_raw_column_names_to_X(raw_data_context.x_raw_column_names,
                                                                    transformed_data_context.X)

            # fit features and transform data
            transformer, transformed_data_context.X, data_snapshot_str = \
                _get_transformer_x(x=transformed_data_context.X,
                                   y=transformed_data_context.y,
                                   dt=data_transformer,
                                   verifier=verifier,
                                   experiment_observer=experiment_observer)

            if transformed_data_context.X_valid is not None:
                transformed_data_context.X_valid = _add_raw_column_names_to_X(
                    raw_data_context.x_raw_column_names, transformed_data_context.X_valid)
                transformed_data_context.X_valid = transformer.transform(transformed_data_context.X_valid)

            if raw_data_context.lag_length is not None and raw_data_context.lag_length > 0:
                # Get engineered names from Data Transformer if available
                x_raw_column_names = np.asarray(raw_data_context.x_raw_column_names)
                if transformer is not None:
                    x_raw_column_names = np.asarray(transformer.get_engineered_feature_names())

                # Create a lagging transformer
                lag_transformer = LaggingTransformer(raw_data_context.lag_length)

                # Fit/Transform using lagging transformer
                transformed_data_context.X = lag_transformer.fit_transform(
                    _add_raw_column_names_to_X(x_raw_column_names, transformed_data_context.X),
                    transformed_data_context.y)

                if transformed_data_context.X_valid is not None:
                    transformed_data_context.X_valid = lag_transformer.transform(
                        _add_raw_column_names_to_X(x_raw_column_names,
                                                   transformed_data_context.X_valid))
                logger.info("lagging transformer is enabled with length {}.".format(raw_data_context.lag_length))

            transformed_data_context._set_transformer(x_transformer=transformer,
                                                      lag_transformer=lag_transformer)
            # Sweeping for class balancing techniques
            if enable_class_balancing:
                balancing_result = _perform_class_balancing_sweeping(raw_data_context.task_type,
                                                                     transformed_data_context.X,
                                                                     transformed_data_context.y,
                                                                     enable_class_balancing=enable_class_balancing,
                                                                     working_dir=working_dir,
                                                                     experiment_observer=experiment_observer,
                                                                     feature_sweeping_config=feature_sweeping_config,
                                                                     is_cross_validation=transformed_data_context.
                                                                     _is_cross_validation_scenario()
                                                                     )

                if balancing_result is not None and len(balancing_result) > 0:
                    for k, v in balancing_result.items():
                        if k == "weights":
                            transformed_data_context.sample_weight = v
                    class_balancing_fixed = True
                    if verifier:
                        verifier.update_data_verifier_for_class_balancing_validation(enable_class_balancing,
                                                                                     class_balancing_fixed,
                                                                                     size_of_smallest_class,
                                                                                     name_of_smallest_class,
                                                                                     y.shape[0])
        elif raw_data_context.timeseries:
            if raw_data_context.featurization is not None and \
                    raw_data_context.label_column_name is not None and \
                    isinstance(raw_data_context.featurization, FeaturizationConfig):
                raw_data_context.featurization._convert_timeseries_target_column_name(
                    raw_data_context.label_column_name)
            if raw_data_context.timeseries_param_dict is not None:
                transformed_data_context.X = _add_raw_column_names_to_X(
                    raw_data_context.x_raw_column_names,
                    transformed_data_context.X,
                    raw_data_context.timeseries_param_dict.get(TimeSeries.TIME_COLUMN_NAME))
            ts_transformer, transformed_data, data_snapshot_str = \
                _get_ts_transformer_x(
                    transformed_data_context.X,
                    transformed_data_context.y,
                    raw_data_context.timeseries_param_dict,
                    for_cv=False,
                    experiment_observer=experiment_observer,
                    featurization_config=raw_data_context.featurization,
                    fault_verifier=verifier
                )
            # Add guard rails for time series.
            if verifier:
                _add_forecasting_guardrails_maybe(ts_transformer, verifier)

            # Report heuristic features if any and if experiment_observer is not None.
            _print_heuristics_maybe(experiment_observer, ts_transformer)

            target_column_name = ts_transformer.target_column_name
            if raw_data_context.timeseries_param_dict is not None and target_column_name in transformed_data.columns:
                transformed_data_context.y = transformed_data.pop(target_column_name).values
                transformed_data_context.X = transformed_data

            if transformed_data_context.X_valid is not None:
                if raw_data_context.timeseries_param_dict is not None:
                    transformed_data_context.X_valid = _add_raw_column_names_to_X(
                        raw_data_context.x_raw_column_names,
                        transformed_data_context.X_valid,
                        raw_data_context.timeseries_param_dict.get(TimeSeries.TIME_COLUMN_NAME))
                transformed_data_valid = ts_transformer.transform(
                    transformed_data_context.X_valid,
                    transformed_data_context.y_valid
                )
                transformed_data_context.y_valid = transformed_data_valid.pop(target_column_name).values
                transformed_data_context.X_valid = transformed_data_valid
                if not raw_data_context.timeseries:
                    transformed_data_context.X_valid = transformed_data_context.X_valid.values

            transformed_data_context.timeseries_param_dict = ts_transformer.parameters
            transformed_data_context._set_transformer(ts_transformer=ts_transformer)

            if scipy.sparse.issparse(transformed_data_context.X):
                transformed_data_context.X = transformed_data_context.X.todense()
        else:
            logger.info("lagging transformer is enabled with length {}.".format(raw_data_context.lag_length))

        transformed_data_context._set_raw_data_snapshot_str(data_snapshot_str)
        transformed_data_context._set_transformer(transformer, lag_transformer, y_transformer=y_transformer,
                                                  ts_transformer=ts_transformer)

        # Create featurized versions of cross validations if user configuration specifies cross validations
        _create_cv_splits_transformed_data(transformed_data_context, raw_data_context,
                                           X, y, sample_weight,
                                           experiment_observer)

        if transformed_data_context._is_cross_validation_scenario() or raw_data_context.timeseries:
            # Refit transformers
            # Only do this for CV since for train-valid this is incorrect, see 507941s
            # TODO: evaluate if this refit is even necessary
            #  CV as a fit on all the data is already done above, see 518786
            time_colname = None
            if raw_data_context.timeseries_param_dict is not None and raw_data_context.timeseries:
                time_colname = raw_data_context.timeseries_param_dict.get(TimeSeries.TIME_COLUMN_NAME)
            raw_X = _add_raw_column_names_to_X(
                raw_data_context.x_raw_column_names,
                X, time_colname)
            transformed_data_context._refit_transformers(raw_X, y)

        if not skip_featurization(raw_data_context.featurization, raw_data_context.timeseries):
            transformed_data_context._update_cache()

        logger.info("The size of transformed data is: " + str(transformed_data_context._get_memory_size()))

        return transformed_data_context


def transform_data(raw_data_context: RawDataContext,
                   cache_store: CacheStore,
                   is_onnx_compatible: bool = False,
                   logger: Optional[logging.Logger] = None,
                   experiment_observer: Optional[ExperimentObserver] = None,
                   enable_feature_sweeping: bool = False,
                   verifier: Optional[VerifierManager] = None,
                   enable_streaming: bool = False,
                   feature_sweeping_config: Dict[str, Any] = {},
                   enable_dnn: bool = False,
                   force_text_dnn: bool = False,
                   working_dir: Optional[str] = None) \
        -> Union[TransformedDataContext, StreamingTransformedDataContext]:
    """
    Transform input data from RawDataContext to TransformedDataContext.

    :param raw_data_context: The raw input data.
    :param cache_store: The object that should be used to cache featurized data.
    :param is_onnx_compatible: If works in onnx compatible mode.
    :param logger: The logger.
    :param experiment_observer: The experiment observer.
    :param enable_feature_sweeping: Enable or disable feature sweeping.
    :param verifier: The verifier to check input data quality.
    :param enable_streaming: Whether run is using streaming.
    :param feature_sweeping_config: Config used for feature sweeping.
    :param enable_dnn: Flag to enable neural networks for forecasting and natural language processing.
    :param force_text_dnn: Flag to force add neural networks for natural language processing in feature sweeping.
    :param working_dir: Working directory to use for featurization/training.
    :return: Transformed data context.
    """
    if working_dir is None:
        working_dir = os.getcwd()

    feature_sweeped_state_container = \
        ml_engine.suggest_featurizers(raw_data_context,
                                      cache_store=cache_store,
                                      is_onnx_compatible=is_onnx_compatible,
                                      logger=logger,
                                      experiment_observer=experiment_observer,
                                      enable_feature_sweeping=enable_feature_sweeping,
                                      verifier=verifier,
                                      enable_streaming=enable_streaming,
                                      feature_sweeping_config=feature_sweeping_config,
                                      enable_dnn=enable_dnn,
                                      force_text_dnn=force_text_dnn,
                                      working_dir=working_dir)

    return complete_featurization(raw_data_context,
                                  cache_store=cache_store,
                                  experiment_observer=experiment_observer,
                                  verifier=verifier,
                                  enable_streaming=enable_streaming,
                                  feature_sweeping_config=feature_sweeping_config,
                                  working_dir=working_dir,
                                  feature_sweeped_state_container=feature_sweeped_state_container)


def fit_and_cache_featurizers(raw_data_context: RawDataContext,
                              featurizer_container: FeaturizerContainer,
                              cache_store: CacheStore,
                              observer: Optional[ExperimentObserver] = None,
                              is_onnx_compatible: bool = False,
                              enable_feature_sweeping: bool = False,
                              enable_dnn: bool = False,
                              force_text_dnn: bool = False,
                              feature_sweeping_config: Optional[Dict[str, Any]] = None,
                              working_dir: Optional[str] = None) -> None:
    """
    Fit and cache individual featurizers. Designed to be called in a separate run from the rest of
    data transformation, so the fitted featurizers must be cached after being fitted.

    :param raw_data_context: The raw input data.
    :param featurizer_container: The featurization JSON that we will use to determine which featurizers to fit.
    :param cache_store: The object that should be used to cache featurized data.
    :param observer: The experiment observer.
    :param is_onnx_compatible: If works in onnx compatible mode.
    :param enable_feature_sweeping: Enable or disable feature sweeping.
    :param enable_dnn: Flag to enable neural networks for forecasting and natural language processing.
    :param force_text_dnn: Flag to force add neural networks for natural language processing in feature sweeping.
    :param feature_sweeping_config: Config used for feature sweeping.
    :param working_dir: Working directory to use for featurization/training.
    :return: None. The results are cached.

    Note that the last six parameters will be condensed into a DataTransformerSettings object once that PR merges.
    """
    if feature_sweeping_config is None:
        feature_sweeping_config = {}

    # investigate caching these results, since they're used in all the runs.
    transformed_data_context, _, _, _ = \
        create_transformed_data_context_no_streaming(raw_data_context,
                                                     cache_store)

    # investigate moving this into create_transformed_data_context_no_streaming so we don't have to put it everywhere
    transformed_data_context.X = _add_raw_column_names_to_X(raw_data_context.x_raw_column_names,
                                                            transformed_data_context.X)

    featurization_config = raw_data_context.featurization if isinstance(raw_data_context.featurization,
                                                                        FeaturizationConfig) else None

    data_transformer = DataTransformer(
        task=raw_data_context.task_type,
        is_onnx_compatible=is_onnx_compatible,
        enable_feature_sweeping=enable_feature_sweeping,
        enable_dnn=enable_dnn,
        force_text_dnn=force_text_dnn,
        logger=logger,
        observer=observer,
        featurization_config=featurization_config,
        is_cross_validation=transformed_data_context._is_cross_validation_scenario(),
        feature_sweeping_config=feature_sweeping_config,
        working_dir=working_dir
    )

    load_and_update_from_sweeping(data_transformer, transformed_data_context.X)

    for featurizer in featurizer_container:
        if is_master_process() or featurizer.is_distributable:
            fitted_featurizer = featurizer.fit(data_transformer=data_transformer,
                                               df=transformed_data_context.X,
                                               y=transformed_data_context.y)
            cache_store.set(get_cache_key_from_index(featurizer.index), fitted_featurizer)


def _add_forecasting_guardrails_maybe(ts_transformer: TimeSeriesTransformer,
                                      verifier: VerifierManager) -> None:
    """
    Add guardrails for the forecasting lookback features.

    :param ts_transformer: The fitted TimeSeriesTransformer.
    :param verifier: The VerifierManager to add guardrails to.
    """
    lags = TimeSeriesInternal.LAGS_TO_CONSTRUCT in ts_transformer.parameters.keys()
    rw = TimeSeriesInternal.WINDOW_SIZE in ts_transformer.parameters.keys()
    verifier.update_data_verifier_lookback_feature(
        lags=lags,
        rw=rw,
        passed=not ts_transformer.lookback_features_removed)
    # The guardrails for the short series handling.
    if ts_transformer.parameters[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] is None:
        # If we have a short grain and there is no handling, we have to fail before this stage.
        verifier.update_data_verifier_short_grain_handling(0, 0)
    elif not verifier.has_fault_member(VerifiedFaultsTypes.TIMESERIES_SHORT_SERIES_HANDLING):
        if ts_transformer.pipeline is None:
            ts_dropper = None
        else:
            ts_dropper = ts_transformer.pipeline.get_pipeline_step(TimeSeriesInternal.SHORT_SERIES_DROPPEER)
        if ts_dropper is not None:
            verifier.update_data_verifier_short_grain_handling(0, ts_dropper.short_grains_in_train)
        else:
            verifier.update_data_verifier_short_grain_handling(0, 0)


def _create_train_valid_data(raw_data_context: RawDataContext) -> None:
    """Use validation_size to create explicit train valid splits."""
    context = raw_data_context
    cv_splits = _CVSplits(context.X, context.y,
                          frac_valid=context.validation_size,
                          cv_splits_indices=None,
                          is_time_series=False,
                          timeseries_param_dict=None,
                          task=context.task_type)

    X, y, weights, X_valid, y_valid, weights_valid, _, _, _ = cv_splits.get_train_validation_test_chunks(
        context.X, context.y, context.sample_weight)

    context.X, context.y, context.sample_weight = X, y, weights
    context.X_valid, context.y_valid, context.sample_weight_valid = X_valid, y_valid, weights_valid
    context.validation_size = None


def _print_heuristics_maybe(experiment_observer: ExperimentObserver,
                            tst: TimeSeriesTransformer) -> None:
    """Print out heuristics to experiment observer."""
    if experiment_observer is not None:
        auto_settings = []
        if tst.get_auto_lag() is not None:
            auto_settings.append('Target_Lag = \'{}\''.format(tst.get_auto_lag()))

        if tst.get_auto_window_size() is not None:
            auto_settings.append('Target_Rolling_Window = \'{}\''.format(tst.get_auto_window_size()))

        if tst.get_auto_max_horizon() is not None:
            auto_settings.append('Max_Horizon = \'{}\''.format(tst.get_auto_max_horizon()))

        if auto_settings:
            message = "Heuristic parameters: {}.\n".format(', '.join(auto_settings))
            if hasattr(experiment_observer, 'file_handler') and experiment_observer.file_handler is not None:
                # Local run
                # Directly output message to console.
                cast(Any, experiment_observer).file_handler.write(message)
            if experiment_observer.run_instance:  # type: ignore
                # Remote run.
                # Put the 'auto' tag to the run to use it later.
                cast(Any, experiment_observer).run_instance.set_tags({TimeSeries.AUTO: message})
        # Set the automatic parameters anyways.
        if experiment_observer.run_instance:  # type: ignore
            # Set potentially heuristic parameters to run,
            # so they will be shown in the UI.
            properties_dict = {
                TimeSeriesInternal.RUN_TARGET_LAGS: str(tst.get_target_lags()),
                TimeSeriesInternal.RUN_WINDOW_SIZE: str(tst.get_target_rolling_window_size()),
                TimeSeriesInternal.RUN_MAX_HORIZON: str(tst.max_horizon)
            }
            cast(Any, experiment_observer).run_instance.add_properties(properties_dict)


def transform_data_streaming(raw_data_context: RawDataContext,
                             observer: Optional[ExperimentObserver] = None) -> StreamingTransformedDataContext:
    """
    Transform the input from RawDataContext to StreamingTransformedDataContext

    :param raw_data_context: The raw input data.
    :return: Transformed data context.
    """
    # Get a snapshot of the raw data (without the label column and weight column),
    # that will become the schema that is used for inferences
    columns_to_drop = []
    if raw_data_context.label_column_name is not None:
        columns_to_drop.append(raw_data_context.label_column_name)
    if raw_data_context.weight_column_name is not None:
        columns_to_drop.append(raw_data_context.weight_column_name)
    raw_data_snapshot = _get_data_snapshot(data=raw_data_context.training_data.drop_columns(columns=columns_to_drop))
    result = StreamingTransformedDataContext(x_raw_column_names=raw_data_context.x_raw_column_names,
                                             training_data=raw_data_context.training_data,
                                             label_column_name=raw_data_context.label_column_name,
                                             raw_data_snapshot=raw_data_snapshot,
                                             weight_column_name=raw_data_context.weight_column_name,
                                             validation_data=raw_data_context.validation_data)

    if not skip_featurization(raw_data_context.featurization):
        streaming_featurizer = StreamingFeaturizer(
            raw_data_context.training_data,
            raw_data_context.label_column_name,
            raw_data_context.weight_column_name,
            logger=logger,
            observer=observer,
            featurization_config=raw_data_context.featurization
            if isinstance(raw_data_context.featurization, FeaturizationConfig) else None)

        logger.info("Learning streaming transformations...")
        streaming_featurization_transformer = streaming_featurizer.learn_transformations()

        result.set_featurization_transformer(streaming_featurization_transformer)
        result.set_featurized_column_names(streaming_featurizer.get_transformed_vector_column_names())

    return result


def _log_data_info(data_name: str,
                   data: Optional[np.ndarray]) -> None:
    """
    Log details about the data.

    :param data_name: Name of data to inspect.
    :param data: Data to inspect.
    """
    if data is not None:
        message_format = "{} datatype is {}, shape is {}, datasize is {}."
        memory_size = memory_utilities.get_data_memory_size(data)
        logger.info(message_format.format(data_name, type(data), data.shape, memory_size))
    else:
        message_format = "{} is None, no data details to log."
        logger.info(message_format.format(data_name))


def _get_dummy_value_by_purpose_or_dtype(purpose: Optional[FeatureType] = None,
                                         npdtype: Optional[np.dtype] = None) -> Any:
    """
    Get dummy values by either purpose or dtype of the column. If dtype is provided, it will get preference
    over purpose since dtypes are more accurate. If dtype is not provided, dummy value is picked based on
    the purpose.

    :param purpose: The FeatureType of the column
    :param npdtype: The dtype of the column
    :return: The dummy value
    """
    if npdtype:
        # we know the dtype because it was pandas dataframe
        for dtype_substring in _DUMMY_VALUES_FOR_TYPE.keys():
            if dtype_substring in npdtype.name:
                return _DUMMY_VALUES_FOR_TYPE[dtype_substring]

    if purpose:
        # if the user passed a numpy array we rely on the column purpose.
        return _DUMMY_VALUES_FOR_FEATURE.get(str(purpose), _DUMMY_VALUES_FOR_TYPE['str'])

    # If neither the dtype nor column purpose is known, it means featurization was turned off and
    # the user passed a numpy array or a sparse matrix. We can safely return a numeric value.
    return _DUMMY_VALUES_FOR_TYPE['int']


def _get_data_snapshot_helper(data: Union[pd.DataFrame, pd.Series],
                              column_names_and_types: Optional[Dict[str, np.dtype]] = None,
                              column_purposes: Optional[List[StatsAndColumnPurposeType]] = None) -> str:
    Contract.assert_type(data, "data", (pd.DataFrame, pd.Series))
    if isinstance(data, pd.DataFrame):
        Contract.assert_value(column_names_and_types, "column_names_and_types")
        col_str_list = []
        column_names_and_types = cast(Dict[str, np.dtype], column_names_and_types)
        for col in column_names_and_types.keys():
            dtype = column_names_and_types[col]
            col_val = _get_dummy_value_by_purpose_or_dtype(npdtype=dtype)
            col_val = json.dumps([col_val]) if isinstance(col_val, str) else [col_val]
            col_str = "{0}: pd.Series({1}, dtype={2})".format(
                json.dumps(str(col)), col_val, json.dumps(str(dtype)))
            col_str_list.append(col_str)
        snapshot_str = "{" + ", ".join(col_str_list) + "}"
    else:
        # data is of type pd.Series
        if not column_purposes:
            # if column_purposes is not set, featurization was turned off
            # construct the column purpose array and set the purpose and raw_stats set to None
            column_purposes = [(None, None, col) for col in range(len(data))]  # type:ignore
        dummy_data = pd.Series([_get_dummy_value_by_purpose_or_dtype(purpose=purpose)  # type:ignore
                                for rawstats, purpose, col in column_purposes])
        snapshot_json_str = dummy_data.to_json(orient='values', date_format='iso')
        snapshot_str = str(json.loads(snapshot_json_str))
    return snapshot_str


def _get_data_snapshot(data: DataInputType, column_names_and_types: Optional[Dict[str, np.dtype]] = None,
                       column_purposes: Optional[List[StatsAndColumnPurposeType]] = None,
                       is_forecasting: bool = False) -> Any:
    Contract.assert_value(data, "data")
    try:
        if isinstance(data, Dataflow) and not column_names_and_types:
            # We need some data to figure out pandas dtypes.
            data = data.take(1000).to_pandas_dataframe()

        Validation.validate_type(data, "data", (np.ndarray, pd.DataFrame, scipy.sparse.spmatrix))

        if isinstance(data, pd.DataFrame) or isinstance(data, Dataflow):
            first_row = data.head(1)
            if not column_names_and_types:
                column_names_and_types = data.dtypes.to_dict()
            df_str = _get_data_snapshot_helper(first_row,
                                               column_names_and_types=column_names_and_types,
                                               column_purposes=column_purposes)
            sample_df_str = 'pd.DataFrame(' + df_str + ')'
            return sample_df_str
        elif isinstance(data, np.ndarray):
            np_array_str = _get_data_snapshot_helper(pd.Series(data[0]), column_purposes=column_purposes)
            sample_numpy_array_str = 'np.array([' + np_array_str + '])'
            return sample_numpy_array_str
        elif scipy.sparse.issparse(data):
            # Assuming that sparse matrix will be inferenced as a numpy array
            # TODO: Test sparse matrices with inference scenario
            np_array_str = _get_data_snapshot_helper(pd.Series(data[0, :].toarray().ravel()),
                                                     column_purposes=column_purposes)
            sample_sparse_array_str = 'np.array([' + np_array_str + '])'
            return sample_sparse_array_str
    except (DataException, ValidationException):
        raise
    except Exception as e:
        exception_error_msg = "Raw data snapshot failed with exception of type: {}".format(type(e))
        logger.error(exception_error_msg)
        error = AzureMLError.create(AutoMLInternal, error_details=exception_error_msg)
        raise ClientException(azureml_error=error, inner_exception=e) from e


def _get_transformer_x(x: DataInputType,
                       y: np.ndarray,
                       dt: DataTransformer,
                       experiment_observer: Optional[ExperimentObserver] = None,
                       verifier: Optional[VerifierManager] = None
                       ) -> Tuple[DataTransformer, Any, str]:
    """
    Given data, compute transformations and transformed data.

    :param x: input data
    :param y: labels
    :param dt:
    :param experiment_observer:
    :param verifier:
    :return:
    """
    if experiment_observer is not None:
        experiment_observer.report_status(
            ExperimentStatus.DatasetFeaturization, "Beginning to fit featurizers and featurize the dataset.")

    data_snapshot_str = _get_data_snapshot(
        x, column_names_and_types=dt._columns_types_mapping, column_purposes=dt.stats_and_column_purposes)

    import azureml.automl.runtime._ml_engine as ml_engine
    x_transform = ml_engine.featurize(x, y, dt)

    if experiment_observer is not None:
        experiment_observer.report_status(
            ExperimentStatus.DatasetFeaturizationCompleted, "Completed fit featurizers and featurizing the dataset.")

    return dt, x_transform, data_snapshot_str


def _get_ts_transformer_x(x,
                          y,
                          timeseries_param_dict,
                          for_cv=False,
                          experiment_observer=None,
                          featurization_config=None,
                          fault_verifier=None):
    """
    Given data, compute transformations and transformed data.

    :param x: input data
    :param y: labels
    :param timeseries_param_dict: timeseries metadata
    :param logger: logger object for logging data from pre-processing
    :param featurization_config: The customized featurization configurations.
    :param fault_verifier: The fault verifier manager.
    :return: transformer, transformed_x
    """
    pipeline_type = TimeSeriesPipelineType.CV_REDUCED if for_cv else TimeSeriesPipelineType.FULL
    tst = TimeSeriesTransformer(
        pipeline_type=pipeline_type, featurization_config=featurization_config, **timeseries_param_dict)

    if fault_verifier is not None:
        fault_verifier.update_data_verifier_for_missing_values_dataframe(
            x, tst._get_numerical_columns(x), tst._featurization_config,
            timeseries_param_dict.get(constants.TimeSeries.DROP_COLUMN_NAMES)
        )

    if experiment_observer is not None:
        message = 'Beginning to featurize the CV split.' if for_cv else 'Beginning to featurize the dataset.'
        experiment_observer.report_status(
            ExperimentStatus.DatasetFeaturization, message)

    data_snapshot_str = _get_data_snapshot(x, is_forecasting=True)
    x_transform = tst.fit_transform(x, y)

    if experiment_observer is not None:
        message = 'Completed featurizing the CV split.' if for_cv else 'Completed featurizing the dataset.'
        experiment_observer.report_status(
            ExperimentStatus.DatasetFeaturizationCompleted, message)

    return tst, x_transform, data_snapshot_str


def _add_raw_column_names_to_X(x_raw_column_names: np.ndarray, X: DataInputType,
                               time_column_name: Optional[str] = None) -> DataInputType:
    """
    Add raw column names to X.

    :param x_raw_column_names: List of raw column names
    :param X: dataframe / array
    :raise ValueError if number of raw column names is not same as the number of columns in X
    :return: Dataframe with column names
    """
    # Combine the raw feature names with X
    if x_raw_column_names is not None:
        if isinstance(X, pd.DataFrame):
            # If X is already a DataFrame, then return X. Assumption here is that raw column names
            # are already present in the data frame header. The passed x_raw_column_names are not
            # needed.
            X = infer_objects_safe(X)
            if time_column_name is not None:
                try:
                    X = frequency_fixer.convert_to_datetime(X, time_column_name)
                except BaseException:
                    pass
            return X
        number_of_columns = 1 if len(X.shape) == 1 else X.shape[1]

        Contract.assert_true(
            x_raw_column_names.shape[0] == number_of_columns,
            "Number of raw column names {} and number of columns in input data {} do not match".format(
                x_raw_column_names.shape[0], number_of_columns)
        )

        if not scipy.sparse.issparse(X):
            # We infer data types to avoid getting data frame, where each column is of object dtype.
            # This significantly decrease memory footprint.
            X_with_raw_columns = pd.DataFrame(
                data=X, columns=x_raw_column_names.tolist())
            X_with_raw_columns = infer_objects_safe(X_with_raw_columns)
            # Do our best to convert time_column_name to datetime.
            if time_column_name is not None:
                try:
                    X_with_raw_columns = frequency_fixer.convert_to_datetime(X_with_raw_columns, time_column_name)
                except BaseException:
                    pass
            return X_with_raw_columns
        else:
            X_with_raw_columns = pd.SparseDataFrame(
                data=X, columns=x_raw_column_names.tolist())
            return X_with_raw_columns

    return X


def infer_objects_safe(X: pd.DataFrame) -> pd.DataFrame:
    """
    Try to infer objects in the data frame in a safe way.

    :param X: The data frame to be fixed.
    :return: The same data frame instance with the bad timestamps replaced.
    """
    try:
        X = X.infer_objects()
    except pd.errors.OutOfBoundsDatetime:
        # pandas > 0.23 seems to correctly handle these large times,
        # while pandas <= 0.23 seems to raise OutOfBoundsDatetime
        X = convert_bad_timestamps_to_strings(X)
        X = X.infer_objects()
    return X


def convert_bad_timestamps_to_strings(X: pd.DataFrame) -> pd.DataFrame:
    """
    Convert bad time stamps to strings.

    Pandas does not support dates earlier than 1677-09-21 00:12:43.145225 or
    later than 2262-04-11 23:47:16.854775807. Here we replace these timestamps with
    string values.
    :param X: The data frame to be fixed.
    :return: The same data frame instance with the bad timestamps replaced.
    """
    min_t = pd.Timestamp.min.to_datetime64().astype('datetime64[ms]')
    max_t = pd.Timestamp.max.to_datetime64().astype('datetime64[ms]')
    for column in X.columns:
        X[column] = X.apply(
            lambda x: str(x[column]) if isinstance(x[column], np.datetime64) and
            (x[column].astype('datetime64[ns]') < min_t or x[column].astype('datetime64[ns]') > max_t) else x[column],
            axis=1)
    return X


def _y_transform(
        y: np.ndarray, y_valid: Optional[np.ndarray], task_type: str
) -> Tuple[Optional[preprocessing.LabelEncoder], np.ndarray, Optional[np.ndarray]]:
    """
    Apply label encoder for string, float and negative int type y data.

    :param y: y data
    :param y_valid: Validation y data
    :param task_type: CLASSIFICATION/REGRESSION
    :return:
    """
    y_transformer = None
    if task_type == constants.Tasks.CLASSIFICATION:
        y_type = runtime_utilities._get_column_data_type_as_str(y)
        y_valid_type = None if y_valid is None else runtime_utilities._get_column_data_type_as_str(y_valid)
        if runtime_utilities._is_y_transform_needed(y, y_type) or \
                runtime_utilities._is_y_transform_needed(y_valid, y_valid_type):
            # Currently y_transformer only support the label encoder for negative, float and categorical data.
            y_is_numeric = utilities._check_if_column_data_type_is_numerical(y_type)
            if y_valid is None:
                if runtime_utilities._is_y_mixed_type(y_type) and not y_is_numeric:
                    y = pd.Series(y).apply(str).values
            else:
                y_valid_type = str(y_valid_type)
                y_valid_is_numeric = utilities._check_if_column_data_type_is_numerical(y_valid_type)
                if runtime_utilities._is_y_conversion_needed(y_type, y_is_numeric, y_valid_type, y_valid_is_numeric):
                    y = pd.Series(y).apply(str).values
                if runtime_utilities._is_y_conversion_needed(y_valid_type, y_valid_is_numeric, y_type, y_is_numeric):
                    y_valid = pd.Series(y_valid).apply(str).values

            logger.info("Start doing label encoding on y data.")
            y_transformer = preprocessing.LabelEncoder()
            if y_valid is None:
                le = y_transformer.fit(y)
                y = le.transform(y)
            else:
                le = y_transformer.fit(np.vstack([y.reshape(-1, 1), y_valid.reshape(-1, 1)]))
                y = le.transform(y)
                y_valid = le.transform(y_valid)
            logger.info("End doing label encoding on y data.")
    return y_transformer, y, y_valid


def _class_balancing_check(y, y_transformer):
    """
    Class balancing check based on y distribution.
    Imbalance would be detected if the Size of the minority class/Size of the majority class <= 20%.
    Comparison between minority & majority class, as opposed to minority class & overall training samples,
    makes more sense as demonstrated with this example:

    For a four class problem with data distributed among labels like this:{'a': 20, 'b': 20, 'c': 20, 'd': 200},
    the fraction of minority to majority is 10%, while minority to overall is 7.7%.

    For a four class problem with data distributed among labels like this:{'a': 20, 'b': 200, 'c': 200, 'd': 200},
    the fraction of minority to majority is 10%, while minority to overall is 3.2%.

    The first fraction is consistent, regardless of other classes and hence gives a more stable estimate of what
    clearly is an imbalance.

    :param y: Training y data
    :param y_transformer: Label-Encoder/Transformer used to encode target/label values
    :return: is class imbalanced, size of smallest class in y, name of smallest class in y
    """
    logger.info("Start checking class balancing on y data.")
    if y_transformer is not None:
        y = y_transformer.inverse_transform(y)
    labels, counts = np.unique(y, return_counts=True)
    is_class_imbalanced = False
    if float(min(counts)) <= constants.CheckImbalance.MINORITY_TO_MAJORITY_THRESHOLD_RATIO * float(max(counts)):
        is_class_imbalanced = True
    if is_class_imbalanced:
        logger.info("Classes are imbalanced in training data.")

    size_of_smallest_class = min(counts)
    name_of_smallest_class = labels[np.argwhere(counts == size_of_smallest_class)]
    name_of_smallest_class = ', '.join(map(str, name_of_smallest_class.flatten()))
    return is_class_imbalanced, size_of_smallest_class, name_of_smallest_class


def _create_cv_splits_transformed_data(transformed_data_context: TransformedDataContext,
                                       raw_data_context: RawDataContext, X: np.ndarray, y: np.ndarray,
                                       sample_weight: Optional[np.ndarray],
                                       experiment_observer: ExperimentObserver) -> None:
    """
    Create featurized data for individual CV splits using the data transformer and lagging trransformer.

    :param raw_data_context: The raw data context.
    :param X: Raw training data
    :param y: Raw output variable data
    :param sample_weight: Sample weight
    :return:
    """
    # Check if CV splits need to featurized
    if transformed_data_context.num_cv_folds is not None or \
        (transformed_data_context.validation_size is not None and
         transformed_data_context.validation_size > 0.0) or \
            transformed_data_context.cv_splits_indices is not None:

        logger.info("Creating cross validations")

        if skip_featurization(raw_data_context.featurization):
            experiment_observer.report_status(
                ExperimentStatus.DatasetCrossValidationSplit,
                "Generating CV splits.")
        else:
            experiment_observer.report_status(
                ExperimentStatus.DatasetCrossValidationSplit,
                "Generating individually featurized CV splits.")

        # Add raw column names to raw training data
        time_colname = None
        if raw_data_context.timeseries_param_dict is not None and raw_data_context.timeseries:
            time_colname = raw_data_context.timeseries_param_dict.get(TimeSeries.TIME_COLUMN_NAME)
        raw_X = _add_raw_column_names_to_X(raw_data_context.x_raw_column_names, X, time_colname)
        raw_y = y

        # If we have a time seriesdata frame with heuristic parameters, we need to replace these parameters.
        # If it is not a time series, just set ts_param_dict_copy to be a
        # reference on raw_data_context.timeseries_param_dict
        ts_param_dict_copy = raw_data_context.timeseries_param_dict
        if raw_data_context.timeseries and raw_data_context.timeseries_param_dict is not None:
            # If raw_data_context.timeseries_param_dict contains data, swap all auto parameters to be
            # inferenced parameters.
            logger.info("Timeseries param dict contains data, inferencing parameters.")
            ts_param_dict_copy = raw_data_context.timeseries_param_dict.copy()
            tst = transformed_data_context.transformers.get(Transformers.TIMESERIES_TRANSFORMER)
            if tst is not None:
                # Swap the auto parameters by theit inferenced values.
                if ts_param_dict_copy.get(TimeSeries.MAX_HORIZON) == TimeSeries.AUTO:
                    ts_param_dict_copy[TimeSeries.MAX_HORIZON] = tst.max_horizon
                if ts_param_dict_copy.get(TimeSeriesInternal.WINDOW_SIZE) == TimeSeries.AUTO:
                    rw_transform = tst.pipeline.get_pipeline_step(TimeSeriesInternal.ROLLING_WINDOW_OPERATOR)
                    if rw_transform is not None:
                        ts_param_dict_copy[TimeSeriesInternal.WINDOW_SIZE] = rw_transform.window_size
                lags_dict = cast(Dict[str, Any], ts_param_dict_copy.get(TimeSeriesInternal.LAGS_TO_CONSTRUCT))
                if lags_dict and lags_dict.get(tst.target_column_name) == [TimeSeries.AUTO]:
                    lag_lead = tst.pipeline.get_pipeline_step(TimeSeriesInternal.LAG_LEAD_OPERATOR)
                    if lag_lead is not None:
                        ts_param_dict_copy[TimeSeriesInternal.LAGS_TO_CONSTRUCT] = lag_lead.lags_to_construct
                # If the short grains will be removed from the series, we need to make sure that the corresponding
                # grains will not get to the rolling origin validator, and it will not fail.
                short_series_processor = tst.pipeline.get_pipeline_step(TimeSeriesInternal.SHORT_SERIES_DROPPEER)
                # Despite ts_param_dict_copy should return Optional[str], we know that grains internally
                # are represented by Optional[List[str]].
                grains = cast(Optional[List[str]], ts_param_dict_copy.get(TimeSeries.GRAIN_COLUMN_NAMES))
                # If short series are being dropped and if there are grains, drop them.
                # Note: if there is no grains i.e. data set contains only one grain, and it have to be dropped,
                # we will show error on the initial data transformation.
                if short_series_processor is not None and short_series_processor.has_short_grains_in_train\
                        and grains is not None and len(grains) > 0:
                    # Preprocess raw_X so that it will not contain the short grains.
                    dfs = []
                    raw_X[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = raw_y
                    for grain, df in raw_X.groupby(grains):
                        if grain in short_series_processor.grains_to_keep:
                            dfs.append(df)
                    raw_X = pd.concat(dfs)
                    raw_y = raw_X.pop(TimeSeriesInternal.DUMMY_TARGET_COLUMN).values
                    del dfs

        # Create CV splits object
        transformed_data_context.cv_splits = \
            _CVSplits(raw_X, raw_y,
                      frac_valid=transformed_data_context.validation_size,
                      CV=transformed_data_context.num_cv_folds,
                      cv_splits_indices=transformed_data_context.cv_splits_indices,
                      is_time_series=raw_data_context.timeseries,
                      timeseries_param_dict=ts_param_dict_copy,
                      task=raw_data_context.task_type)
        logger.info("Found cross validation type: " + str(transformed_data_context.cv_splits._cv_split_type))

        # If data transformer or lagging transformers are valid, then featurize individual CV splits
        if transformed_data_context.transformers[constants.Transformers.X_TRANSFORMER] is not None or \
                transformed_data_context.transformers[constants.Transformers.LAG_TRANSFORMER] is not None or \
                transformed_data_context.transformers[constants.Transformers.TIMESERIES_TRANSFORMER] is not None:

            data_transformer = transformed_data_context.transformers[constants.Transformers.X_TRANSFORMER]
            lag_transformer = transformed_data_context.transformers[constants.Transformers.LAG_TRANSFORMER]
            ts_transformer = transformed_data_context.transformers[constants.Transformers.TIMESERIES_TRANSFORMER]

            if transformed_data_context.cv_splits.get_cv_split_indices() is not None:
                logger.info("Creating featurized version of CV splits data")

                # Walk all CV split indices and featurize individual train and validation set pair
                transformed_data_context.cv_splits._featurized_cv_splits = []
                cv_split_index = 0
                for X_train, y_train, sample_wt_train, X_test, y_test, sample_wt_test \
                        in transformed_data_context.cv_splits.apply_CV_splits(raw_X, raw_y, sample_weight):
                    logger.info("Processing a CV split at index {}.".format(cv_split_index))
                    if X_test.shape[0] == 0:
                        if transformed_data_context.timeseries:
                            raise DataException._with_error(AzureMLError.create(
                                TimeseriesLaggingNans, target="X",
                                reference_code=ReferenceCodes._DATA_TRANSFORMATION_TEST_EMPTY_TS)
                            )
                        else:
                            # todo check if/when this branch is reachable for non-timeseries task, and improve
                            # the error message for the user (if this is indeed due to invalid user inputs)
                            raise DataException._with_error(AzureMLError.create(
                                InputDatasetEmpty, target="X",
                                reference_code=ReferenceCodes._DATA_TRANSFORMATION_TEST_EMPTY)
                            )
                    if data_transformer is not None:
                        logger.info("Data transformer present, running transform operations.")
                        X_train = data_transformer.fit_transform(X_train, y_train)
                        X_test = data_transformer.transform(X_test)

                    if lag_transformer is not None:
                        logger.info("Lag transformer present, running transform operations.")
                        X_train = lag_transformer.fit_transform(X_train, y_train)
                        X_test = lag_transformer.transform(X_test)

                    if ts_transformer is not None:
                        Contract.assert_true(raw_data_context.timeseries_param_dict is not None,
                                             "Expected non-none timeseries parameter dict", log_safe=True)
                        logger.info("Time series transformer present, running transform operations.")
                        # Need to do pipeline introspection on ts_transformer for CV featurization.
                        # For compatibility with old SDK versions, re-compute the ts_transformer feature graph
                        # if it is not set
                        ts_transformer._create_feature_transformer_graph_if_not_set(raw_X, y=raw_y)

                        # Get list of time index features used on full train set fit
                        non_holiday_features = ts_transformer.time_index_non_holiday_features
                        ts_split_param_dict = {}
                        if raw_data_context.timeseries_param_dict is not None:
                            ts_split_param_dict = raw_data_context.timeseries_param_dict.copy()
                        # Make sure we use the frequency inferred on all the data frame, but not on
                        # smaller validation part.
                        ts_split_param_dict[TimeSeries.FREQUENCY] = ts_transformer.freq_offset
                        ts_split_param_dict[constants.TimeSeries.SEASONALITY] = ts_transformer.seasonality
                        ts_split_param_dict[constants.TimeSeriesInternal.FORCE_TIME_INDEX_FEATURES_NAME] = \
                            non_holiday_features

                        ts_split_transformer, X_train, _ = \
                            _get_ts_transformer_x(X_train, y_train, ts_split_param_dict,
                                                  for_cv=True,
                                                  experiment_observer=experiment_observer,
                                                  featurization_config=raw_data_context.featurization)
                        # Join with full featurized set to get re-useable features
                        X_train = \
                            TimeSeriesTransformer._join_reusable_features_for_cv(ts_split_transformer, X_train,
                                                                                 ts_transformer,
                                                                                 transformed_data_context.X)

                        if ts_split_transformer.target_column_name in X_train.columns:
                            y_train = X_train.pop(ts_split_transformer.target_column_name).values

                        if X_train.shape[0] == 0:
                            # This can happen only if we have long target_lag or rolling window size
                            # and leading NaNs which were not trimmed during pre processing step.
                            raise DataException._with_error(AzureMLError.create(
                                TimeseriesLeadingNans, target="X",
                                reference_code=ReferenceCodes._DATA_TRANSFORMATION_TRAIN_EMPTY)
                            )

                        X_test = ts_split_transformer.transform(X_test, y_test)
                        X_test = \
                            TimeSeriesTransformer._join_reusable_features_for_cv(ts_split_transformer, X_test,
                                                                                 ts_transformer,
                                                                                 transformed_data_context.X)

                        # Need to apply some corrections when data has horizon-dependent features (i.e. Lags/RW)
                        if ts_transformer.origin_column_name in X_test.index.names:
                            # X_test may have some origin times later than the latest known train times
                            latest_known_dates = \
                                {gr: df.index.get_level_values(ts_transformer.time_column_name).max()
                                 for gr, df in X_train.groupby(ts_transformer.grain_column_names)}
                            X_test = (X_test.groupby(ts_transformer.grain_column_names, group_keys=False)
                                      .apply(lambda df:
                                             ts_transformer._select_known_before_date(df, latest_known_dates[df.name],
                                                                                      ts_transformer.freq_offset)))

                            # To match forecasting logic, select predictions made from most recent origin times
                            X_test = ts_transformer._select_latest_origin_dates(X_test)
                            if X_test.shape[0] == 0:
                                # This happens when we do not have enough data points
                                # at the end of data set to generate lookback features for
                                # validation set (trimmed in _select_latest_origin_dates).
                                raise DataException._with_error(AzureMLError.create(
                                    TimeseriesLaggingNans, target="X_test",
                                    reference_code=ReferenceCodes._DATA_TRANSFORMATION_TS_INSUFFICIENT_DATA)
                                )
                        if ts_split_transformer.target_column_name in X_test.columns:
                            y_test = X_test.pop(ts_split_transformer.target_column_name).values

                    # Create the featurized CV split object
                    featurized_cv = FeaturizedCVSplit(
                        X_train, y_train, sample_wt_train,
                        X_test, y_test, sample_wt_test, None, None)

                    logger.info(str(featurized_cv))

                    # Flush the featurized data on the cache store
                    transformed_data_context._update_cache_with_featurized_data(
                        TransformedDataContext.FEATURIZED_CV_SPLIT_KEY_INITIALS +
                        str(cv_split_index), featurized_cv)

                    # Clear the in-memory data for the featurized data and record the cache store and key
                    featurized_cv._clear_featurized_data_and_record_cache_store(
                        transformed_data_context.cache_store,
                        TransformedDataContext.FEATURIZED_CV_SPLIT_KEY_INITIALS + str(cv_split_index))

                    cv_split_index += 1

                    # Append to the list of featurized CV splits
                    transformed_data_context.cv_splits._featurized_cv_splits.append(featurized_cv)

            else:
                logger.info("Creating featurized data for train and validation data")

                if raw_data_context.timeseries:
                    raise ConfigException._with_error(AzureMLError.create(
                        ArgumentBlankOrEmpty, argument_name="n_cross_validations", target="n_cross_validations")
                    )

                X_train, y_train, sample_weight_train, X_valid, y_valid, \
                    sample_weight_valid, _, _, _ = \
                    transformed_data_context.cv_splits.get_train_validation_test_chunks(raw_X, raw_y, sample_weight)

                if data_transformer is not None:
                    logger.info("Data transformer present, running transform operations.")
                    if X_train is not None:
                        X_train = data_transformer.fit_transform(X_train, y_train)
                    if X_valid is not None:
                        X_valid = data_transformer.transform(X_valid)

                if lag_transformer is not None:
                    logger.info("Lag transformer present, running transform operations.")
                    if X_train is not None:
                        X_train = lag_transformer.fit_transform(X_train, y_train)
                    if X_valid is not None:
                        X_valid = lag_transformer.transform(X_valid)

                # Create the featurized train, valid and test object
                featurized_train_test_valid = FeaturizedTrainValidTestSplit(
                    X_train, y_train, sample_weight_train,
                    X_valid, y_valid, sample_weight_valid,
                    None, None, None, None, None)

                logger.info(str(featurized_train_test_valid))

                # Flush the featurized data on the cache store
                transformed_data_context._update_cache_with_featurized_data(
                    TransformedDataContext.FEATURIZED_TRAIN_TEST_VALID_KEY_INITIALS,
                    featurized_train_test_valid)

                # Clear the in-memory data for the featurized data and record the cache store and key
                featurized_train_test_valid._clear_featurized_data_and_record_cache_store(
                    transformed_data_context.cache_store,
                    TransformedDataContext.FEATURIZED_TRAIN_TEST_VALID_KEY_INITIALS)

                transformed_data_context.cv_splits._featurized_train_test_valid_chunks = featurized_train_test_valid

        logger.info("Completed creating cross-validation folds and featurizing them")


def _perform_class_balancing_sweeping(task_type: str, df: DataInputType,
                                      y: DataSingleColumnInputType,
                                      enable_class_balancing: bool,
                                      working_dir: str,
                                      experiment_observer: Optional[ExperimentObserver] = None,
                                      feature_sweeping_config: Dict[str, Any] = {},
                                      is_cross_validation: bool = False) -> Dict[str, Any]:
    """
    Perform sweeping over balancing strategies and return name of balancing strategies which outperforms
    the original metrics.

    :param task_type: Task type.
    :param df: Input data frame.
    :param y: Input labels.
    :param enable_class_balancing: Boolean
    :param feature_sweeping_config: Enable or disable balancing.
    :param is_cross_validation: Whether to do the cross validation
    :return: Use class weight, class weight
    """
    if experiment_observer is not None:
        experiment_observer.report_status(ExperimentStatus.DatasetBalancing,
                                          "Performing class balancing sweeping")
    try:
        if enable_class_balancing:
            logger.info("Performing class balancing sweeping")

            from azureml.automl.runtime.sweeping.meta_sweeper import MetaSweeper

            balancing_sweeper = MetaSweeper(task=task_type,
                                            timeout_sec=3600,
                                            is_cross_validation=is_cross_validation,
                                            feature_sweeping_config=feature_sweeping_config)

            balancing_result = balancing_sweeper.sweep(working_dir, df, y, sweeping_mode=SweepingMode.Balancing)
            logger.info("Finished class balancing sweeping")
            if balancing_result is not None:
                for balancer in balancing_result:
                    if balancer == "ClassWeight":
                        logger.info("Adding class weight to data context")
                        weights = _compute_sample_weight(y)
                        return {'weights': weights}
            return {}
    except Exception as e:
        # Never fail the main run even if sweeping fails.
        logging_utilities.log_traceback(e, logger)

    return {}


def _compute_sample_weight(y: DataSingleColumnInputType) -> np.ndarray:
    """
    Compute sample weight based on class weight.

    :param y: Input labels.
    :return: sample weights.
    """

    unique_vals = np.unique(y)

    class_weight = compute_class_weight('balanced', unique_vals, y)
    weights = {uniq: weight for uniq, weight in zip(unique_vals, class_weight)}
    sample_class_weight = [weights[label] for label in y]

    return np.array(sample_class_weight)
