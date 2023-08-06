# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Principles of MLEngine
1) Composable set of APIs that define the various stages of a machine learning experiment
2) APIs are azure service and azureML SDK independent - (except for AzureML dataset package)
3) APIs are ML package concept independent - ie they should NOT project the concepts from ML packages directly
4) APIs are distributed infra independent - APIs hide distributed-infra used however are take "distributed/not" flag
5) APIs are AutoML concept and automl workflow independent - ie they need to work beyond AutoML context
6) APIs params are explicit - ie they explicitly accept params it expects and wont depend on external state, storage
7) APIs are friendly to AML pipelining - ie we expect these APIs to be orchestratable using AML pipelines

Terminology
1) Pipeline: Assembled set of featurizer(s) and trainer. It is a pre training concept.
2) Model: The thing that comes out of fitting/training. It is a post training concept.
        FeaturizedModel: The thing that comes out fitting a featurizers. Can transform but cant predict.
        ClassificationModel/RegressionModel/ForecastingModel: Can transform(optionally) and predict/forecast.
3) Algorithm: Captures the logic used to train - such as LightGBM or LinearRegressor


Pending APIs
1) prepare
2) detect column_purpose
3) featurizer_fit
4) featurizer_transform
5) predict
6) predict_proba
7) ensemble
8) explain
9) convert_to_onnx
10) forecast
11) evaluate_forecaster
12) evaluate_regressor

"""

from typing import Dict, Optional, Any, Union, List
import logging
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline

from azureml.automl.core._experiment_observer import ExperimentObserver
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.runtime._feature_sweeped_state_container import FeatureSweepedStateContainer
from azureml.automl.runtime.data_context import RawDataContext
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.featurization import DataTransformer
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.types import DataInputType


def validate(X: DataInputType,
             y: DataInputType,
             X_valid: Optional[DataInputType],
             y_valid: Optional[DataInputType],
             sample_weight: Optional[DataInputType],
             sample_weight_valid: Optional[DataInputType],
             cv_splits_indices: Optional[np.ndarray],
             automl_settings: AutoMLBaseSettings,
             check_sparse: bool = False,
             x_raw_column_names: Optional[np.ndarray] = None) -> None:
    """
    Checks whether data is ready for ML

    :param X:
    :param y:
    :param X_valid:
    :param y_valid:
    :param sample_weight:
    :param sample_weight_valid:
    :param cv_splits_indices:
    :param automl_settings:
    :param check_sparse:
    :param x_raw_column_names: Raw column names as list of str.
    """

    from azureml.automl.runtime import training_utilities
    training_utilities.validate_training_data(X,
                                              y,
                                              X_valid,
                                              y_valid,
                                              sample_weight,
                                              sample_weight_valid,
                                              cv_splits_indices,
                                              automl_settings,
                                              check_sparse,
                                              x_raw_column_names)


def suggest_featurizers(raw_data_context: RawDataContext,
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
                        working_dir: Optional[str] = None) -> \
        Optional[FeatureSweepedStateContainer]:
    """
    suggest featurizers

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

    import azureml.automl.runtime.data_transformation as DataTransformation
    return DataTransformation.get_transformers_for_full_featurization(raw_data_context,
                                                                      cache_store,
                                                                      is_onnx_compatible,
                                                                      logger,
                                                                      experiment_observer,
                                                                      enable_feature_sweeping,
                                                                      verifier,
                                                                      enable_streaming,
                                                                      feature_sweeping_config,
                                                                      enable_dnn,
                                                                      force_text_dnn,
                                                                      working_dir)


def featurize(x: DataInputType,
              y: DataInputType,
              data_transformer: DataTransformer
              ) -> Union[pd.DataFrame, np.ndarray, sparse.spmatrix]:
    """
    featurize the data so it could be used for final model training

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

    import azureml.automl.runtime.data_transformation as DataTransformation
    return DataTransformation._fit_transform(x, y, data_transformer)


def train(pipeline_obj: Pipeline,
          X: DataInputType,
          y: DataInputType,
          sample_weight: DataInputType = None
          ) -> Pipeline:
    """
    train the model that can do predictions

    :param pipeline_obj: The pipeline to run the fit on.
    :param X: Input data.
    :param y: Target values.
    :param sample_weight: Sample weights for training data.
    :return: fitted pipeline.
    """

    from azureml.automl.runtime.shared.runner import ClientRunner
    return ClientRunner.fit_pipeline(pipeline_obj, X, y, sample_weight)


def evaluate_classifier(
        y_test: np.ndarray,
        y_pred_probs: np.ndarray,
        metrics: List[str],
        class_labels: np.ndarray,
        train_labels: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
        y_transformer: Optional[TransformerMixin] = None,
        use_binary: bool = False,
        logger: Optional[logging.Logger] = None
) -> Dict[str, Union[float, Dict[str, Any]]]:
    """
    given the scored data, generate metrics for classification task

    All class labels for y should come
    as seen by the fitted model (i.e. if the fitted model uses a y transformer the labels
    should also come transformed).

    All metrics present in `metrics` will be present in the output dictionary with either
    the value(s) calculated or `nan` if the calculation failed.

    :param y_test: The target values (Transformed if using a y transformer)
    :param y_pred_probs: The predicted probabilities for all classes.
    :param metrics: Classification metrics to compute
    :param class_labels: All classes found in the full dataset (includes train/valid/test sets).
        These should be transformed if using a y transformer.
    :param train_labels: Classes as seen (trained on) by the trained model. These values
        should correspond to the columns of y_pred_probs in the correct order.
    :param sample_weight: Weights for the samples (Does not need
        to match sample weights on the fitted model)
    :param y_transformer: Used to inverse transform labels from `y_test`. Required for non-scalar metrics.
    :param use_binary: Compute metrics only on the true class for binary classification.
    :param logger: A logger to log errors and warnings
    :return: A dictionary mapping metric name to metric score.
    """

    from azureml.automl.runtime.shared.score import scoring
    return scoring.score_classification(y_test,
                                        y_pred_probs,
                                        metrics,
                                        class_labels,
                                        train_labels,
                                        sample_weight,
                                        y_transformer,
                                        use_binary,
                                        logger)
