# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""A module that contains some forecasting models: ARIMA, Prophet, Naive."""
from typing import Any, Dict

import numpy as np
import pandas as pd

from azureml.automl.core.shared import (
    time_series_data_frame,
    constants)
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.types import GrainType

from azureml.automl.runtime.shared._auto_arima import AutoArima
from azureml.automl.runtime.shared._exponential_smoothing import ExponentialSmoothing
from azureml.automl.runtime.shared._prophet_model import ProphetModel
from azureml.automl.runtime.shared._multi_grain_forecast_base import _MultiGrainForecastBase


class _LowCapacityModelStateContainer():
    def __init__(self, series_values: pd.Series):
        self.series_values = series_values


class _LowCapacityModelFitMixin():
    def _set_seasonality_safe(self, timeseries_param_dict: Dict[str, Any]) -> None:
        self.seasonality = timeseries_param_dict.get(
            constants.TimeSeries.SEASONALITY,
            constants.TimeSeriesInternal.SEASONALITY_VALUE_NONSEASONAL
        )
        Contract.assert_true(
            isinstance(self.seasonality, int) and self.seasonality >= 1,
            "Seasonality is not a positive integer.",
            log_safe=True
        )

    def fit_model(self, X_fit_grain: time_series_data_frame.TimeSeriesDataFrame) -> Any:
        series_values = X_fit_grain[constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN]
        return _LowCapacityModelStateContainer(series_values)


class SeasonalNaive(_LowCapacityModelFitMixin, _MultiGrainForecastBase):
    """Seasonal Naive multigrain forecasting model."""

    def __init__(self, **kwargs):
        """Create an seasonal naive multi-grain forecasting model."""
        timeseries_param_dict = kwargs[constants.TimeSeriesInternal.TIMESERIES_PARAM_DICT]
        super().__init__(timeseries_param_dict)
        self._set_seasonality_safe(timeseries_param_dict)

    def _fit_single_grain_impl(self, X_fit_grain: time_series_data_frame.TimeSeriesDataFrame,
                               grain_level: GrainType) -> Any:
        """Fit seasonal naive model on one grain.

        :param grain_level:
            is an object that identifies the series by its
            grain group in a TimeSeriesDataFrame. In practice, it is an element
            of X.groupby_grain().groups.keys(). Implementers can use
            the grain_level to store time series specific state needed for
            training or forecasting.

        :param X_fit_grain:
            the context data for the prediction (X_train).

        :Returns:
             a model object that can be used to make predictions."""
        return self.fit_model(X_fit_grain=X_fit_grain)

    def _get_forecast_single_grain_impl(self,
                                        model: _LowCapacityModelStateContainer,
                                        max_horizon: int,
                                        grain_level: GrainType,
                                        X_pred_grain: time_series_data_frame.TimeSeriesDataFrame) -> np.ndarray:
        """
        Forecast from Seasonal Naive model.

        Respects the X_pred_grain parameter and max_horizon parameter.
        :param model:
            is an object representation of a model. It is the
            object returned by the _fit_single_grain_impl method.

        :param max_horizon:
            int that represents the max horizon.

        :param grain_level:
            is an object that identifies the series by its
            grain group in a TimeSeriesDataFrame. In practice, it is an element
            of X.groupby_grain().groups.keys(). Implementers can use
            the grain_level to store time series specific state needed for
            training or forecasting.
        :param X_pred_grain:
            the context data for the prediction (X_test).

        :Returns:
            a 1-D numpy array of forecasted values for the training data. The data are
            assumed to be in chronological order"""
        if len(model.series_values) < self.seasonality:
            pred = np.repeat(model.series_values.tail(1), max_horizon)
        else:
            pred = np.tile(model.series_values.tail(self.seasonality), int(np.ceil(max_horizon /
                                                                                   self.seasonality)))
        return self.align_out(in_sample=False, pred=pred, X_pred_grain=X_pred_grain,
                              X_fit_grain=model.series_values, max_horizon=max_horizon, freq=self._freq)

    def _fit_in_sample_single_grain_impl(self,
                                         model: _LowCapacityModelStateContainer,
                                         grain_level: GrainType,
                                         X_grain: time_series_data_frame.TimeSeriesDataFrame) -> np.ndarray:
        """Fit seasonal naive model on one or multiple grains.

        :param model:
            is an object representation of a model. It is the
            object returned by the _fit_single_grain_impl method.

        :param grain_level:
            is an object that identifies the series by its
            grain group in a TimeSeriesDataFrame. In practice, it is an element
            of X.groupby_grain().groups.keys(). Implementers can use
            the grain_level to store time series specific state needed for
            training or forecasting.

        :param X_grain:
            the context data for the in-sample prediction (X_train).

        :Returns:
            a np.ndarray containing the fitted values in `fitted`."""
        pred = model.series_values.shift(self.seasonality).fillna(0)
        return self.align_out(in_sample=True, pred=pred, X_pred_grain=X_grain,
                              X_fit_grain=model.series_values, max_horizon=None, freq=None)


class Naive(SeasonalNaive, _MultiGrainForecastBase):
    """Naive multigrain forecasting model."""

    def __init__(self, **kwargs):
        """Create an naive multi-grain forecasting model."""
        SeasonalNaive.__init__(self, **kwargs)
        self.seasonality = 1


