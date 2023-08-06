# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The set of helper functions for data frames."""
import warnings
from typing import Dict, cast, List, Optional, Set, Tuple, Union

import numpy as np
import pandas as pd
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.featurization.featurizationconfig import FeaturizationConfig
from azureml.automl.core.shared import constants
from azureml.automl.core.shared import utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    BadArgument,
    InsufficientMemoryWithHeuristics,
    TimeSeriesReservedColumn,
    InvalidInputDatatype,
    NoValidDates,
    TimeseriesInvalidTimestamp,
    TimeseriesCannotDropSpecialColumn,
    TimeseriesDfFrequencyNotConsistent,
    TimeseriesDfCannotInferFrequencyFromTSId,
    TimeseriesDfFrequencyGenericError,
    TimeseriesDfMultiFrequenciesDiff,
    TimeseriesDfMissingColumn,
    TimeseriesDfUniqueTargetValueGrain,
    TimeColumnValueOutOfRange,
    TimeseriesDfDuplicatedIndexTimeColTimeIndexColName,
    TimeseriesDfDuplicatedIndexTimeColName,
    TimeseriesDfFrequencyChanged,
    TimeseriesDfTrainingValidDataNotContiguous,
    TimeseriesInsufficientData,
    TimeseriesTimeColNameOverlapIdColNames,
    TimeseriesInsufficientDataValidateTrainData,
    TimeseriesGrainAbsentValidateTrainValidData,
    TimeseriesDfInvalidArgNoValidationData,
    TimeseriesDfInvalidArgParamIncompatible)
from azureml.automl.core.shared.constants import TimeSeries, TimeSeriesInternal, SupportedInputDatatypes,\
    ShortSeriesHandlingValues
from azureml.automl.core.shared.exceptions import DataException, ResourceException, ValidationException
from azureml.automl.core.shared.forecasting_exception import (ForecastingDataException,
                                                              ForecastingConfigException
                                                              )
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.types import GrainType
from azureml.automl.runtime import _common_training_utilities
from azureml.automl.runtime import frequency_fixer
from azureml.automl.runtime.data_transformation import _add_raw_column_names_to_X
from azureml.automl.runtime.featurizer.transformer import TimeSeriesPipelineType, TimeSeriesTransformer
from azureml.automl.runtime.featurizer.transformer.timeseries import forecasting_heuristic_utils
from azureml.automl.runtime.shared import memory_utilities
from azureml.automl.runtime.shared.time_series_data_frame import TimeSeriesDataFrame
from azureml.automl.runtime.shared.types import DataInputType
from pandas.tseries.frequencies import to_offset


def _get_df_or_raise(X: DataInputType,
                     x_raw_column_names: Optional[np.ndarray] = None,
                     ignore_errors: bool = False) -> pd.DataFrame:
    """
    Create a pandas DataFrame based on the raw column names or raise an exception if it is not possible.

    :param X: The input data to be converted to a data frame.
    :param x_raw_column_names: The names for columns of X.
    :param ignore_errors: if True, the absent column names will not trigger the exception.
    :raises: DataException if X is not a data frame and columns are not provided.
    """
    if isinstance(X, pd.DataFrame):
        return X

    if x_raw_column_names is not None:
        # check if there is any conflict in the x_raw_column_names
        if not ignore_errors:
            _check_timeseries_input_column_names(x_raw_column_names)
            # generate dataframe for tsdf.
            return _add_raw_column_names_to_X(x_raw_column_names, X)
        return pd.DataFrame(X, columns=x_raw_column_names)
    df = pd.DataFrame(X)
    if not ignore_errors:
        # if x_raw_column_name is None, then the origin input data is ndarray.
        raise DataException._with_error(AzureMLError.create(
            InvalidInputDatatype, target="X", input_type=type(X), supported_types=SupportedInputDatatypes.PANDAS))
    return df


def _check_timeseries_input_column_names(x_raw_column_names: np.ndarray) -> None:
    """
    Check if the column name is not in the reserved column name list.

    :param x_raw_column_names: The list of the columns names.
    :raises: ForecastingDataException if the column is contained in the reserved column list.
    """
    for col in x_raw_column_names:
        if col in constants.TimeSeriesInternal.RESERVED_COLUMN_NAMES:
            raise ForecastingDataException._with_error(
                AzureMLError.create(
                    TimeSeriesReservedColumn,
                    target="reserved_columns",
                    reference_code=ReferenceCodes._TS_VALIDATION_RESERVED_COLUMNS,
                    col=col)
            )


