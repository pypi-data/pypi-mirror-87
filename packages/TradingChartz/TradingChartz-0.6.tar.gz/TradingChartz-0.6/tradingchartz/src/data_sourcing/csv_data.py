# external standard
import pandas as pd
from typing import List


class BBGcsvData:

    HEADERS = ['Open', 'High', 'Low', 'Close', 'Vol']

    def __init__(self, file_path):
        self._file_path = file_path
        self.refresh_flag = True
        self._available_tickers = None
        self._raw_data = None

    @property
    def raw_data(self):
        if self.refresh_flag:
            self._raw_data = pd.read_csv(self.file_path, index_col='Date')
            self._raw_data.sort_index(inplace=True)
            self._available_tickers = list({col_name.split("_")[0] for col_name in self._raw_data.columns})
            self.refresh_flag = False
        return self._raw_data

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, path):
        self.refresh_flag = True
        self._file_path = path

    @property
    def available_tickers(self) -> List:
        if (self._available_tickers is None) or self.refresh_flag:
            self._available_tickers = list({col_name.split("_")[0] for col_name in self.raw_data.columns})
        return self._available_tickers

    def get_OHLCv_data(self, ticker: str) -> pd.DataFrame:
        ohlcv_df = self.raw_data[[f"{ticker}_{field}" for field in self.HEADERS]]
        ohlcv_df.dropna(how='any', inplace=True)
        ohlcv_df.columns = self.HEADERS
        return ohlcv_df




