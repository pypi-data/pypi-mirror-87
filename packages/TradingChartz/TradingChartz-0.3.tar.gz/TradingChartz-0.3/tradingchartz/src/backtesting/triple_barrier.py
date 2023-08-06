# import standard
import pandas as pd
import numpy as np
import datetime as dt

from typing import Tuple


# internal imports
from tradingchartz.src.backtesting.data_classes import TripleBarrierSetter, TripleBarrier, TripleBarrierConfig
from tradingchartz.src.backtesting.default_and_configs import DEFAULT_TB_CONFIG
from tradingchartz.src.backtesting.enums_and_constants import BetDirection


class TripleBarrierCalculator:
    """
    Calculates the triple barrier for each signal bar.
    It returns the tuple with five elements, first indicates barrier hit bar (bar # post signal bar)
    and rest 3 corresponding to each barrier either 0 or 1 based on which barrier is hit first. Last is % return
    calculated based on which ever barrier is hit first.
    For upper and lower barrier last element will be % return at barrier level itself and for vertical barrier it will
    return based on close price for vertical barrier bar.
    Note: Upper barrier hit will be calculated based on High price of following bars and similarly Lower barrier
     will be calculated based on Low price of bars and vertical barrier based on close price.
    All returns are calculated based on entry point field which is open price of next bar from signal bar as default.
    Reco: Instead of fixing the barrier level %, we can dynamically determine it as multiple of average true range on
    signal day.
    Both entry point and price_move_field is calculated based on bar following th e signal bar.
    """
    def __init__(self,
                 triple_barrier: TripleBarrierSetter,
                 df_OHLCV: pd.DataFrame,
                 sr_signal: pd.DataFrame = None,
                 triple_barrier_config: TripleBarrierConfig = DEFAULT_TB_CONFIG
                 ):
        """

        :param triple_barrier: Triple barrier data class with barrier details
        :param df_OHLCV:  pandas dataframe with columns of Open, High, Low, Close
        :param sr_signal: pandas series with index of dates unidirectional signal
        :param triple_barrier_config: Default value is set. Don't update until necessary.
        """
        self.triple_barrier = triple_barrier
        self.df_OHLCV = df_OHLCV
        self.sr_signal = sr_signal

    @property
    def df_signal_with_barrier(self):
        if self.sr_signal is None:
            raise ValueError("Please set the sr_signal value")
        df_temp_signal = self.sr_signal.to_frame(name='signals')
        df_temp_signal['entry_price'] = self.df_OHLCV.loc[self.df_OHLCV.index,
                                                          DEFAULT_TB_CONFIG.entry_point_field]
        df_temp_signal[self.triple_barrier.lower_barrier_field] = self.df_OHLCV.loc[df_temp_signal.index,
                                                                            self.triple_barrier.lower_barrier_field]
        # Checking floor
        if self.triple_barrier.lower_min:
            df_temp_signal[self.triple_barrier.lower_barrier_field] = np.maximum(df_temp_signal[self.triple_barrier.lower_barrier_field],
                                                                              self.triple_barrier.lower_min * df_temp_signal['entry_price'])
        if self.triple_barrier.lower_max:
            df_temp_signal[self.triple_barrier.lower_barrier_field] = np.minimum(df_temp_signal[self.triple_barrier.lower_barrier_field],
                                                                              self.triple_barrier.lower_max * df_temp_signal['entry_price'])

        # Barrier level calculations
        if True:
            df_temp_signal['lower_barrier'] = df_temp_signal['entry_price'] \
                                                  - (df_temp_signal[self.triple_barrier.lower_barrier_field])

        if self.triple_barrier.ratio:
            df_temp_signal['upper_barrier'] = df_temp_signal['entry_price'] \
                                                  + (df_temp_signal[self.triple_barrier.lower_barrier_field] *
                                                     self.triple_barrier.ratio)
        if self.triple_barrier.vertical:
            df_temp_signal['vertical_barrier'] = self.df_OHLCV.shift(-self.triple_barrier.vertical).loc[
                df_temp_signal.index, 'Close']
            # vertical barrier could be NAN here if for the latest signal vertical barrier is still not hit.
        return df_temp_signal

    @property
    def df_triple_barrier_details(self):
        df_temp_triple_barrier_details = self.df_signal_with_barrier

        for date_index, row in df_temp_triple_barrier_details.iterrows():
            # find barrier strategy period.
            _signal_loc = self.df_OHLCV.index.get_loc(date_index)
            barrier = None
            barrier_bar = None
            max_level = None
            if self.triple_barrier.vertical:
                if (_signal_loc + self.triple_barrier.vertical) < len(self.df_OHLCV.index):
                    _ref_df = self.df_OHLCV.iloc[_signal_loc + 1: _signal_loc + self.triple_barrier.vertical, :]
                    barrier = 'vertical'
                    barrier_bar = _ref_df.index[-1]
                else:
                    _ref_df = self.df_OHLCV.iloc[_signal_loc + 1:, :]
            else:
                _ref_df = self.df_OHLCV.iloc[_signal_loc + 1:, :]
            max_level = _ref_df['High'].max()
            if len(_ref_df['Close']) == 0:
                continue
            close_position = _ref_df.iloc[-1]['Close']
            if True:
                # barrier check
                lower_barrier_check = any((_ref_df['Low'] < row['lower_barrier']).values) #Low to cLose
                if lower_barrier_check:
                    barrier = 'lower'
                    _ref_df = _ref_df.iloc[:np.argmax((_ref_df['Low'] < row['lower_barrier']).values) + 1, :] # Low to cLose
                    barrier_bar = _ref_df.index[-1]
                    close_position = row['lower_barrier']  # _ref_df.loc[barrier_bar, "Close"]
                    max_level = _ref_df['High'].iloc[:-1].max()
            if self.triple_barrier.ratio:
                upper_barrier_check = any((_ref_df['High'] > row['upper_barrier']).values) #High to close
                if upper_barrier_check:
                    barrier = 'upper'
                    barrier_bar = _ref_df.index[np.argmax((_ref_df['High'] > row['upper_barrier']).values)] # High to CLose
                    close_position = row['upper_barrier']  # _ref_df.loc[barrier_bar, "Close"]
                    max_level = close_position
            vol_value = self.df_OHLCV.loc[date_index, 'Volume']
            avg_vol_value = self.df_OHLCV.iloc[_signal_loc-10:_signal_loc, self.df_OHLCV.columns.get_loc('Volume')].mean()

            df_temp_triple_barrier_details.loc[date_index, 'barrier_type'] = barrier
            df_temp_triple_barrier_details.loc[date_index, 'barrier_bar'] = barrier_bar
            df_temp_triple_barrier_details.loc[date_index, 'close_level'] = close_position
            df_temp_triple_barrier_details.loc[date_index, 'Vol'] = vol_value
            df_temp_triple_barrier_details.loc[date_index, 'preceding_10day_avg'] = avg_vol_value
            df_temp_triple_barrier_details.loc[date_index, 'max_level'] = max_level

            if barrier_bar:
                barrier_bar_loc = self.df_OHLCV.index.get_loc(barrier_bar)
                df_temp_triple_barrier_details.loc[date_index, 'holding_period_tb'] = barrier_bar_loc - _signal_loc
                df_temp_triple_barrier_details.loc[date_index, 'holding_period_return'] = (close_position/df_temp_triple_barrier_details.loc[date_index,'entry_price'])-1

        return df_temp_triple_barrier_details

    @staticmethod
    def get_triple_barrier_summary(df_triple_barrier_details):
        temp_df = pd.concat([df_triple_barrier_details['barrier_type'].value_counts().T,
                            (df_triple_barrier_details['barrier_type'].value_counts()
                            / df_triple_barrier_details['signals'].count()).T], axis=1)
        temp_df.columns = ['barrier_count', 'barrier_%']
        return temp_df