def validate_timeseries_training_data(automl_settings: AutoMLBaseSettings,
                                      X: DataInputType,
                                      y: DataInputType,
                                      X_valid: Optional[DataInputType] = None,
                                      y_valid: Optional[DataInputType] = None,
                                      sample_weight: Optional[np.ndarray] = None,
                                      sample_weight_valid: Optional[np.ndarray] = None,
                                      cv_splits_indices: Optional[np.ndarray] = None,
                                      x_raw_column_names: Optional[np.ndarray] = None) -> None:
    """
    Quick check of the timeseries input values, no tsdf is required here.

    :param automl_settings: automl settings
    :param X: Training data.
    :param y: target/label data.
    :param X: Validation data.
    :param y: Validation target/label data.
    :param sample_weight: Sample weights for the training set.
    :param sample_weight_valid: Sample weights for the validation set.
    :param cv_splits_indices: Indices for the cross validation.
    :param x_raw_column_names: The column names for the features in train and valid set.
    """
    if automl_settings.freq is not None:
        frequency_fixer.str_to_offset_safe(automl_settings.freq,
                                           ReferenceCodes._TRAINING_UTILITIES_CHECK_FREQ)
    if automl_settings.grain_column_names is None:
        grain_set = set()  # type: Set[str]
    else:
        grain_set = set(automl_settings.grain_column_names)
    if automl_settings.drop_column_names is not None:
        drop_set = set(automl_settings.drop_column_names)
        if (automl_settings.time_column_name in drop_set):
            raise ForecastingConfigException._with_error(
                AzureMLError.create(TimeseriesCannotDropSpecialColumn,
                                    target='automl_settings.drop_column_names',
                                    reference_code=ReferenceCodes._TS_CANNOT_DROP_SPECIAL_COL_TM,
                                    column_name='Time')
            )
        # Check if grain columns are overlapped with drop columns.
        if automl_settings.grain_column_names is not None:
            if drop_set.intersection(grain_set):
                raise ForecastingConfigException._with_error(
                    AzureMLError.create(TimeseriesCannotDropSpecialColumn,
                                        target='automl_settings.drop_column_names',
                                        reference_code=ReferenceCodes._TS_CANNOT_DROP_SPECIAL_COL_TM_IDX,
                                        column_name='Time series identifier')
                )
    if automl_settings.time_column_name in grain_set:
        raise ForecastingConfigException._with_error(
            AzureMLError.create(TimeseriesTimeColNameOverlapIdColNames, target='time_series_id_values',
                                reference_code=ReferenceCodes._TS_TIME_COL_NAME_OVERLAP_ID_COL_NAMES,
                                time_column_name=automl_settings.time_column_name)
        )

    if automl_settings.n_cross_validations is None and X_valid is None:
        raise ForecastingConfigException._with_error(
            AzureMLError.create(TimeseriesDfInvalidArgNoValidationData,
                                target='automl_settings.n_cross_validations, X_valid',
                                reference_code=ReferenceCodes._TSDF_INVALID_ARG_NO_VALIDATION_DATA)
        )
    elif cv_splits_indices is not None or \
            (automl_settings.validation_size is not None and automl_settings.validation_size > 0.0):
        if cv_splits_indices is not None:
            error_validation_config = "cv_splits_indices"
        else:
            error_validation_config = "validation_size"
        raise ForecastingConfigException._with_error(
            AzureMLError.create(TimeseriesDfInvalidArgParamIncompatible,
                                target='cv_splits_indices',
                                reference_code=ReferenceCodes._TSDF_INVALID_ARG_PARAM_INCOMPATIBLE,
                                param=error_validation_config)
        )
    else:
        # Create the data frame before we will determine heuristic parameters.
        # The data frame is necessary for this function.
        X = _check_timeseries_input(X, y, automl_settings, x_raw_column_names, is_validation_data=False)
        X_valid = _check_timeseries_input(
            X_valid, y_valid, automl_settings, x_raw_column_names, is_validation_data=True)
        lags, window_size, forecast_horizon = _get_auto_parameters_maybe(automl_settings, X, y)
        min_points = utilities.get_min_points(
            window_size,
            lags,
            forecast_horizon,
            automl_settings.n_cross_validations)
        _post_auto_param_gen_validation(X, y, X_valid, y_valid,
                                        automl_settings, forecast_horizon,
                                        window_size=window_size, lags=lags,
                                        min_points=min_points)


