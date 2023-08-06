# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Preprocessing class that can be added in pipeline for input."""
import json
import logging
import math
import os
from typing import Any, cast, Dict, List, Mapping, Optional, Tuple, Union

import numpy as np
import pandas as pd
from azureml._common._error_definition import AzureMLError
from azureml._common._error_definition.user_error import ArgumentBlankOrEmpty
from azureml.automl.runtime._engineered_feature_names import (_FeatureTransformers, _GenerateEngineeredFeatureNames,
                                                              _Transformer, _TransformerParamsHelper)
from azureml.automl.runtime.column_purpose_detection import ColumnPurposeDetector
from azureml.automl.runtime.column_purpose_detection import ColumnPurposeSweeper
from azureml.automl.runtime.column_purpose_detection import StatsAndColumnPurposeType
from azureml.automl.runtime.featurization import data_transformer_utils
from azureml.automl.runtime.featurization_info_provider import FeaturizationInfoProvider
from azureml.automl.runtime.shared import utilities as runtime_utilities, memory_utilities
from azureml.automl.runtime.shared.types import (TransformerType,
                                                 DataInputType,
                                                 DataSingleColumnInputType,
                                                 FeaturizationSummaryType)
from pandas.core.indexes.base import Index
from pandas.core.series import Series
from scipy import sparse
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn_pandas import DataFrameMapper

from azureml.automl.core._experiment_observer import ExperimentStatus, ExperimentObserver, NullExperimentObserver
from azureml.automl.core.constants import (FeatureType as _FeatureType,
                                           SupportedTransformersInternal as _SupportedTransformersInternal,
                                           _TransformerOperatorMappings, TextNeuralNetworks,
                                           _OperatorNames)
from azureml.automl.core.featurization.featurizationconfig import FeaturizationConfig
from azureml.automl.core.shared import constants, logging_utilities, utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    DatasetsFeatureCountMismatch,
    FeaturizationConfigParamOverridden,
    InconsistentColumnTypeInTrainValid,
    InsufficientMemory,
    MissingColumnsInData,
    UnrecognizedFeatures
)
from azureml.automl.core.shared.exceptions import (
    AutoMLException,
    ConfigException,
    DataException,
    FitException,
    ResourceException,
    TransformException
)
from azureml.automl.core.shared.pickler import DefaultPickler
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.transformer_runtime_exceptions import (
    DataTransformerUnknownTaskException)
from ._featurized_data_combiners import FeaturizedDataCombiners
from ._featurizer_container import FeaturizerContainer
from .generic_transformer import GenericTransformer
from .text_transformer import TextTransformer
from .transformer_and_mapper import TransformerAndMapper
from ..featurizer.transformer import (AutoMLTransformer, CategoricalFeaturizers, DateTimeFeaturesTransformer,
                                      featurization_utilities, GenericFeaturizers, get_ngram_len, TextFeaturizers)
from ..stats_computation import PreprocessingStatistics as _PreprocessingStatistics

logger = logging.getLogger(__name__)


