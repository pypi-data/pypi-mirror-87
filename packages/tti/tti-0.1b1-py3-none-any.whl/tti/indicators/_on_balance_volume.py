"""
Trading-Technical-Indicators (tti) python library

File name: _on_balance_volume.py
    Implements the On Balance Volume technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS


class OnBalanceVolume(TechnicalIndicator):
    """
    On Balance Volume Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, fill_missing_values=True):

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
                It contains one column, the 'obv'.
        """

        obv = pd.DataFrame(index=self._input_data.index, columns=['obv'],
                           data=0, dtype='int64')

        obv['obv'][self._input_data['close'] > self._input_data['close'].
            shift(1)] = self._input_data['volume']

        obv['obv'][self._input_data['close'] < self._input_data['close'].
            shift(1)] = -self._input_data['volume']

        obv['obv'] = obv['obv'].cumsum()

        return obv

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

        # Trading signals on warnings for breakout (upward or downward)
        # 3-days period is used for trend calculation

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 3:
            return TRADE_SIGNALS['hold']

        # Warning for a downward breakout
        if self._ti_data['obv'].iat[-3] > self._ti_data['obv'].iat[-2] > \
                self._ti_data['obv'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # Warning for a upward breakout
        elif self._ti_data['obv'].iat[-3] < self._ti_data['obv'].iat[-2] < \
                self._ti_data['obv'].iat[-1]:
            return TRADE_SIGNALS['sell']

        else:
            return TRADE_SIGNALS['hold']
