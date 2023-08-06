# external standard
import pandas as pd
import datetime as dt

# internal imports
from tradingchartz.src.data_sourcing.web_paths import broader_indices_path
import tradingchartz.src.helper.web_scrapping as ws


class NSEPyData(object):
    """Enabling fetching EOD OHLC data from NSE for cash equities"""
    # ToDo: Test and add other instruments such as Index, futures, options etc
    init_ = False

    # new added to insure that we import nsepy and nsetool only once.
    def __new__(cls, *args, **kwargs):
        if not NSEPyData.init_:
            import nsepy
            cls.nsepy = nsepy
            from nsetools import Nse
            cls.nse = Nse()
            NSEPyData.init_ = True
        instance = super(NSEPyData, cls).__new__(cls, *args, **kwargs)
        return instance

    def __init__(self):
        pass

    @staticmethod
    def get_symbol_list(symbol_type: str = 'stock') -> pd.DataFrame:
        """
        Return pandas data frame with list of symbols
        symbol type {'stock', 'index'}
        :param symbol_type:
        :return: for symbol type 'stock' return data frame with index as symbol and name column
        """
        NSEPyData()
        if symbol_type == 'stock':
            return pd.DataFrame.from_dict(NSEPyData.nse.get_stock_codes(),
                                          orient='index',
                                          columns=['Names']).iloc[1:, :]
        elif symbol_type == 'index':
            return pd.DataFrame({'Codes': NSEPyData.nse.get_index_list()})
        else:
            raise KeyError("Select the correct symbol type")

    @staticmethod
    def get_index_constituents(index_name: str) -> pd.DataFrame:
        """
        Returns the pandas dataframe with list of constituents of index on the recent re-balancing date.
        :param index_name: str - use get_symbol_list to view index names. Currently working on only broader market index.
        :return: Returns the pandas dataframe with list of constituents of index on the recent re-balancing date.
        """
        index_formatted = ''.join(index_name.split()).lower()
        index_path = broader_indices_path.format(index_formatted)
        return ws.read_csv_from_web_as_df(index_path)

    @staticmethod
    def historical_stock_close_price(symbol: str,
                                     start_date: dt.date,
                                     end_date: dt.date = dt.date.today()) -> pd.DataFrame:
        """

        :param symbol:
        :param start_date:
        :param end_date:
        :return:
        """
        NSEPyData()
        return NSEPyData.nsepy.get_history(symbol,
                                           start_date,
                                           end_date)

    @staticmethod
    def historical_index_close_levels(symbol: str,
                                      start_date: dt.date,
                                      end_date: dt.date = dt.date.today()) -> pd.DataFrame:
        """

        :param symbol:
        :param start_date:
        :param end_date:
        :return:
        """
        NSEPyData()
        return NSEPyData.nsepy.get_history(symbol,
                                           start_date,
                                           end_date,
                                           index=True)