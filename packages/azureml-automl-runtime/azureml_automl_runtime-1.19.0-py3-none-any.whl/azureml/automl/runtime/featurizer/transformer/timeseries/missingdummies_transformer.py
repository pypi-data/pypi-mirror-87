# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Add columns indicating corresponding numeric columns have NaN."""
import numpy
import pandas as pd
import warnings

from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from ..automltransformer import AutoMLTransformer
from azureml.automl.runtime.shared.time_series_data_frame import TimeSeriesDataFrame
from typing import Any, Optional, List


# Prevent warnings when using Jupyter
warnings.simplefilter("ignore")
pd.options.mode.chained_assignment = None


class MissingDummiesTransformer(AutoMLTransformer):
    """Add columns indicating corresponding numeric columns have NaN."""

    def __init__(self, numerical_columns: List[str]) -> None:
        """
        Construct for MissingDummiesTransformer.

        :param numerical_columns: The columns that will be marked.
        :type numerical_columns: list
        :return:
        """
        super().__init__()
        self.numerical_columns = numerical_columns

    @function_debug_log_wrapped('info')
    def fit(self, x: TimeSeriesDataFrame, y: Optional[numpy.ndarray] = None) -> 'MissingDummiesTransformer':
        """
        Fit function for MissingDummiesTransformer.

        :param x: Input data.
        :type x: azureml.automl.runtime.shared.time_series_data_frame.TimeSeriesDataFrame
        :param y: Target values.
        :type y: numpy.ndarray
        :return: Class object itself.
        """
        return self

    @function_debug_log_wrapped('info')
    def transform(self, x: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        """
        Transform function for MissingDummiesTransformer.

        :param x: Input data.
        :type x: azureml.automl.runtime.shared.time_series_data_frame.TimeSeriesDataFrame
        :return: Result of MissingDummiesTransformer.
        """
        for col in self.numerical_columns:
            x[MissingDummiesTransformer.get_column_name(col)] = x[col].isnull().astype('int')
        return x

    @staticmethod
    def get_column_name(col: str) -> str:
        """
        Return the name of column marking nan in the given source column.

        :param col: the name of the source column.
        :return: the name of new feature column.
        """
        return col + '_WASNULL'
