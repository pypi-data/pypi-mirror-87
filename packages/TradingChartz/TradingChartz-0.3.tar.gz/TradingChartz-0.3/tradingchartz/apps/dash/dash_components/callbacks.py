# external standard
import pandas as pd
import os, tradingchartz


from typing import Any, List, Tuple
from pandas_datareader import get_data_yahoo as data

# dash imports
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

# internal imports
import tradingchartz.apps.dash.helpers.helper_functions as hf
import tradingchartz.apps.dash.dash_components.charts_and_tables as cts
from tradingchartz.src.signal_and_indicators import SignalGenerator


def register_main_page_callbacks(app: Any) -> Any:

    @app.callback(
        Output('selected-stock-dropdown', 'options'),
        [
            Input('selected-universe-dropdown', 'value'),
        ]
    )
    def set_stock_selection_list(universe_symbol: str):
        file_path = os.path.join(tradingchartz.__path__[0], 'data', 'NIFTY50_constituents.csv')
        index_constituents = pd.read_csv(file_path)
        stock_options = [{'label': row['Company Name'],
                          'value': row['Symbol']} for _, row in index_constituents.iterrows()]
        return stock_options

    @app.callback(
        [
            Output('stock-ohlcv-data', 'data'),
            Output('chart-underlying-header', 'children')
        ],
        [
            Input('selected-stock-dropdown', 'value'),
            Input('selected-stock-dropdown', 'options'),
            Input('stock-data-date-range', 'start_date'),
            Input('stock-data-date-range', 'end_date')
        ]
    )
    def fetch_price_data(stock_symbol: str,
                         stock_mapping: str,
                         start_date: str,
                         end_date: str) -> Tuple:
        if (start_date is None) or (end_date is None) or (stock_symbol is None) or (stock_mapping is None):
            raise PreventUpdate
        # start_date = hf.string_to_date(start_date)
        # end_date = hf.string_to_date(end_date)
        df = data(stock_symbol+'.NS', start_date, end_date)
        df = df.round(2)
        # df = NSEPyData.historical_stock_close_price(stock_symbol, start_date, end_date)
        stock_name = [mapping['label'] for mapping in stock_mapping if mapping['value'] == stock_symbol]
        chart_header_msg = f"{stock_name[0]} - {stock_symbol}"
        return df.to_json(orient='index', date_format='iso'), chart_header_msg

    @app.callback(
        Output('stock-pattern-data', 'data'),
        [
            Input('stock-ohlcv-data', 'data'),
            Input('selected-candle-pattern-dropdown', 'value')
        ]
    )
    def calculate_pattern_signals(stock_ohlcv_data: str,
                                  pattern_list: List) -> str:
        if not stock_ohlcv_data:
            raise PreventUpdate
        stock_ohlcv_df = hf.df_from_jason(stock_ohlcv_data)
        empty_json = pd.DataFrame().to_json(orient='index')
        if pattern_list is None:
            return empty_json
        sg = SignalGenerator(stock_ohlcv_df)
        _pattern_sr_dict = {}
        for pattern in pattern_list:
            try:
                _pattern_sr_dict[pattern] = sg.raw_candle_pattern(pattern)
            except:
                pass
        if not _pattern_sr_dict:
            return empty_json
        pattern_df = pd.concat(_pattern_sr_dict.values(), axis=1, keys=_pattern_sr_dict.keys())
        return pattern_df.to_json(orient='index', date_format='iso')

    @app.callback(
        Output('stock-ohlc-chart', 'figure'),
        [
            Input('selected-stock-dropdown', 'value'),
            Input('stock-ohlcv-data', 'data'),
            Input('stock-pattern-data', 'data')
        ]
    )
    def generate_ohlc_graph(stock_name: str,
                            stock_ohlcv_data: str,
                            stock_pattern_data: str) -> go.Figure():
        stock_ohlcv_df = hf.df_from_jason(stock_ohlcv_data)
        stock_pattern_df = hf.df_from_jason(stock_pattern_data)
        fig = go.Figure()
        fig = cts.generate_ohlc_graph(fig, stock_ohlcv_df)
        if not stock_pattern_df.empty:
            fig = cts.add_signals_to_chart(fig, stock_pattern_df, stock_ohlcv_df)
        fig.update_xaxes(type='category')
        return fig

    @app.callback(
        [Output(f"collapse-triple-barrier", "is_open")],
        [Input(f"collapse-triple-toggle", "n_clicks")],
        [State(f"collapse-triple-barrier", "is_open")],
    )
    def toggle_accordion(n1, is_open1):
        ctx = dash.callback_context

        if not ctx.triggered:
            return (False,)
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "collapse-triple-toggle" and n1:
            return (not is_open1,)
        return (False,)
