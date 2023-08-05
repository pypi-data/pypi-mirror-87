"""
Trading-Technical-Indicators (tti) python library

File name: _chaikin_money_flow.py
    Implements the Chaikin Money Flow technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class ChaikinMoneyFlow(TechnicalIndicator):
    """
    Chaikin Money Flow Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 5): The past periods to be used for the
            calculation of the sum parts in the indicator formula.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, period=5, fill_missing_values=True):

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
                It contains one column, the 'cmf'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Chaikin Money Flow', self._period,
                                     len(self._input_data.index))

        cmf = pd.DataFrame(index=self._input_data.index, columns=['cmf'],
                           data=0, dtype='float64')

        cmf['numerator'] = \
            (self._input_data['volume'] * (
                (self._input_data['close'] - self._input_data['low']) -
                (self._input_data['high'] - self._input_data['close'])
            ) / (
                    self._input_data['high'] - self._input_data['low']
            ))

        cmf['numerator'] = cmf['numerator'].rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).sum()

        cmf['denominator'] = self._input_data['volume'].rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).sum()

        cmf['cmf'] = (cmf['numerator'] / cmf['denominator']).round(4)

        return cmf[['cmf']]

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
        if len(self._ti_data.index) < 3:
            return TRADE_SIGNALS['hold']

        # A sell signal occurs when price reaches a higher high into overbought
        # with the CMF starting to fall.
        if self._ti_data['cmf'].iat[-2] > self._ti_data['cmf'].iat[-1] and \
                max(self._input_data['close'].iloc[-3:-1]) < \
                self._input_data['close'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # A buy signal occurs when price reaches a lower low into overbought
        # with the CMF starting to rise.
        elif self._ti_data['cmf'].iat[-2] < self._ti_data['cmf'].iat[-1] and \
                min(self._input_data['close'].iloc[-3:-1]) >  \
                self._input_data['close'].iat[-1]:
            return TRADE_SIGNALS['buy']

        else:
            return TRADE_SIGNALS['hold']