class DataTransformer(AutoMLTransformer, FeaturizationInfoProvider):
    """
    Preprocessing class that can be added in pipeline for input.

    This class does the following:
    1. Numerical inputs treated as it is.
    2. For dates: year, month, day and hour are features
    3. For text, tfidf features
    4. Small number of unique values for a column that is not float become
        categoricals

    :param task: 'classification' or 'regression' depending on what kind of
    ML problem to solve.
    :param is_onnx_compatible: if works in onnx compatible mode.
    """

    DEFAULT_DATA_TRANSFORMER_TIMEOUT_SEC = 3600 * 24  # 24 hours
    UNSUPPORTED_PARAMETER_WARNING_MSG = "Unsupported parameter passed to {t}, proceeding with default values"
    FIT_FAILURE_MSG = "Failed while fitting learned transformations."
    TRANSFORM_FAILURE_MSG = "Failed while applying learned transformations."

    def __init__(self,
                 task: Optional[str] = constants.Tasks.CLASSIFICATION,
                 is_onnx_compatible: bool = False,
                 logger: Optional[logging.Logger] = None,
                 observer: Optional[ExperimentObserver] = None,
                 enable_feature_sweeping: bool = False,
                 enable_dnn: bool = False,
                 force_text_dnn: bool = False,
                 feature_sweeping_timeout: int = DEFAULT_DATA_TRANSFORMER_TIMEOUT_SEC,
                 featurization_config: Optional[FeaturizationConfig] = None,
                 is_cross_validation: bool = False,
                 feature_sweeping_config: Dict[str, Any] = {},
                 working_dir: Optional[str] = None) -> None:
        """
        Initialize for data transformer for pre-processing raw user data.

        :param task: 'classification' or 'regression' depending on what kind
        of ML problem to solve.
        :type task: str or azureml.train.automl.constants.Tasks
        :param is_onnx_compatible: If works in onnx compatible mode.
        :param logger: External logger handler.
        :param enable_feature_sweeping: Whether to run feature sweeping or not.
        :param enable_dnn: Flag to enable neural networks for forecasting and natural language processing.
        :param force_text_dnn: Flag to force add dnn's for natural language processing via feature sweeping.
        :param feature_sweeping_timeout: Max time to run feature sweeping.
        :param featurization_config: Configuration used for custom featurization.
        :param is_cross_validation: Whether to do the cross validation.
        :param feature_sweeping_config: Feature sweeping config.
        :param working_dir: the working directory to use for temporary files.
        """
        super().__init__()
        self._is_inference_time = False
        if task not in constants.Tasks.ALL:
            raise DataTransformerUnknownTaskException(
                "Unknown task", has_pii=False, reference_code=ReferenceCodes._DATA_TRANSFORMER_UNKNOWN_TASK)

        # TODO: Remove this
        self.logger = logger

        self.working_directory = working_dir or os.getcwd()
        self._task_type = task or constants.Tasks.CLASSIFICATION
        self._is_onnx_compatible = is_onnx_compatible
        self._is_text_dnn = False
        self.mapper = None  # type: Optional[DataFrameMapper]
        self._init_logger(logger)  # External logger if None, then no logs
        # list of TrasformerAndMapper objects
        self.transformer_and_mapper_list = []  # type: List[TransformerAndMapper]
        # Maintain a list of raw feature names
        self._raw_feature_names = []  # type: List[str]
        # Maintain engineered feature name class
        self._engineered_feature_names_class = \
            _GenerateEngineeredFeatureNames()  # type: Optional[_GenerateEngineeredFeatureNames]
        # Maintain statistics about the pre-processing stage
        self._pre_processing_stats = _PreprocessingStatistics()
        # Text transformer
        self._text_transformer = None  # type: Optional[TextTransformer]
        # Stats and column purpose
        self.stats_and_column_purposes = None  # type: Optional[List[StatsAndColumnPurposeType]]
        # Generic transformer
        # TODO Need to enable this later
        self._generic_transformer = None  # type: Optional[GenericTransformer]
        self._observer = observer or NullExperimentObserver()  # type: ExperimentObserver
        self._enable_feature_sweeping = enable_feature_sweeping
        self._enable_dnn = enable_dnn
        self._force_text_dnn = force_text_dnn
        self._feature_sweeping_config = feature_sweeping_config
        self._feature_sweeping_timeout = feature_sweeping_timeout
        self._is_cross_validation = is_cross_validation

        self._logger_wrapper("info", "Feature sweeping enabled: {}".format(self._enable_feature_sweeping))
        self._logger_wrapper("info", "Feature sweeping timeout: {}".format(self._feature_sweeping_timeout))

        # Used for injecting test transformers.
        self._test_transforms = []  # type: List[Any]
        self._columns_types_mapping = None  # type: Optional[Dict[str, np.dtype]]
        self._featurization_config = featurization_config
        self._feature_sweeped = False
        # empty featurizer list
        self._featurizer_container = FeaturizerContainer(featurizer_list=[])

    @logging_utilities.function_debug_log_wrapped()
    def _learn_transformations(self, df: DataInputType,
                               stats_and_column_purposes: List[StatsAndColumnPurposeType],
                               y: DataSingleColumnInputType = None) -> List[TransformerAndMapper]:
        """
        Learn data transformation to be done on the raw data.

        :param df: Dataframe representing text, numerical or categorical input.
        :param stats_and_column_purposes: Statistics and column purposes of the given data.
        :param y: To match fit signature.
        """
        runtime_utilities.check_input(df)
        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)

        if self._engineered_feature_names_class is None:
            # Create class for engineered feature names
            self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()

        # Column purpose determination and stats computation
        self._observer.report_status(
            ExperimentStatus.DatasetEvaluation, "Gathering dataset statistics.")

        transforms = self._get_transforms(df, stats_and_column_purposes, y)
        if self._is_onnx_compatible:
            self.mapper = DataFrameMapper(transforms, input_df=True, sparse=True)
        else:
            transformer_and_mapper_list = []
            for transformers in transforms:
                transform_and_mapper = TransformerAndMapper(transformers=transformers[1],
                                                            mapper=DataFrameMapper([transformers],
                                                                                   input_df=True, sparse=True))
                transformer_and_mapper_list.append(transform_and_mapper)
                self._set_is_text_dnn_if_available(transform_and_mapper)
            return transformer_and_mapper_list
        return []

    def _add_test_transforms(self, transforms: List[Any]) -> None:
        self._test_transforms.extend(transforms)

    def fit_transform_with_logger(self,
                                  X: DataInputType,
                                  y: Optional[DataInputType] = None,
                                  logger: Optional[logging.Logger] = None,
                                  **fit_params: Any) -> Union[pd.DataFrame, np.ndarray, sparse.spmatrix]:
        """
        Wrap the fit_transform function for the Data transformer class.

        :param X: Dataframe representing text, numerical or categorical input.
        :type X:numpy.ndarray or pandas.DataFrame
        :param y: To match fit signature.
        :type y: numpy.ndarray or pandas.DataFrame
        :param logger: External logger handler.
        :type logger: logging.Logger
        :param fit_params: Additional parameters for fit_transform().
        :return: Transformed data.
        """
        # Init the logger
        self.logger = logger

        # Call the fit and transform function
        transform_out = self.fit_transform(X, y, **fit_params)  # type: Union[pd.DataFrame, np.ndarray]
        return transform_out

    def configure_featurizers(self, df: DataInputType, y: DataSingleColumnInputType = None) -> None:
        """
        Run column type mappings, column purpose detection and feature sweeping.

        :param df: Dataframe representing text, numerical or categorical input.
        :param y: To match fit signature.
        :return: None
        """
        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)

        if self._columns_types_mapping is None:
            self._columns_types_mapping = data_transformer_utils.get_pandas_columns_types_mapping(df)

        # checking two conditions due onnx compatibilty issues.
        if (self._is_onnx_compatible and not self.mapper) or (not self.transformer_and_mapper_list):
            self._logger_wrapper(
                'info', 'Featurizer mapper not found so learn all ' + 'the transforms')
            self.stats_and_column_purposes = ColumnPurposeDetector.get_raw_stats_and_column_purposes(df)
            # update stats and column purposes based on customized featurization config column purpose setting
            self._update_customized_feature_types()
            self.transformer_and_mapper_list = self._learn_transformations(df, self.stats_and_column_purposes, y)
        self._feature_sweeped = True
        if self._engineered_feature_names_class is None:
            self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()

    @logging_utilities.function_debug_log_wrapped()
    def fit(self, df: DataInputType,
            y: Optional[DataSingleColumnInputType] = None) -> "DataTransformer":
        """
        Perform the raw data validation and identify the transformations to apply.

        :param df: The input data object representing text, numerical or categorical input.
        :param y: The target column data.
        :return: The DataTransformer object.
        :raises: FitException if fitting the learned transformations fail.
        """
        self._is_inference_time = False
        runtime_utilities.check_input(df)
        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)

        # If feature sweeping hasn't happened yet, run it
        if not self._feature_sweeped and not self.transformer_and_mapper_list:
            self.configure_featurizers(df, y)

        fitted_featurizer_indices = {featurizer.index for featurizer
                                     in self._featurizer_container if featurizer.is_cached}

        if self._is_onnx_compatible and self.mapper is not None:
            try:
                fitted_featurizers = {}
                for index in range(len(self.mapper.features)):
                    if index in fitted_featurizer_indices:
                        featurizer = self.mapper.features[index]
                        fitted_featurizers[index] = featurizer
                        # replace the featurizer in the mapper with a copy that will not be re-fitted.
                        self.mapper.features[index] = \
                            data_transformer_utils.get_feature_that_avoids_refitting(featurizer)
                self.mapper.fit(df, y)
                for index in fitted_featurizers:
                    # restore the mapper with the previously fitted featurizers.
                    self.mapper.features[index] = fitted_featurizers[index]
            except AutoMLException:
                raise
            except MemoryError as e:
                raise ResourceException._with_error(
                    AzureMLError.create(
                        InsufficientMemory,
                        target='MapperFit',
                        reference_code=ReferenceCodes._DATA_TRANSFORMER_FIT_MAPPER_MEMORYERROR,
                    ), inner_exception=e) from e
            except Exception as ex:
                fit_exception = FitException.from_exception(
                    ex,
                    msg=self.FIT_FAILURE_MSG,
                    target='DataTransformer',
                    has_pii=False,
                    reference_code=ReferenceCodes._DATA_TRANSFORMER_FIT_ONNX_COMPATIBLE)  # type: Exception
                raise fit_exception
            return self

        if not self.transformer_and_mapper_list:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ArgumentBlankOrEmpty, target="transformer_and_mapper_list",
                    argument_name="transformer_and_mapper_list",
                    reference_code=ReferenceCodes._DATA_TRANSFORMER_FIT_FEATCONFIG_NONE
                )
            )

        for index in range(len(self.transformer_and_mapper_list)):
            transformer_mapper = self.transformer_and_mapper_list[index]
            self._set_is_text_dnn_if_available(transformer_mapper)
            if index not in fitted_featurizer_indices:  # we haven't already fitted
                self.fit_individual_transformer_mapper(transformer_mapper, df, y)
        return self

    def fit_individual_transformer_mapper(self, transformer_mapper: TransformerAndMapper,
                                          df: DataInputType, y: Optional[DataSingleColumnInputType] = None) -> None:
        is_text_dnn = self._get_is_text_dnn()
        if is_text_dnn:
            self._observer.report_status(
                ExperimentStatus.TextDNNTraining,
                "Training a deep learning text model, this may take a while.")

            has_observer = not isinstance(self._observer, NullExperimentObserver)

            # pt_dnn transformers require an instance of the current run to log progress
            if self._get_is_BERT(transformer_mapper) and has_observer:
                pt_dnn = transformer_mapper.transformers.steps[-1][-1].steps[-1][-1]  # type: ignore
                pt_dnn.observer = self._observer

        try:
            transformer_mapper.mapper.fit(df, y)
        except AutoMLException:
            raise
        except MemoryError as e:
            raise ResourceException._with_error(
                AzureMLError.create(
                    InsufficientMemory,
                    target='TransformerMapperFit',
                    reference_code=ReferenceCodes._DATA_TRANSFORMER_FIT_DATAFRAME_MAPPER_MEMORYERROR,
                ), inner_exception=e) from e
        except Exception as ex:
            if isinstance(ex, ValueError) and \
                    'After pruning, no terms remain. Try a lower min_df or a higher max_df.' in ex.args[0]:
                # TODO: Below is fix for bug #611949.
                #  Need to have a complete solution for TfIdf parameter adjustments: Work item #617820
                self._logger_wrapper('info',
                                     'TfIdf ValueError caused by adjusted min_df or max_df. '
                                     'Retrying fit with default value.')
                try:
                    from sklearn.feature_extraction.text import TfidfVectorizer
                    for tr in transformer_mapper.mapper.features[0][1]:
                        if isinstance(tr, TfidfVectorizer):
                            if tr.max_df < 1.0:
                                tr.max_df = 1.0
                            if tr.min_df != 1:
                                tr.min_df = 1
                    transformer_mapper.mapper.fit(df, y)
                except Exception:
                    fit_exception = FitException.from_exception(
                        ex,
                        msg='Re-running fit using default min_df and max_df failed.',
                        target='DataTransformer',
                        has_pii=False,
                        reference_code=ReferenceCodes._DATA_TRANSFORMER_FIT_RERUN)
                    raise fit_exception from None
            else:
                self._check_transformer_param_error(ex, True, transformer_mapper)
                raise FitException.from_exception(
                    ex,
                    msg=self.FIT_FAILURE_MSG,
                    target='DataTransformer.fit',
                    has_pii=False,
                    reference_code=ReferenceCodes._DATA_TRANSFORMER_FIT_LEARNED)

        if is_text_dnn:
            self._observer.report_status(
                ExperimentStatus.TextDNNTrainingCompleted, "Completed training a deep learning text model.")

        steps = transformer_mapper.transformers.steps \
            if isinstance(transformer_mapper.transformers, Pipeline) else transformer_mapper.transformers

        transform_count = len(steps)
        if transform_count == 0:
            return
        # Only last transformer gets applied, all other are input to next transformer.
        last_transformer = steps[transform_count - 1]
        last_transformer = last_transformer[1] if isinstance(last_transformer, tuple) and len(
            last_transformer) > 1 else last_transformer
        memory_estimate = (0 if not issubclass(type(last_transformer), AutoMLTransformer)
                           else last_transformer.get_memory_footprint(df, y))
        transformer_mapper.memory_footprint_estimate = memory_estimate

    @logging_utilities.function_debug_log_wrapped()
    def transform(self, df: DataInputType) -> Union[pd.DataFrame, np.ndarray, sparse.spmatrix]:
        """
        Transform the input raw data with the transformations idetified in fit stage.

        :param df: Dataframe representing text, numerical or categorical input.
        :type df: numpy.ndarray or pandas.DataFrame
        :return: Numpy array.
        """
        runtime_utilities.check_input(df)
        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)

        if self._columns_types_mapping is not None:
            df = self._check_columns_names_and_convert_types(df, self._columns_types_mapping)

        features = []   # type: List[Any]
        try:
            features = self._apply_transforms(df)
        except AutoMLException:
            raise
        except MemoryError as e:
            raise ResourceException._with_error(
                AzureMLError.create(
                    InsufficientMemory,
                    target='ApplyTransforms',
                    reference_code=ReferenceCodes._DATA_TRANSFORMER_TRANSFORM_MEMORYERROR,
                ), inner_exception=e) from e
        except Exception as ex:
            raise TransformException.from_exception(
                ex,
                msg=self.TRANSFORM_FAILURE_MSG,
                target='DataTransformer.transform',
                reference_code=ReferenceCodes._DATA_TRANSFORMER_TRANSFROM_LEARNED,
                has_pii=False)

        if self._engineered_feature_names_class is not None:
            if not self._engineered_feature_names_class.are_engineered_feature_names_available():
                # Generate engineered feature names if they are not already generated
                if self._is_onnx_compatible and self.mapper is not None:
                    self._engineered_feature_names_class.parse_raw_feature_names(self.mapper.transformed_names_)
                else:
                    names = []  # type: List[str]
                    for transformer_mapper in self.transformer_and_mapper_list:
                        names.extend(transformer_mapper.mapper.transformed_names_)
                    self._engineered_feature_names_class.parse_raw_feature_names(
                        names)

        is_there_a_sparse_column = any(sparse.issparse(fea) for fea in features)
        combiner = FeaturizedDataCombiners.get(is_there_a_sparse_column,
                                               self._is_inference_time,
                                               memory_utilities._is_low_memory())

        ret = combiner(features,
                       **{'working_directory': self.working_directory,
                          'logger': logger,
                          'pickler': DefaultPickler()})  # type: Union[pd.DataFrame, np.ndarray, sparse.spmatrix]
        return ret

    def _update_customized_feature_types(self) -> None:
        if self._featurization_config is None:
            return

        self._logger_wrapper("info", "Start updating column purposes using customized feature type settings.")
        if self.stats_and_column_purposes is not None:
            featurization_utilities.update_customized_feature_types(
                self.stats_and_column_purposes,
                self._featurization_config
            )
        self._logger_wrapper("info", "End updating column purposes using customized feature type settings.")

    def _get_is_text_dnn(self) -> bool:
        return self._is_text_dnn

    def _set_is_text_dnn_if_available(self, transformer_mapper: TransformerAndMapper) -> bool:
        # determine if a transform is a text dnn or not
        is_text_dnn = False
        try:
            cname = transformer_mapper.transformers.steps[-1][-1].steps[-1][-1].__class__.__name__  # type: ignore
            is_text_dnn = cname in TextNeuralNetworks.ALL_CLASS_NAMES
            if is_text_dnn:
                self._is_text_dnn = True
        except Exception:
            pass
        return self._is_text_dnn

    def _get_is_BERT(self, transformer_mapper: TransformerAndMapper) -> bool:
        # determine if a transform is a BERT text dnn or not
        is_text_dnn = False
        try:
            text_dnn = transformer_mapper.transformers.steps[-1][-1].steps[-1][-1]  # type: ignore
            is_text_dnn = text_dnn.__class__.__name__ is TextNeuralNetworks.BERT_CLASS_NAME
        except Exception:
            pass
        return is_text_dnn

    def _apply_transforms(self, df: pd.DataFrame) -> List[Union[np.ndarray, pd.DataFrame, sparse.spmatrix]]:
        features = []
        if (self._is_onnx_compatible and not self.mapper) or \
                (not self._is_onnx_compatible and not self.transformer_and_mapper_list):
            raise TransformException("fit not called", has_pii=False,
                                     reference_code=ReferenceCodes._DATA_TRANSFORMER_TRANSFROM_NOT_CALL_FIT)

        if self._is_onnx_compatible:
            assert self.mapper is not None
            transformed_data = self.mapper.transform(df)
            features.append(transformed_data)
        else:
            total_ram = memory_utilities.get_all_ram()
            self._logger_wrapper("info", "Starting to apply transforms. Total ram: {} bytes".format(total_ram))
            for transformer_mapper in self.transformer_and_mapper_list:
                current_available_physical_memory = memory_utilities.get_available_physical_memory()
                transform_memory_footprint = transformer_mapper.memory_footprint_estimate
                self._logger_wrapper("info", "Transform memory estimate: {} bytes, Current available memory: {} bytes"
                                     .format(transform_memory_footprint, current_available_physical_memory))
                apply_transform = (transform_memory_footprint < current_available_physical_memory)

                transformer_list = featurization_utilities.get_transform_names(transformer_mapper.transformers)
                transformer_names = ",".join(transformer_list)
                if apply_transform:
                    self._logger_wrapper(
                        "info", "{}: Applying transform.".format(transformer_names))
                    try:
                        transform_output = transformer_mapper.mapper.transform(df)
                        features.append(transform_output)
                    except Exception as ex:
                        self._check_transformer_param_error(
                            ex, False, transformer_mapper=transformer_mapper
                        )
                        raise
                    self._logger_wrapper("info",
                                         "{transformers}: Finished applying transform. Shape {shape}".format(
                                             shape=transform_output.shape,
                                             transformers=transformer_names))
                else:
                    self._logger_wrapper("info", "{}: Transform not applied due to memory constraints.".format(
                        transformer_names))
            self._logger_wrapper("info", "Finished applying transforms")

        return features

    def set_cached_featurizers(self, featurizer_index_mapping: Mapping[int, Any]) -> None:
        """
        Overwrite featurizers in mapper.features or transformer_and_mapper_list that have
        already been fitted.

        :param featurizer_index_mapping: A mapping of indices to fitted featurizers that were pulled from the cache.
        :return: None.
        """
        if self._is_onnx_compatible and self.mapper is not None:
            for index in featurizer_index_mapping:
                self.mapper.features[index] = featurizer_index_mapping[index]
        else:
            for index in featurizer_index_mapping:
                self.transformer_and_mapper_list[index] = featurizer_index_mapping[index]

    def get_engineered_feature_names(self) -> List[str]:
        """
        Get the engineered feature names.

        Return the list of engineered feature names as string after data transformations on the
        raw data have been finished.

        :return: The list of engineered fearure names as strings
        """
        if self._engineered_feature_names_class is None:
            self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()
        return self._engineered_feature_names_class._engineered_feature_names

    def _get_json_str_for_engineered_feature_name(self,
                                                  engineered_feature_name: str) -> Optional[str]:
        """
        Return JSON string for engineered feature name.

        :param engineered_feature_name: Engineered feature name for
                                        whom JSON string is required
        :return: JSON string for engineered feature name
        """
        if self._engineered_feature_names_class is None:
            self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()
        engineered_feature_name_json_obj = self._engineered_feature_names_class \
            .get_json_object_for_engineered_feature_name(engineered_feature_name)

        # If the JSON object is not valid, then return None
        if engineered_feature_name_json_obj is None:
            self._logger_wrapper(
                'info', "Engineered feature name json object is None.")
            return None

        # Convert JSON into string and return
        return json.dumps(engineered_feature_name_json_obj)

    def get_stats_feature_type_summary(
            self,
            raw_column_name_list: Optional[List[str]] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Return column stats and feature type summary.
        :param raw_column_name_list: List of raw column names.
        :return: List of stats and feature type summary for each input raw column.
        """

        if self.stats_and_column_purposes is None:
            return None
        else:
            filtered_stats_and_column_purposes = self.stats_and_column_purposes
            if raw_column_name_list is not None:
                filtered_stats_and_column_purposes = [x for x in self.stats_and_column_purposes if
                                                      x[2] in raw_column_name_list]
            return list(map(
                lambda x: dict(
                    (
                        ("statistic", x[0].__str__()),
                        ("feature type", x[1]),
                        ("column name", x[2])
                    )
                ),
                filtered_stats_and_column_purposes))

    def get_featurization_summary(self, is_user_friendly: bool = True) -> FeaturizationSummaryType:
        """
        Return the featurization summary for all the input features seen by DataTransformer.
        :param is_user_friendly: If True, return user friendly summary, otherwise, return detailed
        featurization summary.
        :return: List of featurization summary for each input feature.
        """
        if self._engineered_feature_names_class is None:
            self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()
        return self._engineered_feature_names_class.get_raw_features_featurization_summary(is_user_friendly)

    @property
    def get_column_names_and_types(self) -> Optional[Dict[str, np.dtype]]:
        """
        Return the column name and the dtype mapping for each input raw column.
        """
        return self._columns_types_mapping

    def _get_transforms(self, df: pd.DataFrame,
                        stats_and_column_purposes: List[StatsAndColumnPurposeType],
                        y: DataSingleColumnInputType = None) -> List[TransformerType]:
        """
        Identify the transformations for all the columns in the dataframe.

        :param df: Dataframe representing text, numerical or categorical input.
        :param stats_and_column_purposes: Statistics and column purposes of the given data.
        :param y: To match fit signature.
        :return: Transformations that go into datamapper.
        """
        transforms = []  # type: List[TransformerType]
        all_columns = df.columns
        dtypes = df.dtypes

        column_groups = {}  # type: Dict[str, List[str]]
        for _, column_purpose, column in stats_and_column_purposes:
            column_groups.setdefault(column_purpose, []).append(column)

        self._raw_feature_names, all_new_column_names = data_transformer_utils.generate_new_column_names(all_columns)

        self._logger_wrapper('info', "Start getting transformers.")
        self._observer.report_status(
            ExperimentStatus.FeaturesGeneration, "Generating features for the dataset.")

        # Get default transformers based on column purpose
        for column_purpose in column_groups.keys():
            current_column_transforms = self._get_transforms_per_column_purpose(column_groups[column_purpose],
                                                                                all_columns,
                                                                                dtypes,
                                                                                all_new_column_names,
                                                                                column_purpose,
                                                                                stats_and_column_purposes)

            if current_column_transforms:
                transforms.extend(current_column_transforms)
            else:
                # skip if hashes or ignore case
                self._logger_wrapper(
                    'info', "No transforms available. Either hashes, single value column, or transformer is blocked.")

        # Experiment with different transform pipelines through feature sweeping

        sweeping_added_transformers = []  # type: List[TransformerType]
        with logging_utilities.log_activity(logger=logger, activity_name="FeatureSweeping"):
            sweeping_added_transformers = self._perform_feature_sweeping(df, y,
                                                                         stats_and_column_purposes,
                                                                         all_new_column_names)
            transforms.extend(sweeping_added_transformers)

        # TODO: Do not allow column purpose sweep if type if set in featurizer config
        transforms.extend(self._sweep_column_purpose(transforms, all_columns, dtypes,
                                                     stats_and_column_purposes, all_new_column_names, column_groups))

        if not transforms:
            # can happen when we get all hashes
            self._logger_wrapper(
                'warning', "No features could be identified or generated. Please inspect your data.")

            column_drop_reasons = self._get_column_purposes_user_friendly(stats_and_column_purposes)
            raise DataException._with_error(AzureMLError.create(
                UnrecognizedFeatures, target="X", column_drop_reasons="\n".join(column_drop_reasons),
                reference_code=ReferenceCodes._DATA_TRANSFORMER_TRANSFROM_NO_FEATURE)
            )

        # Log the transformations done for raw data into the logs
        self._logger_wrapper(
            'info', self._get_transformations_str(all_columns, transforms))

        # Log stats_computation about raw data
        self._logger_wrapper('info',
                             self._pre_processing_stats.get_raw_data_stats())

        self._logger_wrapper('info', "End getting transformers.")

        # Used for testing only
        if self._test_transforms is not None:
            transforms.extend(self._test_transforms)

        return transforms

    def _get_column_purposes_user_friendly(
            self, stats_and_column_purposes: List[StatsAndColumnPurposeType]
    ) -> List[str]:
        column_drop_reason_list = []  # type: List[str]
        for _, column_purpose, column_name in stats_and_column_purposes:
            column_drop_reason_list.append(
                "Column {} identified as {}.".format(column_name, column_purpose)
            )
        return column_drop_reason_list

    def _perform_feature_sweeping(self, df: pd.DataFrame, y: DataSingleColumnInputType,
                                  stats_and_column_purposes: List[StatsAndColumnPurposeType],
                                  all_new_column_names: List[str],
                                  feature_sweeper: Any = None) -> \
            List[TransformerType]:
        """
        Perform feature sweeping and return transforms.

        :param df: Input data frame.
        :param y: Input labels.
        :param stats_and_column_purposes: Stats and column purposes.
        :return: Transformers identified by the sweeping logic.
        """
        transforms = []  # type: List[TransformerType]

        try:
            if self._enable_feature_sweeping:
                self._logger_wrapper("info", "Performing feature sweeping")
                from azureml.automl.runtime.sweeping.meta_sweeper import MetaSweeper

                if feature_sweeper is None:
                    feature_sweeper = MetaSweeper(task=self._task_type,
                                                  timeout_sec=self._feature_sweeping_timeout,
                                                  is_cross_validation=self._is_cross_validation,
                                                  featurization_config=self._featurization_config,
                                                  enable_dnn=self._enable_dnn,
                                                  force_text_dnn=self._force_text_dnn,
                                                  feature_sweeping_config=self._feature_sweeping_config)

                sweeped_transforms = feature_sweeper.sweep(
                    self.working_directory,
                    df, y, stats_and_column_purposes)  # type: List[Tuple[str, Pipeline]]

                if sweeped_transforms is not None and len(sweeped_transforms) > 0:
                    added_transformers = ','.join(map(self.get_added_transformer_from_sweeped_transform,
                                                      sweeped_transforms))
                    self._logger_wrapper('info',
                                         'Sweeping added the following transforms: {}'.format(added_transformers))

                    cols_list = []  # type: List[str]
                    for cols, tfs in sweeped_transforms:
                        if not isinstance(cols, list):
                            stats_and_column_purpose = next((x for x in stats_and_column_purposes if x[2] == cols))
                            column_purpose = stats_and_column_purpose[1]
                            index = stats_and_column_purposes.index(stats_and_column_purpose)
                            new_column_name = all_new_column_names[index]
                            cols_list = [str(new_column_name)]
                        else:
                            for col in cols:
                                stats_and_column_purpose = next((x for x in stats_and_column_purposes if x[2] == col))
                                # Assumption here is that all the columns in the list will be of one type
                                column_purpose = stats_and_column_purpose[1]
                                index = stats_and_column_purposes.index(stats_and_column_purpose)
                                new_column_name = all_new_column_names[index]
                                cols_list.append(new_column_name)

                        if self._engineered_feature_names_class is None:
                            self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()
                        column_name_alias = self._engineered_feature_names_class. \
                            get_alias_name_from_pipeline_object(cols_list, tfs, column_purpose)

                        transforms.append((cols,
                                           make_pipeline(tfs),
                                           {"alias": str(column_name_alias)}))
                else:
                    self._logger_wrapper('info', 'Sweeping did not add any transformers.')

            else:
                self._logger_wrapper("info", "Feature sweeping disabled.")
        except Exception:
            self._logger_wrapper("debug", "Sweeping failed with an error.")
        finally:
            return transforms

    def _sweep_column_purpose(self, transforms: List[TransformerType],
                              columns: Index, dtypes: Series,
                              stats_and_column_purposes: List[StatsAndColumnPurposeType],
                              new_column_names: List[str],
                              column_groups: Dict[str, List[str]]) -> List[TransformerType]:
        """
        Perform column purpose sweeping and return appropriate transforms.

        :param transforms: Current set of transforms.
        :param columns: Current set of columns in the data frame.
        :param dtypes: Current pandas dtypes.
        :param stats_and_column_purposes: Stats and column purposes of various columns.
        :param new_column_names: New columns names for Engineered feature name generation.
        :param column_groups: Dictionary representing list of columns belonging to column purpose
        :return: Alternate transformer identified by the column sweep.
        """

        if not transforms and len(columns) == 1:
            column_index = 0
            if not np.issubdtype(dtypes[column_index], np.number):
                raw_stats, feature_type, column = stats_and_column_purposes[column_index]
                alternate_column_purpose = ColumnPurposeSweeper.safe_convert_on_feature_type(feature_type)
                if alternate_column_purpose:
                    return self._get_alternate_transformer(column_index, columns, dtypes,
                                                           new_column_names, alternate_column_purpose,
                                                           stats_and_column_purposes)

        columns_with_transformers = [x[0] for x in transforms if not isinstance(x[0], list)]
        columns_with_transformers_set = set(columns_with_transformers)
        for feature_type in column_groups.keys():
            if feature_type == _FeatureType.Numeric:
                continue
            for column in column_groups[feature_type]:
                # Check if any transforms are available for this column.
                # If not, see if column type sweeping can be made.
                if column not in columns_with_transformers_set:
                    stats_and_column_purpose = next(
                        (x for x in stats_and_column_purposes if x[2] == column))
                    column_index = stats_and_column_purposes.index(stats_and_column_purpose)
                    raw_stats, _, _ = stats_and_column_purposes[column_index]
                    alternate_column_purpose = ColumnPurposeSweeper.safe_convert_on_data_type(feature_type,
                                                                                              raw_stats.column_type)
                    if alternate_column_purpose:
                        return self._get_alternate_transformer(column_index, columns, dtypes,
                                                               new_column_names,
                                                               alternate_column_purpose,
                                                               stats_and_column_purposes)

        return []

    def _get_alternate_transformer(
            self,
            column_index: int,
            columns: Index,
            dtypes: Series,
            new_column_names: List[str],
            alternate_feature_type: str,
            stats_and_column_purposes: List[StatsAndColumnPurposeType]) -> List[TransformerType]:
        """
        Return alternate transformer for given alternate column purpose

        :param column_index: Index of a referred column.
        :param columns: Columns to get transforms for.
        :param dtypes: Current pandas dtypes.
        :param new_column_names: New columns names for Engineered feature name generation.
        :param alternate_feature_types: Alternative feature type detected.
        :param stats_and_column_purposes: Stats and column purposes of various columns.
        :return: Alternate transformer identified by the new feature type.
        """
        raw_stats, original_feature_type, column = stats_and_column_purposes[column_index]

        self._logger_wrapper(
            "info",
            "Column index: {column_index}, current column purpose: {detected_column_purpose}, "
            "Alternate column purpose: {alternate_column_purpose}".format(
                detected_column_purpose=original_feature_type,
                column_index=column_index,
                alternate_column_purpose=alternate_feature_type))
        stats_and_column_purposes[column_index] = raw_stats, alternate_feature_type, column
        return self._get_transforms_per_column_purpose([columns[column_index]],
                                                       columns, dtypes,
                                                       new_column_names,
                                                       alternate_feature_type,
                                                       stats_and_column_purposes)

    def _get_transforms_per_column_purpose(
            self,
            columnspurpose: List[str],
            columns: Index, dtypes: Series,
            new_column_names: List[str],
            detected_column_purpose: str,
            stats_and_column_purposes: List[StatsAndColumnPurposeType]) -> List[TransformerType]:
        """Obtain transformations based on column purpose and feature stats.

        :param: columnspurpose: Columns to get transforms for.
        :param columns: Column names for columns.
        :param dtypes: Current pandas dtypes.
        :param new_column_names: Column names for engineered features.
        :param detected_column_purpose: Column purpose detected.
        :param stats_and_column_purposes: Statistics and column purposes of the given data.

        :return: List of transformations to be done on this column.
        """
        trs = []  # type: List[TransformerType]
        for column in columnspurpose:
            stats_and_column_purpose = next(
                (x for x in stats_and_column_purposes if x[2] == column))
            index = stats_and_column_purposes.index(stats_and_column_purpose)
            raw_stats, _, _ = stats_and_column_purposes[index]
            new_column_name = new_column_names[index]
            if detected_column_purpose == _FeatureType.Numeric:
                tr = self._get_numeric_transforms(column, new_column_name)
                # if there are lot of imputed values, add an imputation marker
                if raw_stats.num_na > 0.01 * raw_stats.total_number_vals:
                    tr.extend(self._get_imputation_marker_transforms(column, new_column_name))
            elif detected_column_purpose == _FeatureType.DateTime:
                tr = self._get_datetime_transforms(column, new_column_name)
            elif detected_column_purpose == _FeatureType.CategoricalHash:
                tr = self._get_categorical_hash_transforms(column, new_column_name, raw_stats.num_unique_vals)
            elif detected_column_purpose == _FeatureType.Categorical:
                tr = self._get_categorical_transforms(column, new_column_name, raw_stats.num_unique_vals)
            elif detected_column_purpose == _FeatureType.Text:
                self._text_transformer = self._text_transformer or TextTransformer(
                    self._task_type, logger, self._is_onnx_compatible,
                    featurization_config=self._featurization_config)
                if self._engineered_feature_names_class is None:
                    self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()
                tr = self._text_transformer.get_transforms(column, new_column_name,
                                                           get_ngram_len(raw_stats.lengths),
                                                           self._engineered_feature_names_class,
                                                           self._featurization_config.blocked_transformers
                                                           if self._featurization_config is not None else None)
            elif detected_column_purpose in _FeatureType.DROP_SET:
                tr = self._get_drop_column_transform(column, new_column_name, detected_column_purpose)

            if tr is not None:
                trs.extend(tr)

            column_loc = columns.get_loc(column)

            utilities._log_raw_data_stat(
                raw_stats,
                prefix_message="[XColNum:{}]".format(
                    column_loc
                )
            )

            self._logger_wrapper(
                'info',
                "Preprocess transformer for col {}, datatype: {}, detected "
                "datatype {}".format(
                    column_loc,
                    str(dtypes.values[index]),
                    str(detected_column_purpose)
                )
            )
            # Update pre-processing stats_computation
            self._pre_processing_stats.update_raw_feature_stats(
                detected_column_purpose)

        return trs

    def _get_drop_column_transform(
            self,
            column: str,
            column_name: str,
            column_purpose: str) -> List[TransformerType]:

        tr = []  # type:  List[TransformerType]

        # Add the transformations to be done and get the alias name
        # for the drop transform.
        drop_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_SupportedTransformersInternal.Drop,
            operator=None,
            feature_type=column_purpose,
            should_output=True)
        # Create an object to convert transformations into JSON object
        feature_transformers = \
            _FeatureTransformers([drop_transformer])

        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()
        # Persist the JSON object for later use
        if self._engineered_feature_names_class is None:
            self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()
        self._engineered_feature_names_class.get_raw_feature_alias_name(json_obj)

        return tr

    def _get_categorical_hash_transforms(
            self,
            column: str,
            column_name: str,
            num_unique_categories: int) -> List[TransformerType]:
        """
        Create a list of transforms for categorical hash data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :param num_unique_categories: Number of unique categories
        :return: Categorical hash transformations to use in a list.
        """
        # Add the transformations to be done and get the alias name
        # for the hashing one hot encode transform.
        tr = []  # type:  List[TransformerType]

        transformer_fncs = [_SupportedTransformersInternal.StringCast,
                            _SupportedTransformersInternal.HashOneHotEncoder]

        # Check whether the transformer functions are in blocked list
        if self._featurization_config is not None:
            transformers_in_blocked_list = featurization_utilities\
                .transformers_in_blocked_list(transformer_fncs, self._featurization_config.blocked_transformers)
            if transformers_in_blocked_list:
                self._logger_wrapper(
                    'info', "Excluding blocked transformer(s): {0}".format(transformers_in_blocked_list))
                return tr

        string_cast = TextFeaturizers.string_cast(logger=logger)

        transformer_params = featurization_utilities.get_transformer_params_by_column_names(
            _SupportedTransformersInternal.HashOneHotEncoder, [column], self._featurization_config)

        try:
            # TODO: update HashOneHotVectorizerTransformer to accept number_of_bits instead of num_cols
            if transformer_params.get("number_of_bits"):
                number_of_bits = transformer_params.pop("number_of_bits")
            else:
                number_of_bits = int(math.log(num_unique_categories, 2))
            num_cols = pow(2, number_of_bits)
            hashonehot_vectorizer = CategoricalFeaturizers.hashonehot_vectorizer(
                **{
                    'hashing_seed_val': constants.hashing_seed_value,
                    'num_cols': int(num_cols),
                    'logger': logger
                }
            )
            if len(transformer_params) > 0:
                self._logger_wrapper("warning", "Ignoring unsupported parameters")
        except Exception as e:
            logging_utilities.log_traceback(e, self.logger, is_critical=False)
            self._logger_wrapper(
                "warning",
                self.UNSUPPORTED_PARAMETER_WARNING_MSG.format(t=_SupportedTransformersInternal.HashOneHotEncoder)
            )
            hashonehot_vectorizer = CategoricalFeaturizers.hashonehot_vectorizer(
                **{
                    'hashing_seed_val': constants.hashing_seed_value,
                    'num_cols': int(pow(2, int(math.log(num_unique_categories, 2)))),
                    'logger': logger
                }
            )

        categorical_hash_string_cast_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=transformer_fncs[0],
            operator=None,
            feature_type=_FeatureType.CategoricalHash,
            should_output=False)
        # This transformation depends on the previous transformation
        categorical_hash_onehot_encode_transformer = _Transformer(
            parent_feature_list=[1],
            transformation_fnc=transformer_fncs[1],
            operator=None,
            feature_type=None,
            should_output=True,
            transformer_params=_TransformerParamsHelper.to_dict(hashonehot_vectorizer))
        # Create an object to convert transformations into JSON object
        feature_transformers = \
            _FeatureTransformers(
                [categorical_hash_string_cast_transformer,
                 categorical_hash_onehot_encode_transformer])

        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()

        if self._engineered_feature_names_class is None:
            self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()
        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = self._engineered_feature_names_class.get_raw_feature_alias_name(
            json_obj)

        # Add the transformations to be done and get the alias name
        # for the raw column.

        tr = [(column, [string_cast, hashonehot_vectorizer], {'alias': str(alias_column_name)})]
        return tr

    def _get_datetime_transforms(
            self,
            column: str,
            column_name: str) -> List[TransformerType]:
        """
        Create a list of transforms for date time data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :return: Date time transformations to use in a list.
        """
        cat_imputer = CategoricalFeaturizers.cat_imputer(
            **{
                'logger': logger,
                **featurization_utilities.get_transformer_params_by_column_names(
                    _SupportedTransformersInternal.CatImputer, [column], self._featurization_config)
            })
        string_cast = TextFeaturizers.string_cast(logger=logger)
        datetime_transformer = DateTimeFeaturesTransformer(logger=logger)
        # Add the transformations to be done and get the alias name
        # for the date time transform.
        datatime_imputer_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_SupportedTransformersInternal.CatImputer,
            operator=_OperatorNames.Mode,
            feature_type=_FeatureType.DateTime,
            should_output=True,
            transformer_params=_TransformerParamsHelper.to_dict(cat_imputer))
        # This transformation depends on the previous transformation
        datatime_string_cast_transformer = _Transformer(
            parent_feature_list=[1],
            transformation_fnc=_SupportedTransformersInternal.StringCast,
            operator=None,
            feature_type=None,
            should_output=False)
        # This transformation depends on the previous transformation
        datatime_datetime_transformer = _Transformer(
            parent_feature_list=[2],
            transformation_fnc=_SupportedTransformersInternal.DateTimeTransformer,
            operator=None,
            feature_type=None,
            should_output=False)
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers(
            [datatime_imputer_transformer,
             datatime_string_cast_transformer,
             datatime_datetime_transformer])
        # Create the JSON object
        json_obj = \
            feature_transformers.encode_transformations_from_list()

        if self._engineered_feature_names_class is None:
            self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()
        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = \
            self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)

        # Add the transformations to be done and get the alias name
        # for the raw column.
        tr = []  # type:  List[TransformerType]
        tr = [(column, [cat_imputer, string_cast, datetime_transformer], {'alias': str(alias_column_name)})]
        return tr

    def _get_categorical_transforms(
            self,
            column: str,
            column_name: str,
            num_unique_categories: int) -> List[TransformerType]:
        """
        Create a list of transforms for categorical data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :param num_unique_categories: Number of unique categories
        :return: Categorical transformations to use in a list.
        """
        tr = []  # type:  List[TransformerType]

        if num_unique_categories <= 2:

            transformer_fncs = [_SupportedTransformersInternal.CatImputer,
                                _SupportedTransformersInternal.StringCast,
                                _SupportedTransformersInternal.LabelEncoder]

            # Check whether the transformer functions are in blocked list
            if self._featurization_config is not None:
                transformers_in_blocked_list = featurization_utilities \
                    .transformers_in_blocked_list(transformer_fncs, self._featurization_config.blocked_transformers)
                if transformers_in_blocked_list:
                    self._logger_wrapper(
                        'info', "Excluding blocked transformer(s): {0}".format(transformers_in_blocked_list))
                    return tr

            # Add the transformations to be done and get the alias name
            # for the hashing label encode transform.
            cat_two_category_imputer = CategoricalFeaturizers.cat_imputer(
                **{
                    'logger': logger,
                    **featurization_utilities.get_transformer_params_by_column_names(
                        _SupportedTransformersInternal.CatImputer, [column], self._featurization_config)
                })
            cat_two_category_string_cast = TextFeaturizers.string_cast(logger=logger)
            cat_two_category_labelencoder = CategoricalFeaturizers.labelencoder(
                **{
                    'hashing_seed_val': constants.hashing_seed_value,
                    'logger': logger,
                    **featurization_utilities.get_transformer_params_by_column_names(
                        _SupportedTransformersInternal.LabelEncoder, [column], self._featurization_config)
                })
            cat_two_category_imputer_transformer = _Transformer(
                parent_feature_list=[str(column_name)],
                transformation_fnc=transformer_fncs[0],
                operator=_OperatorNames.Mode,
                feature_type=_FeatureType.Categorical,
                should_output=True,
                transformer_params=_TransformerParamsHelper.to_dict(cat_two_category_imputer))
            # This transformation depends on the previous transformation
            cat_two_category_string_cast_transformer = _Transformer(
                parent_feature_list=[1],
                transformation_fnc=transformer_fncs[1],
                operator=None,
                feature_type=None,
                should_output=False)
            # This transformation depends on the previous transformation
            cat_two_category_label_encode_transformer = _Transformer(
                parent_feature_list=[2],
                transformation_fnc=transformer_fncs[2],
                operator=None,
                feature_type=None,
                should_output=True,
                transformer_params=_TransformerParamsHelper.to_dict(cat_two_category_labelencoder))
            # Create an object to convert transformations into JSON object
            feature_transformers = _FeatureTransformers(
                [cat_two_category_imputer_transformer,
                 cat_two_category_string_cast_transformer,
                 cat_two_category_label_encode_transformer])
            # Create the JSON object
            json_obj = \
                feature_transformers.encode_transformations_from_list()

            if self._engineered_feature_names_class is None:
                self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()
            # Persist the JSON object for later use and obtain an alias name
            alias_column_name = self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)

            # Add the transformations to be done and get the alias name
            # for the raw column.
            tr = [(column, [cat_two_category_imputer, cat_two_category_string_cast,
                            cat_two_category_labelencoder], {'alias': str(alias_column_name)})]
            return tr
        else:

            transformer_fncs = [_SupportedTransformersInternal.StringCast,
                                _SupportedTransformersInternal.CountVectorizer]

            # Check whether the transformer functions are in blocked list
            if self._featurization_config is not None:
                transformers_in_blocked_list = featurization_utilities \
                    .transformers_in_blocked_list(transformer_fncs, self._featurization_config.blocked_transformers)
                if transformers_in_blocked_list:
                    self._logger_wrapper(
                        'info', "Excluding blocked transformer(s): {0}".format(transformers_in_blocked_list))
                    return tr

            # Add the transformations to be done and get the alias name
            # for the hashing one hot encode transform.
            cat_multiple_category_string_cast = TextFeaturizers.string_cast(logger=logger)
            count_vect_lowercase = not self._is_onnx_compatible
            cat_multiple_category_count_vectorizer = \
                TextFeaturizers.count_vectorizer(
                    **{
                        'tokenizer': self._wrap_in_lst,
                        'binary': True,
                        'lowercase': count_vect_lowercase,
                        **featurization_utilities.get_transformer_params_by_column_names(
                            _SupportedTransformersInternal.CountVectorizer, [column], self._featurization_config)
                    })
            cat_multiple_category_string_cast_transformer = _Transformer(
                parent_feature_list=[str(column_name)],
                transformation_fnc=transformer_fncs[0],
                operator=None,
                feature_type=_FeatureType.Categorical,
                should_output=False)
            # This transformation depends on the previous transformation
            cat_multiple_category_countvec_transformer = _Transformer(
                parent_feature_list=[1],
                transformation_fnc=transformer_fncs[1],
                operator=_OperatorNames.CharGram,
                feature_type=None,
                should_output=True,
                transformer_params=_TransformerParamsHelper.to_dict(cat_multiple_category_count_vectorizer))
            # Create an object to convert transformations into JSON object
            feature_transformers = _FeatureTransformers([
                cat_multiple_category_string_cast_transformer,
                cat_multiple_category_countvec_transformer])
            # Create the JSON object
            json_obj = feature_transformers.encode_transformations_from_list()

            if self._engineered_feature_names_class is None:
                self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()
            # Persist the JSON object for later use and obtain an alias name
            alias_column_name = self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)

            # use CountVectorizer for both Hash and CategoricalHash for now
            tr = [(column, [cat_multiple_category_string_cast, cat_multiple_category_count_vectorizer],
                   {'alias': str(alias_column_name)})]
            return tr

    def _get_numeric_transforms(
            self,
            column: str,
            column_name: str) -> List[TransformerType]:
        """
        Create a list of transforms for numerical data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :return: Numerical transformations to use in a list.
        """
        # Add the transformations to be done and get the alias name
        # for the numerical transform
        transformer_params = featurization_utilities.get_transformer_params_by_column_names(
            _SupportedTransformersInternal.Imputer, [column], self._featurization_config)
        operator = _TransformerOperatorMappings.Imputer.get(str(transformer_params.get('strategy')))
        if not operator:
            if transformer_params.get('strategy'):
                self._logger_wrapper("warning", "Given strategy is not supported, proceeding with default value")
            operator = _OperatorNames.Mean
            transformer_params['strategy'] = operator.lower()
        try:
            imputer = GenericFeaturizers.imputer(**transformer_params)
        except Exception as e:
            logging_utilities.log_traceback(e, self.logger, is_critical=False)
            self._logger_wrapper(
                "warning",
                self.UNSUPPORTED_PARAMETER_WARNING_MSG.format(t=_SupportedTransformersInternal.Imputer)
            )
            imputer = GenericFeaturizers.imputer()
        numeric_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_SupportedTransformersInternal.Imputer,
            operator=operator,
            feature_type=_FeatureType.Numeric,
            should_output=True,
            transformer_params=_TransformerParamsHelper.to_dict(imputer))
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers([numeric_transformer])
        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()

        if self._engineered_feature_names_class is None:
            self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()
        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = \
            self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)

        # Add the transformations to be done and get the alias name
        # for the imputation marker transform.
        # floats or ints go as they are, we only fix NaN
        tr = [([column], [imputer], {'alias': str(alias_column_name)})]
        return cast(List[TransformerType], tr)

    def _get_imputation_marker_transforms(self, column, column_name):
        """
        Create a list of transforms for numerical data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :return: Numerical transformations to use in a list.
        """
        # Add the transformations to be done and get the alias name
        # for the imputation marker transform.
        imputation_marker = GenericFeaturizers.imputation_marker(logger=logger)
        imputation_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_SupportedTransformersInternal.ImputationMarker,
            operator=None,
            feature_type=_FeatureType.Numeric,
            should_output=True)
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers([imputation_transformer])
        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()

        if self._engineered_feature_names_class is None:
            self._engineered_feature_names_class = _GenerateEngineeredFeatureNames()
        # Persist the JSON object for later use and obtain an alias name
        alias_column_name = \
            self._engineered_feature_names_class.get_raw_feature_alias_name(
                json_obj)

        # Add the transformations to be done and get the alias name
        # for the imputation marker transform.
        tr = [([column], [imputation_marker], {'alias': str(alias_column_name)})]

        return tr

    def _wrap_in_lst(self, x):
        """
        Wrap an element in list.

        :param x: Element like string or integer.
        """
        return [x]

    def _check_columns_names_and_convert_types(self,
                                               df: pd.DataFrame,
                                               columns_types_mapping: Dict[str, np.dtype]) -> pd.DataFrame:
        """
        Check given data to see if column names and number of features line up
        with fitted data before going through data transformation

        :param df: input data to check.
        :param columns_types_mapping: column types from fitted data
        :return data to be used on transformation
        """
        curr_columns_types_mapping = data_transformer_utils.get_pandas_columns_types_mapping(df)
        if len(curr_columns_types_mapping) != len(columns_types_mapping):
            raise DataException._with_error(
                AzureMLError.create(
                    DatasetsFeatureCountMismatch,
                    target="X",
                    first_dataset_name="fitted data", first_dataset_shape=len(columns_types_mapping),
                    second_dataset_name="input data", second_dataset_shape=len(curr_columns_types_mapping),
                    reference_code=ReferenceCodes._DATA_TRANSFORMER_TRANSFROM_WRONG_COLUMN
                )
            )

        type_converted_columns = {}  # type: Dict[str, np.dtype]
        for col, col_type in curr_columns_types_mapping.items():
            if col not in columns_types_mapping:
                raise DataException._with_error(
                    AzureMLError.create(
                        MissingColumnsInData,
                        target="X",
                        columns=col,
                        data_object_name='fitted data',
                        reference_code=ReferenceCodes._DATA_TRANSFORMER_TRANSFROM_COLUMN_NOT_FOUND
                    )
                )

            if col_type != columns_types_mapping[col]:
                type_converted_columns[col] = columns_types_mapping[col]

        if len(type_converted_columns) > 0:
            for col, col_type in type_converted_columns.items():
                try:
                    df[col] = df[col].astype(col_type)
                except Exception:
                    input_dtype = runtime_utilities._get_column_data_type_as_str(df[col])
                    raise DataException._with_error(
                        AzureMLError.create(
                            InconsistentColumnTypeInTrainValid,
                            target="X",
                            reference_code=ReferenceCodes._DATA_TRANSFORMER_TRANSFROM_WRONG_COLUMN_TYPE,
                            column_name=col,
                            train_dtype=col_type,
                            validation_dtype=input_dtype
                        )
                    )
        return df

    def _get_transformations_str(
            self,
            columns: Index,
            transforms: List[TransformerType]) -> str:
        """
        Get the data transformations recorded for raw columns as strings.

        :param df: Input dataframe.
        :type df:numpy.ndarray or pandas.DataFrame or sparse matrix
        :param transforms: List of applied transformations for various raw
        columns as a string.
        :type transforms: List
        """
        transformation_str = 'Transforms:\n'
        list_of_transforms_as_list = []

        num_transforms = len(transforms)
        # Walk all columns in the input dataframe
        for column in columns:
            # Get all the indexes of transformations for the current column
            column_matches_transforms = [i for i in range(
                num_transforms) if transforms[i][0] == column]

            # If no matches for column name is found, then look for list having
            # this column name
            if len(column_matches_transforms) == 0:
                column_matches_transforms = [i for i in range(
                    num_transforms) if transforms[i][0] == [column]]

            # look for list of columns having this column name
            column_matches_transforms = \
                [i for i in range(0, len(transforms))
                 if isinstance(transforms[i][0], list) and column in transforms[i][0]]

            # Walk all the transformations found for the current column and add
            # to a string
            for transform_index in column_matches_transforms:

                transformers_list = transforms[transform_index][1]
                if isinstance(transformers_list, Pipeline):
                    transformers_list = [t[1] for t in transformers_list.steps]

                some_str = 'col {}, transformers: {}'.format(
                    columns.get_loc(column), '\t'.join([tf.__class__.__name__ for tf in transformers_list]))

                list_of_transforms_as_list.append(some_str)

        transformation_str += '\n'.join(list_of_transforms_as_list)

        # Return the string representation of all the transformations
        return transformation_str

    def _check_transformer_param_error(
            self,
            ex: BaseException,
            is_fit: bool,
            transformer_mapper: TransformerAndMapper
    ) -> None:
        if featurization_utilities.is_transformer_param_overridden(self._featurization_config):
            # there was a transformer parameter override that could have led to failure
            # Ideally transformer should throw error during initialization (e.g. CountVectorizer)
            # but some transformers verify the input later in the process
            # during fit or transform (e.g. Imputer).
            columns = list(transformer_mapper.mapper._selected_columns)

            try:
                for transformer in transformer_mapper.transformers:
                    if hasattr(transformer, '_transformer_name'):
                        transformer_name = transformer._transformer_name
                    else:
                        transformer_name = transformer.__class__.__name__
                    if featurization_utilities.get_transformer_params_by_column_names(
                        transformer_name, columns, self._featurization_config
                    ):
                        stage = "fitting" if is_fit else "applying"
                        raise ConfigException._with_error(
                            AzureMLError.create(
                                FeaturizationConfigParamOverridden, target='DataTransformer', stage=stage,
                                reference_code=ReferenceCodes._DATA_TRANSFORMER_TRANSFORMER_PARAM_ERROR
                            )
                        )
            except AutoMLException:
                raise
            except Exception as e:
                # if check fails, then we raise Fit / Transform Exception instead from caller.
                logging_utilities.log_traceback(e, self.logger, is_critical=False)

    def __getstate__(self):
        """
        Get state picklable objects.

        :return: state
        """
        base_sanitized_state = super(DataTransformer, self).__getstate__()
        state = dict(base_sanitized_state)
        state['_is_inference_time'] = True
        # Remove the unpicklable entries.
        del state['_observer']
        del state['_feature_sweeping_config']
        del state['_featurizer_container']
        del state['stats_and_column_purposes']
        return state

    def __setstate__(self, state):
        """
        Set state for object reconstruction.

        :param state: pickle state
        """
        state['_observer'] = NullExperimentObserver()
        state['_feature_sweeping_config'] = {}
        working_dir = state.get('working_directory')
        if working_dir is None or not os.path.exists(working_dir):
            state['working_directory'] = os.getcwd()

        new_data_transformer = DataTransformer()
        new_data_transformer.logger = None
        for k, v in new_data_transformer.__dict__.items():
            if k not in state:
                state[k] = v
        super(DataTransformer, self).__setstate__(state)

    @classmethod
    def _pipeline_name_(cls, pipeline: Pipeline) -> str:
        """
        Method for extracting the name of the last transformer in a pipeline.

        :param pipeline: The input pipeline.
        :return: The name of the last transformer or 'Unknown' if pipeline is None.
        """
        if pipeline is not None:
            if isinstance(pipeline, Pipeline):
                return type(pipeline.steps[-1][1]).__name__
            return type(pipeline).__name__
        return "Unknown"

    @classmethod
    def get_added_transformer_from_sweeped_transform(cls, sweeped_transform: Tuple[str, Pipeline]) -> str:
        """
        Get the name of a transformer added during feature sweeping.

        :param sweeped_transform: A tuple containing the pipeline with the transformer in it generated
        by the MetaSweeper.
        :return: The name of the transformer object.
        """
        pipeline = sweeped_transform[1]
        return cls._pipeline_name_(pipeline)