def _post_auto_param_gen_validation(
        X: pd.DataFrame,
        y: DataInputType,
        X_valid: pd.DataFrame,
        y_valid: DataInputType,
        automl_settings: AutoMLBaseSettings,
        forecast_horizon: int,
        window_size: int,
        lags: List[int],
        min_points: int) -> None:
    """
    The set of validations, whic can run only after we have detected the auto parameters.

    :param X: The data frame with features.
    :param y: The array with targets/labels.
    :param X_valid: The validation data set.
    :param y_valid: The target
    :param automl_settings: The settings to be used.
    :param forecast_horizon : The max horizon used (after the heuristics were applied).
    :param window_size: The actual window size, provided by the user or detected.
    :param lags: Tje actual lags, provided by the user or detected.
    :param min_points: The minimal number of points necessary to train the model.
    """
    if X.shape[0] < min_points:
        raise ForecastingDataException._with_error(
            AzureMLError.create(TimeseriesInsufficientDataValidateTrainData, target='X.shape',
                                reference_code=ReferenceCodes._TS_WRONG_SHAPE_DATA_VALIDATE_TRAIN_DATA,
                                min_points=min_points,
                                n_cross_validations=automl_settings.n_cross_validations,
                                max_horizon=forecast_horizon,
                                lags=lags,
                                window_size=window_size,
                                shape=X.shape[0])
        )
    _common_training_utilities._column_value_number_check(y, constants.Subtasks.FORECASTING)
    tsdf = _get_and_validate_tsdf(
        X, y, automl_settings, forecast_horizon, min_points, is_validation_data=False)
    tsdf_valid = None
    if X_valid is not None:
        tsdf_valid = _get_and_validate_tsdf(
            X_valid,
            y_valid,
            automl_settings,
            forecast_horizon,
            min_points=0,
            is_validation_data=True)
        _validate_timeseries_train_valid_tsdf(tsdf, tsdf_valid, bool(window_size + max(lags)))


