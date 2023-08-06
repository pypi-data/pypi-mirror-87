# external standard
import datetime as dt

# external packages
import talib as ta

# internal packages
from tradingchartz.src.data_sourcing.nsepy_data import NSEPyData

DEFAULT_UNIVERSE = "NIFTY 50"
DEFAULT_START_DATE = dt.date.today() - dt.timedelta(1825)
DEFAULT_END_DATE = dt.date.today()

UNIVERSE_LIST = ['NIFTY 50']

ALL_TA_INDICATORS = ta.get_function_groups()

CANDLE_PATTERNS = ALL_TA_INDICATORS['Pattern Recognition']
