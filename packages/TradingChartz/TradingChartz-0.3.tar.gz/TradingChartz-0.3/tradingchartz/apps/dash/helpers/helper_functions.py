# external standards
import datetime as dt
import pandas as pd

from typing import Tuple

# internal imports
from tradingchartz.src.backtesting.triple_barrier import TripleBarrierCalculator


def string_to_date(date_: str):
    return dt.datetime.strptime(date_, '%Y-%m-%d')


def df_from_jason(json_data: str) -> pd.DataFrame:
    return pd.read_json(json_data, orient='index')


def df_bifurcate_positive_and_negative_signals(df_raw_signals: pd.Series) -> Tuple[pd.Series, pd.Series]:
    return df_raw_signals[df_raw_signals > 0], df_raw_signals[df_raw_signals < 0]


def df_add_tb_details(obj_tb_calc: TripleBarrierCalculator,
                      sr_signals: pd.Series):
    obj_tb_calc.sr_signals = sr_signals
    return obj_tb_calc.df_triple_barrier_details

