"""
Trading-Technical-Indicators (tti) python library

File name: _median_price.py
    Implements the Median Price technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import WrongTypeForInputParameter,\
    WrongValueForInputParameter


class MedianPrice(TechnicalIndicator):
    """
    Median Price Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 20): The past periods to be used for the
            calculation of the moving average for the trading signal.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, period=20, fill_missing_values=True):

        # Validate and store if needed, the input parameters
        if isinstance(period, int):
            if period > 0:
                self._period = period
            else:
                raise WrongValueForInputParameter(
                    period, 'period', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(period), 'period', 'int')

        # Control is passing to the parent class
        super().__init__(calling_instance=self.__class__.__name__,
                         input_data=input_data,
                         fill_missing_values=fill_missing_values)

    def _calculateTi(self):
        """
        Calculates the technical indicator for the given input data. The input
        data are taken from an attribute of the parent class.

        Parameters:
            -

        Raises:
            -

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type date.
                It contains one column, the 'mp'.
        """

        # Append to input_data the period-ema for close prices
        # This is required for the trading signal calculation and we want
        # to include it in the graph
        self._input_data['close_ema'] = self._input_data['close'].ewm(
            span=self._period, min_periods=self._period, adjust=False,
            axis=0).mean()

        mp = pd.DataFrame(
            index=self._input_data.index, columns=['mp'],
            data=0.5 * (self._input_data['high'] + self._input_data['low']),
            dtype='float64')

        return mp.round(4)

    def getTiSignal(self):
        """
        Calculates and returns the signal of the technical indicator. The
        Technical Indicator data are taken from an attribute of the parent
        class.

        Parameters:
            -

        Raises:
            -

        Returns:
            tuple (string, integer): The Trading signal. Possible values are
                ('hold', 0), ('buy', -1), ('sell', 1). See TRADE_SIGNALS
                constant in the tti.utils package, constants.py module.
        """

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < self._period:
            return TRADE_SIGNALS['hold']

        # Indicator value goes below Moving Average
        if self._input_data['close_ema'].iat[-2] < \
                self._ti_data['mp'].iat[-2] and \
                self._input_data['close_ema'].iat[-1] > \
                self._ti_data['mp'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # Indicator value goes above Moving Average
        if self._input_data['close_ema'].iat[-2] > \
                self._ti_data['mp'].iat[-2] and \
                self._input_data['close_ema'].iat[-1] < \
                self._ti_data['mp'].iat[-1]:
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
