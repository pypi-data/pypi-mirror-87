# external package
import talib as ta

# external standard
import pandas as pd


class SignalGenerator:

    def __init__(self,
                 ohlcv_df: pd.DataFrame):
        self.market_data = ohlcv_df
        self.op = self.market_data['Open']
        self.cl = self.market_data['Close']
        self.lo = self.market_data['Low']
        self.hi = self.market_data['High']
        self.v = self.market_data['Volume']
        self._ta_cdl_ptrn_list = None

    @property
    def ta_candle_pattern_list(self):
        if self._ta_cdl_ptrn_list is None:
            self._ta_cdl_ptrn_list = ta.get_function_groups()['Pattern Recognition']
        return self._ta_cdl_ptrn_list

    def ta_candle_pattern(self,
                          pattern_name: str,
                          filter_type: str = None) -> pd.DataFrame:
        return getattr(ta, pattern_name)(self.op, self.hi, self.lo, self.cl)


