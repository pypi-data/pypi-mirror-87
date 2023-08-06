import unittest
import datetime as dt

# internal imports
from tradingchartz.src.data_sourcing.nsepy_data import NSEPyData


class TestNSEPyData(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def test_stock_symbol_list(self) -> None:
        symbol_list = NSEPyData.get_symbol_list()
        self.assertNotEqual(symbol_list.empty, True)

    def test_index_symbol_list(self) -> None:
        symbol_list = NSEPyData.get_symbol_list('index')
        self.assertNotEqual(symbol_list.empty, True)

    def test_index_constituent_path(self) -> None:
        data_df = NSEPyData.get_index_constituents('nifty50')
        self.assertNotEqual(data_df.empty, True)

    def test_stock_historical_data(self) -> None:
        historical_data = NSEPyData.historical_stock_close_price('sbin',
                                                                 dt.date(2020, 1, 1),
                                                                 dt.date(2020, 1, 31))
        self.assertNotEqual(historical_data.empty, True)


if __name__ == '__main__':
    unittest.main()