def _get_auto_parameters_maybe(automl_settings: AutoMLBaseSettings,
                               X: pd.DataFrame,
                               y: DataInputType) -> Tuple[List[int], int, int]:
    """
    Return the parameters which should be estimated heuristically.

    Now 09/18/2019 it is lags, window_size and max_horizon.
    :param automl_settings: The settings of the run.
    :param X: The input data frame. If the type of input is not a data frame no heursitics will be estimated.
    :param y: The expected data.
    """
    # quick check of the data, no need of tsdf here.
    window_size = automl_settings.window_size if automl_settings.window_size is not None else 0
    lags = automl_settings.lags[constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN] \
        if automl_settings.lags is not None else [0]  # type: List[Union[str, int]]
    # We need to get the heuristics to estimate the minimal number of points needed for training.
    max_horizon = automl_settings.max_horizon
    # Estimate heuristics if needed.
    if max_horizon == constants.TimeSeries.AUTO:
        max_horizon = forecasting_heuristic_utils.get_heuristic_max_horizon(
            X,
            automl_settings.time_column_name,
            automl_settings.grain_column_names)
    if window_size == constants.TimeSeries.AUTO or lags == [constants.TimeSeries.AUTO]:
        X[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y
        heuristics_lags, heuristics_rw = forecasting_heuristic_utils.analyze_pacf_per_grain(
            X,
            automl_settings.time_column_name,
            TimeSeriesInternal.DUMMY_TARGET_COLUMN,
            automl_settings.grain_column_names)
        # Make sure we have removed the y back from the data frame.
        X.drop(TimeSeriesInternal.DUMMY_TARGET_COLUMN, axis=1, inplace=True)
        if window_size == constants.TimeSeries.AUTO:
            window_size = heuristics_rw
        if lags == [constants.TimeSeries.AUTO]:
            lags = [heuristics_lags]
    return cast(List[int], lags), cast(int, window_size), cast(int, max_horizon)


def _check_grain_min_points(number_of_data_points: int,
                            min_points: int,
                            automl_settings: AutoMLBaseSettings,
                            grain_name: Optional[GrainType] = None) -> None:
    """
    Check if each of the grain(series) contains minimal number of the data points.

    :param number_of_data_points: The number of data points in one grain.
    :param min_points: The minimal number of points required for training.
    :param automl_settings: The autoML settings.
    :param grain_name: The name of a grain being checked.
    :raises: DataException
    """
    # First check if we have the short series handling configuration and then fall back
    # to the legacy mechanism.
    has_config = hasattr(automl_settings,
                         TimeSeries.SHORT_SERIES_HANDLING_CONFIG)
    config_val = automl_settings.short_series_handling_configuration if has_config else None
    if (has_config and
        config_val == ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO or
            config_val == ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP):
        # If we are going to remove short series, do not validate for it.
        # If all series are too short, grain dropper will throw an error.
        return
    if (not has_config and
            hasattr(automl_settings, TimeSeries.SHORT_SERIES_HANDLING) and
            getattr(automl_settings, TimeSeries.SHORT_SERIES_HANDLING)):
        # If we are going to remove short series, do not validate for it.
        # If all series are too short, grain dropper will throw an error.
        return

    if number_of_data_points < min_points:
        window_size = automl_settings.window_size if automl_settings.window_size is not None else 0
        lags = automl_settings.lags[constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN] \
            if automl_settings.lags is not None else 0
        if grain_name is None:
            raise DataException._with_error(AzureMLError.create(
                TimeseriesInsufficientData, target="X", grains=grain_name, num_cv=automl_settings.n_cross_validations,
                max_horizon=automl_settings.max_horizon, lags=str(lags), window_size=window_size)
            )
        if not isinstance(grain_name, list) and not isinstance(grain_name, tuple):
            grain_name = [grain_name]

        raise DataException._with_error(AzureMLError.create(
            TimeseriesInsufficientData, target="X", grains=str(grain_name),
            num_cv=automl_settings.n_cross_validations, max_horizon=automl_settings.max_horizon, lags=str(lags),
            window_size=window_size)
        )


def check_memory_limit(X: DataInputType, y: DataInputType) -> None:
    """
    Check the memory availiability.

    :param X: The dataframe with predictors.
    :param y: The data set with targets.
    :raises: ResourceException
    """
    # We need to estimate the amount of memory, used by the data set and if
    # there is a risk of out of memory we need to raise an exception here.
    avail_memory = None  # Optional[int]
    all_memory = None  # Optional[int]
    try:
        # Make this code safe.
        avail_memory = memory_utilities.get_available_physical_memory()
        all_memory = memory_utilities.get_all_ram()
    except Exception:
        return
    memory_per_df = memory_utilities.get_data_memory_size(X)
    memory_per_df += memory_utilities.get_data_memory_size(y)
    # We have found that the amount of memory needed to process the data frame is
    # approximately 10 * data frame size.
    needed_memory = memory_per_df * 10
    if avail_memory < needed_memory:
        raise ResourceException._with_error(
            AzureMLError.create(
                InsufficientMemoryWithHeuristics,
                avail_mem=avail_memory,
                total_mem=all_memory,
                min_mem=needed_memory
            ))


def _check_timeseries_input(
        X: Optional[DataInputType],
        y: Optional[DataInputType],
        automl_settings: AutoMLBaseSettings,
        x_raw_column_names: Optional[np.ndarray],
        is_validation_data: bool = False) -> pd.DataFrame:
    """
    Check the time series data frame parameters.

    :param X: The data frame with features.
    :param y: The array with targets/labels.
    :param automl_settings: The settings to be used.
    :param x_raw_column_names: The column names for the features in train and valid set.
    :param is_validation_data: True if this is a validation data set.
    """
    if X is None or y is None:
        return None
    X = _get_df_or_raise(X, x_raw_column_names)
    # Check if we have enough memory.
    check_memory_limit(X, y)
    timeseries_param_dict = utilities._get_ts_params_dict(automl_settings)
    if timeseries_param_dict is None:
        raise ForecastingConfigException._with_error(
            AzureMLError.create(BadArgument,
                                target='timeseries_param_dict',
                                reference_code=ReferenceCodes._TSDF_INVALID_ARG_CHK_INPUT,
                                argument_name='timeseries_param_dict')
        )
    _check_columns_present(X, timeseries_param_dict)
    # Check that we contain the actual time stamps in the DataFrame
    if X[automl_settings.time_column_name].count() == 0:
        raise ForecastingDataException._with_error(
            AzureMLError.create(
                NoValidDates,
                time_column_name=automl_settings.time_column_name,
                reference_code=ReferenceCodes._TSDF_TM_COL_CONTAINS_NAT_ONLY,
                target=TimeSeries.TIME_COLUMN_NAME)
        )
    # Convert time column to datetime only if all columns are already present.
    time_param = timeseries_param_dict.get(TimeSeries.TIME_COLUMN_NAME)
    if isinstance(time_param, str):
        frequency_fixer.convert_to_datetime(X, time_param)
    # Check not supported datatypes and warn
    _check_supported_data_type(X)
    _check_time_index_duplication(X, automl_settings.time_column_name, automl_settings.grain_column_names)
    _check_valid_pd_time(X, automl_settings.time_column_name)
    return X


def _get_and_validate_tsdf(
        X: pd.DataFrame,
        y: DataInputType,
        automl_settings: AutoMLBaseSettings,
        forecast_horizon: int,
        min_points: int = 0,
        is_validation_data: bool = False
) -> TimeSeriesDataFrame:
    """
    Generate the TimeSeriesDataFrame and run validations on it.

    :param X: The data frame with features.
    :param y: The array with targets/labels.
    :param automl_settings: The settings to be used.
    :param forecast_horizon : The max horizon used (after the heuristics were applied).
    :param min_points: The minimal number of points necessary to train the model.
    :param is_validation_data: True if this is a validation data set.
    :return: TimeSeriesDataFrame with the data from the X and y.

    """
    # We cast timeseries_param_dict to dictionary, because we have already checked that it is not None
    # before in the _check_timeseries_input method.
    timeseries_param_dict = cast(Dict[str, str], utilities._get_ts_params_dict(automl_settings))
    feat_config = cast(Optional[FeaturizationConfig], timeseries_param_dict.pop("featurization_config", None))
    tst = TimeSeriesTransformer(pipeline_type=TimeSeriesPipelineType.FULL,
                                featurization_config=feat_config, **timeseries_param_dict)
    tsdf = tst.construct_tsdf(X, y)
    tsdf.sort_index(inplace=True)
    frequencies_grain_names = {}  # type: Dict[pd.DateOffset, List[GrainType]]
    short_grains = set()
    if automl_settings.grain_column_names is not None:
        # to deal the problem that user has no input grain
        try:
            freq_by_grain = None  # type: pd.Series
            if automl_settings.freq is None:
                freq_by_grain = tsdf.infer_freq_by_grain()
            for data_tuple in tsdf.groupby_grain():
                grain_name_str = data_tuple[0]
                tsdf_grain = data_tuple[1]
                data_points = tsdf_grain.shape[0]

                if not is_validation_data or tsdf_grain.shape[0] > 1:
                    # if validation data is only one data point, no need to check freq.
                    # If frequency is provided, check if it is consistent.
                    if automl_settings.freq is None:
                        freq = freq_by_grain[grain_name_str]
                    else:
                        freq = to_offset(automl_settings.freq)
                    if tsdf_grain.shape[0] != 1:
                        # We can not establish the frequency only if tsdf_grain has only one value.
                        if freq is None:
                            raise ForecastingDataException._with_error(
                                AzureMLError.create(TimeseriesDfCannotInferFrequencyFromTSId, target='tsdf_grain',
                                                    reference_code=ReferenceCodes._TSDF_CANNOT_INFER_FREQ_FROM_TS_ID,
                                                    grain_name_str=grain_name_str)
                            )
                        # Check alignment with the inferred frequency
                        _check_timeseries_alignment_single_grain(grain_name_str, tsdf_grain, freq)

                        if freq in frequencies_grain_names:
                            frequencies_grain_names[freq].append(grain_name_str)
                        else:
                            frequencies_grain_names[freq] = [grain_name_str]
                    # check min data points for train and forecast_horizon  for validation
                    data_points = tsdf_grain.ts_value.count()
                    if not is_validation_data:
                        if data_points < min_points:
                            short_grains.add(grain_name_str)
                        _check_grain_min_points(
                            data_points, min_points, automl_settings, grain_name=grain_name_str)
                        if tsdf_grain.shape[0] != 1:
                            _check_cv_gap_exist(tsdf_grain,
                                                forecast_horizon,
                                                automl_settings.n_cross_validations,
                                                grain_name_str, freq)
                        # check if individual grain has more than 1 unique observation
                        if (not automl_settings.short_series_handling or grain_name_str not in short_grains) and \
                                (tsdf_grain.ts_value.nunique(dropna=True) <= 1):
                            raise ForecastingDataException._with_error(
                                AzureMLError.create(
                                    TimeseriesDfUniqueTargetValueGrain,
                                    target="grain_target",
                                    grain=grain_name_str,
                                    reference_code=ReferenceCodes._TSDF_UNIQUE_VALUE_IN_GRAIN)
                            )
                if is_validation_data:
                    if data_points < forecast_horizon:
                        print(("WARNING: Validation set has fewer data points ({}) "
                               "than forecast_horizon  ({}) for one of time series identifiers. "
                               "We will be unable to estimate error and predictive quantiles at some horizons. "
                               "Please consider increasing the validation data to the length of max horizon.").
                              format(data_points, forecast_horizon))
                    elif data_points > forecast_horizon:
                        print(("WARNING: Validation set has more data points {} "
                               "than forecast_horizon  {} for one of time series identifiers. "
                               "Not all validation data will be used in the training. "
                               "Please consider decreasing the validation data to the length of max horizon.").
                              format(data_points, forecast_horizon))

        except DataException:
            # If we already have a descriptive Exception, raise it.
            raise
        except Exception as me:
            # If not, raise generic exception.
            raise ForecastingDataException._with_error(
                AzureMLError.create(
                    TimeseriesDfFrequencyGenericError, target='ts_freq_generic',
                    reference_code=ReferenceCodes._TSDF_FREQUENCY_GENERIC_ERROR
                ), inner_exception=me
            ) from me

        _check_tsdf_frequencies(frequencies_grain_names, short_grains)
    # check all the tsdf at the end.
    if not is_validation_data:
        if automl_settings.freq is None:
            tsdf_freq = tsdf.infer_freq()
        else:
            tsdf_freq = to_offset(automl_settings.freq)
        data_points = tsdf.ts_value.count()
        _check_grain_min_points(data_points, min_points, automl_settings)
        _check_cv_gap_exist(tsdf, forecast_horizon, automl_settings.n_cross_validations, freq=tsdf_freq)
    return tsdf


def _check_cv_gap_exist(tsdf: TimeSeriesDataFrame,
                        max_horizon: int,
                        n_cross_validations: Optional[int] = None,
                        grain_name: Optional[str] = None,
                        freq: Optional[pd.DateOffset] = None) -> None:
    """
    Check if one of the cross validation splits lacks the data.

    :param tsdf: One grain of a time series data frame.
    :param max_horizon: The maximal horizon, used for prediction.
    :param n_cross_validations: The number of cross validations.
    :param grain_name: The grain being analyzed if any.
    :param freq: The frequency of the data in the time series data frame.
    """
    if n_cross_validations is not None:
        if freq is None:
            freq = tsdf.infer_freq()
        for i in range(n_cross_validations):
            # In this code we are estimating the number of missing values in the cross
            # validation fold.
            # if this amount is bigger then some arbitrary number, currently 25%
            # the validation is considered to be failed.
            max_time = tsdf.time_index.max()
            # pandas bug: https://github.com/pandas-dev/pandas/issues/33683
            # may result in weird behavior when freq * 0 is applied. For that reason,
            # end time will have special handling. Start time will always have multiplier
            # of at least one since max_horizon must be >= 1
            end_time = max_time if i != 0 else max_time - i * freq
            expected_dates = pd.date_range(start=max_time - (i + max_horizon) * freq,
                                           end=end_time,
                                           freq=freq)
            # Compare the expected dates with the real dates.
            missing_dates = sorted([str(val) for val in set(expected_dates).difference(set(tsdf.time_index))])
            n_absent_in_cv = len(missing_dates)
            # Currently we have commented out the exceptions, because the check is strict.
            # In future we want to replace the exceptions by guard rails.
            if n_absent_in_cv == max_horizon:
                missing_dates_str = ", ".join(missing_dates)
                if grain_name is None:
                    exception_msg = (
                        "Missing timestamp(s) {} in data. "
                        "One of the validation folds will be empty "
                        "because the data at the end of time series are missing")
                    exception_msg = exception_msg.format(missing_dates_str)
                    # deEx = DataException(
                    #    exception_msg.format(missing_dates_str)).with_generic_msg(
                    #        exception_msg.format(MASKED))
                else:
                    exception_msg = ("Missing timestamp(s) {} in data in series {}. "
                                     "One of the validation folds will be empty "
                                     "because the data at the end of time series are missing")
                    exception_msg = exception_msg.format(missing_dates_str, grain_name)
                    # deEx = DataException(
                    #    exception_msg.format(missing_dates_str, grain_name)).with_generic_msg(
                    #        exception_msg.format(MASKED, MASKED))
                # raise deEx
                # Warning is commented, because the warning text may be logged.
                # warnings.warn(exception_msg)


def _check_valid_pd_time(df: pd.DataFrame, time_column_name: str) -> None:
    """
    Check the validity of data in the date column.

    :param df: The data frame to be checked.
    :param time_column_name: the name of a time column.
    """
    try:
        pd.to_datetime(df[time_column_name])
    except pd.errors.OutOfBoundsDatetime as e:
        raise DataException._with_error(
            AzureMLError.create(TimeColumnValueOutOfRange, target=time_column_name, column_name=time_column_name,
                                min_timestamp=pd.Timestamp.min, max_timestamp=pd.Timestamp.max),
            inner_exception=e
        ) from e
    except ValueError as ve:
        raise ValidationException._with_error(
            AzureMLError.create(TimeseriesInvalidTimestamp, target="X"), inner_exception=ve
        ) from ve


def _check_time_index_duplication(df: pd.DataFrame,
                                  time_column_name: str,
                                  grain_column_names: Optional[List[str]] = None) -> None:
    """
    Check if the data frame contain duplicated timestamps within the one grain.

    :param df: The data frame to be checked.
    :param time_column_name: the name of a time column.
    :param grain_column_names: the names of grain columns.
    """
    group_by_col = [time_column_name]
    if grain_column_names is not None:
        if isinstance(grain_column_names, str):
            grain_column_names = [grain_column_names]
        group_by_col.extend(grain_column_names)
    duplicateRowsDF = df[df.duplicated(subset=group_by_col, keep=False)]
    if duplicateRowsDF.shape[0] > 0:
        if grain_column_names is not None and len(grain_column_names) > 0:
            raise ForecastingDataException._with_error(
                AzureMLError.create(TimeseriesDfDuplicatedIndexTimeColTimeIndexColName,
                                    target='time_column_name',
                                    reference_code=ReferenceCodes._TSDF_DUPLICATED_INDEX_TM_COL_TM_IDX_COL_NAME,
                                    time_column_name=time_column_name,
                                    grain_column_names=grain_column_names)
            )
        else:
            raise ForecastingDataException._with_error(
                AzureMLError.create(TimeseriesDfDuplicatedIndexTimeColName,
                                    target='time_column_name',
                                    reference_code=ReferenceCodes._TSDF_DUPLICATED_INDEX_TM_COL_NAME,
                                    time_column_name=time_column_name)
            )


def _check_timeseries_alignment_single_grain(grain_level: GrainType, tsdf: TimeSeriesDataFrame,
                                             freq: pd.DateOffset) -> None:
    """
    Check if single timeseries (single grain) is aligned to the given frequency.

    :param grain_level: The name of a grain.
    :param tsdf: The time series dataframe to be tested.
    :param freq: Frequency to check alignment against.
    """
    time_index = tsdf.time_index
    if not isinstance(time_index[0], pd.Timestamp):
        raise ValidationException._with_error(AzureMLError.create(TimeseriesInvalidTimestamp, target="X"))

    onfreq_time = pd.date_range(start=time_index.min(), end=time_index.max(), freq=freq)
    if not set(time_index).issubset(onfreq_time):
        raise ForecastingDataException._with_error(
            AzureMLError.create(TimeseriesDfFrequencyNotConsistent,
                                target='_check_timeseries_alignment_single_grain.time_index',
                                reference_code=ReferenceCodes._TSDF_FREQUENCY_NOT_CONSISTENT_SINGLE_GRAIN,
                                grain_level=str(grain_level),
                                freq=str(freq))
        )


def _validate_timeseries_train_valid_tsdf(tsdf_train: TimeSeriesDataFrame,
                                          tsdf_valid: TimeSeriesDataFrame,
                                          has_lookback_features: bool) -> None:
    """
    Validate train-valid pair in the time series task.

    :param tsdf_train: The training data set.
    :param tsdf_valid: The validation data set.
    :param has_lookback_features: True if rolling window or lag lead is switched on.
    """
    train_grain_data_dict = {grain: tsdf for grain, tsdf in tsdf_train.groupby_grain()}
    valid_grain_data_dict = {grain: tsdf for grain, tsdf in tsdf_valid.groupby_grain()}
    train_grain = set(train_grain_data_dict.keys())
    valid_grain = set(valid_grain_data_dict.keys())
    # check grain is the same for train and valid.
    grain_difference = train_grain.symmetric_difference(valid_grain)
    if len(grain_difference) > 0:
        grain_in_train_not_in_valid = train_grain.intersection(grain_difference)
        grain_in_valid_not_in_train = valid_grain.intersection(grain_difference)
        if len(grain_in_train_not_in_valid) > 0:
            grains = ",".join(["[{}]".format(grain) for grain in grain_in_train_not_in_valid])
            dataset_contain = "training"
            dataset_not_contain = "validation"
        if len(grain_in_valid_not_in_train) > 0:
            grains = ",".join(["[{}]".format(grain) for grain in grain_in_valid_not_in_train])
            dataset_contain = "validation"
            dataset_not_contain = "training"
        raise ForecastingDataException._with_error(
            AzureMLError.create(TimeseriesGrainAbsentValidateTrainValidData, target='grain_difference',
                                reference_code=ReferenceCodes._TS_GRAIN_ABSENT_VALIDATE_TRAIN_VALID,
                                grains=grains,
                                dataset_contain=dataset_contain,
                                dataset_not_contain=dataset_not_contain)
        )
    # check per grain contiguous and frequency.
    for grain, tsdf in train_grain_data_dict.items():
        tsdf_valid = valid_grain_data_dict[grain]
        train_freq = tsdf.infer_freq()
        if train_freq is None:
            # The only reason we cannot determine the frequency is because we have a grain'
            # with one value, or two values, one of which is pd.NaT.
            # In this case we have a short grain, which should be dropped, or we should raise the exception later.
            continue
        if has_lookback_features and tsdf.time_index.max() + tsdf.infer_freq() != tsdf_valid.time_index.min():
            raise ForecastingDataException._with_error(
                AzureMLError.create(TimeseriesDfTrainingValidDataNotContiguous, target='tsdf_valid',
                                    reference_code=ReferenceCodes._TSDF_TRAINING_VALID_DATA_NOT_CONTIGUOUS,
                                    grain=str(grain))
            )
        if tsdf_valid.shape[0] > 1:
            valid_freq = tsdf_valid.infer_freq()
            if train_freq != valid_freq:
                raise ForecastingDataException._with_error(
                    AzureMLError.create(TimeseriesDfFrequencyChanged, target='train_freq',
                                        reference_code=ReferenceCodes._TSDF_FREQUENCY_CHANGED,
                                        grain=str(grain),
                                        train_freq=train_freq,
                                        valid_freq=valid_freq)
                )


def _check_columns_present(df: pd.DataFrame, timeseries_param_dict: Dict[str, str]) -> None:
    """
    Determine if df has the correct column names for time series.

    :param df: The data frame to be analyzed.
    :param timeseries_param_dict: The parameters specific to time series.
    """

    def check_a_in_b(a: Union[str, List[str]], b: List[str]) -> List[str]:
        """
        checks a is in b.

        returns any of a not in b.
        """
        if isinstance(a, str):
            a = [a]

        set_a = set(a)
        set_b = set(b)
        return list(set_a - set_b)

    missing_col_names = []  # type: List[str]
    # check time column in df
    col_name = timeseries_param_dict.get(constants.TimeSeries.TIME_COLUMN_NAME)
    if col_name is not None:
        missing_col_names = check_a_in_b(col_name, df.columns)
    # raise if missing
    if len(missing_col_names) != 0:
        raise ForecastingDataException._with_error(
            AzureMLError.create(TimeseriesDfMissingColumn,
                                target=TimeseriesDfMissingColumn.TIME_COLUMN,
                                reference_code=ReferenceCodes._TST_NO_TIME_COLNAME_TRAIN_UTIL,
                                column_names=constants.TimeSeries.TIME_COLUMN_NAME)
        )

    # check grain column(s) in df
    col_names = timeseries_param_dict.get(constants.TimeSeries.GRAIN_COLUMN_NAMES)
    if col_names is not None:
        missing_col_names = check_a_in_b(col_names, df.columns)
    # raise if missing
    if len(missing_col_names) != 0:
        raise ForecastingDataException._with_error(
            AzureMLError.create(TimeseriesDfMissingColumn,
                                target=TimeseriesDfMissingColumn.GRAIN_COLUMN,
                                reference_code=ReferenceCodes._TST_CHECK_PHASE_NO_GRAIN_CHK_COLS,
                                column_names=constants.TimeSeries.TIME_SERIES_ID_COLUMN_NAMES)
        )

    # check drop column(s) in df
    missing_drop_cols = []  # type: List[str]
    col_names = timeseries_param_dict.get(constants.TimeSeries.DROP_COLUMN_NAMES)
    if col_names is not None:
        missing_drop_cols += check_a_in_b(col_names, df.columns)

    # warn if missing
    if len(missing_drop_cols) != 0:
        warnings.warn("The columns to drop were not found and will be ignored.")


def _check_tsdf_frequencies(frequencies_grain_names: Dict[pd.DateOffset, List[GrainType]],
                            short_grains: Set[GrainType]) -> None:
    """
    Check if all series in the training set have only one frequency.

    :param frequencies_grain_names: The dictionary, containing frequencies and grain names.
    :param short_grains: The grains, which should not be used in this analysis as they
                         will be dropped.
    """
    # pd.DateOffset can not compare directly. need a start time.
    if len(frequencies_grain_names) == 0:
        return
    date_offsets = set()
    for k, v in frequencies_grain_names.items():
        if len(set(v) - short_grains) > 0:
            date_offsets.add(k)
    if len(date_offsets) > 1:
        raise ForecastingDataException._with_error(
            AzureMLError.create(TimeseriesDfMultiFrequenciesDiff, target='date_offsets',
                                reference_code=ReferenceCodes._TSDF_MULTI_FREQUENCIES_DIFF)
        )


def _check_supported_data_type(df: pd.DataFrame) -> None:
    """
    Check if the data frame contains non supported data types.

    :param df: The data frame to be analyzed.
    """
    supported_datatype = set([np.number, np.dtype(object), pd.Categorical.dtype, np.datetime64])
    unknown_datatype = set(df.infer_objects().dtypes) - supported_datatype
    if (len(unknown_datatype) > 0):
        warnings.warn("Following datatypes: {} are not recognized".
                      format(unknown_datatype))