class SeasonalAverage(_LowCapacityModelFitMixin, _MultiGrainForecastBase):
    """Seasonal average multigrain forecasting model."""

    def __init__(self, **kwargs):
        """Create an seasonal average multi-grain forecasting model."""
        timeseries_param_dict = kwargs[constants.TimeSeriesInternal.TIMESERIES_PARAM_DICT]
        super().__init__(timeseries_param_dict)
        self._set_seasonality_safe(timeseries_param_dict)
        self.window_size = self.seasonality

    def _fit_single_grain_impl(self, X_fit_grain: time_series_data_frame.TimeSeriesDataFrame,
                               grain_level: GrainType) -> Any:
        """Fit seasonal average model on one grain.

        :param grain_level:
            is an object that identifies the series by its
            grain group in a TimeSeriesDataFrame. In practice, it is an element
            of X.groupby_grain().groups.keys(). Implementers can use
            the grain_level to store time series specific state needed for
            training or forecasting.

        :param X_fit_grain:
            the context data for the prediction (X_train).

        :Returns:
             a model object that can be used to make predictions."""
        return self.fit_model(X_fit_grain=X_fit_grain)

    def _get_forecast_single_grain_impl(self,
                                        model: _LowCapacityModelStateContainer,
                                        max_horizon: int,
                                        grain_level: GrainType,
                                        X_pred_grain: time_series_data_frame.TimeSeriesDataFrame) -> np.ndarray:
        """
        Forecast from Seasonal Average model.

        Respects the X_pred_grain parameter and max_horizon parameter.
        :param model:
            is an object representation of a model. It is the
            object returned by the _fit_single_grain_impl method.

        :param max_horizon:
            int that represents the max horizon.

        :param grain_level:
            is an object that identifies the series by its
            grain group in a TimeSeriesDataFrame. In practice, it is an element
            of X.groupby_grain().groups.keys(). Implementers can use
            the grain_level to store time series specific state needed for
            training or forecasting.

        :param X_pred_grain:
            the context data for the prediction (X_test).

        :Returns:
            a 1-D numpy array of forecasted values for the training data. The data are
            assumed to be in chronological order"""
        if self.window_size is None:
            # Set window_size to length of training data
            self.window_size = len(model.series_values)

        if len(model.series_values) < self.window_size:
            mean_value = model.series_values.mean()
        else:
            mean_value = model.series_values.tail(self.window_size).mean()
        pred = np.repeat(mean_value, max_horizon)
        return self.align_out(in_sample=False, pred=pred, X_pred_grain=X_pred_grain,
                              X_fit_grain=model.series_values, max_horizon=max_horizon, freq=self._freq)

    def _fit_in_sample_single_grain_impl(self,
                                         model: _LowCapacityModelStateContainer,
                                         grain_level: GrainType,
                                         X_grain: time_series_data_frame.TimeSeriesDataFrame) -> np.ndarray:
        """Fit seasonal average model on one or multiple grains.

        :param model:
            is an object representation of a model. It is the
            object returned by the _fit_single_grain_impl method.

        :param grain_level:
            is an object that identifies the series by its
            grain group in a TimeSeriesDataFrame. In practice, it is an element
            of X.groupby_grain().groups.keys(). Implementers can use
            the grain_level to store time series specific state needed for
            training or forecasting.

        :param X_grain:
            the context data for the in-sample prediction (X_train).

        :Returns:
            a np.ndarray containing the fitted values in `fitted`."""
        if self.window_size is None:
            # Set window_size to length of training data
            self.window_size = len(X_grain)

        pred = model.series_values.rolling(window=self.window_size,
                                           min_periods=1).mean().fillna(0)
        return self.align_out(in_sample=True, pred=pred, X_pred_grain=X_grain,
                              X_fit_grain=model.series_values, max_horizon=None, freq=None)


class Average(SeasonalAverage, _MultiGrainForecastBase):
    """Average multigrain forecasting model."""

    def __init__(self, **kwargs):
        """Create an average multi-grain forecasting model."""
        SeasonalAverage.__init__(self, **kwargs)
        self.window_size = None

    def _fit_in_sample_single_grain_impl(self,
                                         model: _LowCapacityModelStateContainer,
                                         grain_level: GrainType,
                                         X_grain: time_series_data_frame.TimeSeriesDataFrame) -> np.ndarray:
        """Fit averaage model on one or multiple grains.

        :param model:
            is an object representation of a model. It is the
            object returned by the _fit_single_grain_impl method.

        :param grain_level:
            is an object that identifies the series by its
            grain group in a TimeSeriesDataFrame. In practice, it is an element
            of X.groupby_grain().groups.keys(). Implementers can use
            the grain_level to store time series specific state needed for
            training or forecasting.

        :param X_grain:
            the context data for the in-sample prediction (X_train).

        :Returns:
            a np.ndarray containing the fitted values in `fitted`."""
        pred = model.series_values.rolling(window=len(model.series_values), min_periods=1).mean()
        return self.align_out(in_sample=True, pred=pred, X_pred_grain=X_grain,
                              X_fit_grain=model.series_values, max_horizon=None, freq=None)
