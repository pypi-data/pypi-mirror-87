import os
import random
import datetime as dt
import pandas as pd


from dateutil.relativedelta import relativedelta
from typing import Optional, List


def run_daily_data(run_date: dt.date = dt.date.today(),
                   ticker_list: Optional = None,
                   candle_pattern_list: Optional = None,
                   sl_min: float = .02,
                   sl_max: float = .1) -> pd.DataFrame:

    import talib
    import numpy as np
    from pandas_datareader import get_data_yahoo as data

    end_date = run_date.strftime('%Y-%m-%d')
    start_date = (run_date - relativedelta(months=2)).strftime('%Y-%m-%d')

    index_constituents = pd.read_csv(os.path.join(os.path.dirname(__file__), '../../data/NIFTY500_constituents.csv'))
    final_df = pd.DataFrame()
    ticker_fail_list = []

    if ticker_list is None:
        ticker_list = index_constituents.Symbol
    if candle_pattern_list is None:
        candle_pattern_list = talib.get_function_groups()['Pattern Recognition']

    data_check = data(random.choice(ticker_list) + '.NS', end_date, end_date).round(2)
    if data_check.empty:
        raise ValueError("data for run_date not available")

    for ticker in ticker_list:
        try:
            df_price_data = data(ticker + '.NS', start_date, end_date).round(2)
        except:
            ticker_fail_list.append(ticker)
            continue
        value_check = df_price_data.Close.iloc[-20:].isnull().values.any()
        if value_check or df_price_data.empty:
            continue
        print(ticker)
        df_price_data.dropna(how='any', inplace=True)
        open = df_price_data['Open']
        high = df_price_data['High']
        low = df_price_data['Low']
        close = df_price_data['Close']
        volume = df_price_data['Volume']

        macd, _, macdhist = talib.MACD(close, fastperiod=5, slowperiod=10, signalperiod=3)
        macd.rename('macd', inplace=True)
        macdhist.rename('macdhist', inplace=True)
        macd_final = pd.concat([macd, macdhist], axis=1)
        macd_final['Ticker'] = ticker
        macd_final['macd_crossover'] = np.where(macd_final['macd']/macd_final['macd'].shift(1) < 0, 1, 0)
        macd_final['macd_crossover7d'] = macd_final['macd_crossover'].shift(1).rolling(7).sum()
        macd_final['macdhist_crossover'] = np.where(macd_final['macdhist']/macd_final['macdhist'].shift(1) < 0, 1, 0)
        macd_final['macdhist_crossover7d'] = macd_final['macdhist_crossover'].shift(1).rolling(7).sum()
        macd_final['macdhist_trend'] = np.where(macd_final['macdhist'] < 0, 1, 0)
        macd_final['macd_trend'] = np.where(macd_final['macd'] < 0, 1, 0)

        vol_5_day = volume.rolling(5).mean()

        for candle_pattern in candle_pattern_list:

            signal_sr = getattr(talib, candle_pattern)(df_price_data[f"Open"],
                                                       df_price_data[f"High"],
                                                       df_price_data[f"Low"],
                                                       df_price_data[f"Close"])
            if signal_sr.empty:
                continue
            for n in range(1):
                try:
                    index = ticker + candle_pattern + signal_sr.index[-1-n].strftime('%Y-%m-%d')
                    final_df.loc[index, 'date'] = signal_sr.index[-1-n]
                    final_df.loc[index, 'pattern'] = candle_pattern
                    final_df.loc[index, 'ticker'] = ticker
                    final_df.loc[index, 'signal'] = signal_sr.values[-1-n]
                    final_df.loc[index, 'Open'] = df_price_data["Open"].iloc[-1-n]
                    final_df.loc[index, 'High'] = df_price_data[f"High"].iloc[-1-n]
                    final_df.loc[index, 'Low'] = df_price_data[f"Low"].iloc[-1-n]
                    final_df.loc[index, 'Close'] = df_price_data[f"Close"].iloc[-1-n]
                    final_df.loc[index, 'Stop-Loss'] = round(max(min(df_price_data[f"Low"].iloc[-1-n],
                                                                     df_price_data[f"Low"].iloc[-2-n],
                                                                     round((1-sl_min) * df_price_data[f"Close"].iloc[-1-n])),
                                                                 (1 - sl_max) * df_price_data[f"Close"].iloc[-1-n]),
                                                             2)
                    final_df.loc[index, 'Take-Profit'] = round(((3 * df_price_data[f"Close"].iloc[-1-n])
                                                                - (2 * final_df.loc[index, 'Stop-Loss'])),
                                                               2)
                    final_df.loc[index, 'macd_crossover'] = macd_final.iloc[-1-n, :]['macd_crossover']
                    final_df.loc[index, 'macd_crossover7d'] = macd_final.iloc[-1-n, :]['macd_crossover7d']
                    final_df.loc[index, 'macdhist_crossover'] = macd_final.iloc[-1-n, :]['macdhist_crossover']
                    final_df.loc[index, 'macdhist_crossover7d'] = macd_final.iloc[-1-n, :]['macdhist_crossover7d']
                    final_df.loc[index, 'macd_trend'] = macd_final.iloc[-1-n, :]['macd_trend']
                    final_df.loc[index, 'macdhist_trend'] = macd_final.iloc[-1-n, :]['macdhist_trend']
                    final_df.loc[index, '5d_vol_criteria'] = (volume.iloc[-1-n] > vol_5_day.iloc[-2-n])
                except:
                    pass
                    ticker_fail_list.append(ticker)
            final_df = final_df[final_df['signal'] != 0]

    final_df_non_zero = final_df[final_df['signal'] != 0]
    print("Failed - Ticker", set(ticker_fail_list))
    return final_df_non_zero.reset_index(drop=True)


if __name__ == "__main__":
    run_date = dt.date.today()
    daily_data = run_daily_data(run_date=dt.date(2020, 12, 7))
    daily_data.to_csv(f'../../../daily_run_{run_date}.csv', index=False)
