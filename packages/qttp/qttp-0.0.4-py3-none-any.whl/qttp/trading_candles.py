from qttp.tools.date_interval import DateInterval
from qttp.tools.date import HunDate
from qttp.tools.time_span import time_span
from qttp.tools.log import setup_custom_logger

from datetime import datetime, timedelta
import pandas as pd
import requests
import time
import os


pd.set_option('mode.chained_assignment',  None) # turn off the warning

logger = setup_custom_logger("Candles")

hun_date = HunDate()

class Candles:
    def save_file_name(self, exchange, since, span, base):
        exchange = exchange
        market   = self.market
        start    = since
        end      = self.today
        span     = span
        base     = base
        path = 'candles/'

        if not os.path.isdir(path):
            os.mkdir(path)

        file_name = f'{exchange}_{market}_{start}_{end}_{span}_{base}.csv'
        return path + file_name

    # def request_candle(self, exchange, unit, since):
    #     url, path, params = self.__url_path_params(exchange, unit, since)
    #     page = requests.get(url + path, params=params)
    #     return page.json()
    #
    # def __url_path_params(self, exchange, unit, since):
    #     if exchange == "upbit":
    #         url = "https://api.upbit.com"
    #         if unit == "1D":
    #             path = "/v1/candles/minutes/days"
    #         else:
    #             path = "/v1/candles/minutes/" + unit
    #         params = {
    #
    #         }
    #
    #     if exchange == "deribit":
    #          url = "https://www.deribit.com"
    #          path = "/api/v2/public/get_tradingview_chart_data"
    #          params = {
    #
    #          }
    #
    #     if exchange == "bybit":
    #          url = "https://api.bybit.com"
    #          path = "/v2/public/kline/list"
    #          params = {
    #              "symbol" : self.market,
    #              "interval" : unit,
    #              "from" : since
    #          }
    #
    #     return url, path, params


class UpbitCandle(Candles):
    def __init__(self, market):
        self.market = market
        self.base_url = "https://api.upbit.com"

    def candle_since(self, since, span='24h', base='9h'):
        self.today = hun_date.today_plus_1day()
        to_dates = DateInterval(since, self.today, 200)[0][1]
        save_file_name = super().save_file_name('upbit', since, span, base)

        try:
            result_df = pd.read_csv(save_file_name, index_col=0, parse_dates=True)

        except FileNotFoundError:
            new_df = pd.DataFrame()
            for to_date in to_dates:
                time.sleep(0.5)
                df = self.real_time_candle_days(to_date)
                new_df = pd.concat([new_df, df])

                logger.info(f"Getting Upbit Candles, {to_date} Done")

            result_df = time_span(new_df, span=span, base=base)
            result_df.to_csv(save_file_name, index=True)

        return result_df

    def real_time_candle_days(self, date=None):
        path = "/v1/candles/days/"
        parameters = {
            "market" : self.market,
            "count" : 200
        }
        if date:
            path = "/v1/candles/minutes/60"
            parameters['to'] = date

        page = requests.get(self.base_url + path, params=parameters)
        df = pd.DataFrame(page.json())
        df = self.__preprocessing(df)
        return df

    def __preprocessing(self, df):
        columns = [
            'candle_date_time_kst',
            'opening_price',
            'high_price',
            'low_price',
            'trade_price',
            'candle_acc_trade_volume'
        ]
        df['candle_acc_trade_volume'] = round(df['candle_acc_trade_volume'], 0)
        df = df[columns]
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume' ]
        df = df.sort_values(by='date')
        df.index = df['date']
        df.drop('date', axis=1, inplace=True)
        df.index = pd.to_datetime(df.index)
        return df

class DeribitCandle(Candles):
    def __init__(self, market):
        self.market = market
        self.base_url = "https://www.deribit.com"


    def candle_since(self, since, span='24h', base='9h'):
        self.today = hun_date.today_plus_1day()
        dates = DateInterval(since, self.today, 10000)[0]
        start_dates = dates[0]
        end_dates = dates[1]

        save_file_name = super().save_file_name('deribit', since, span, base)

        try:
            result_df = pd.read_csv(save_file_name, index_col=0, parse_dates=True)

        except FileNotFoundError:
            new_df = pd.DataFrame()
            for s_date, e_date in zip(start_dates, end_dates):
                time.sleep(0.5)
                df = self.real_time_candle_days(start_date=s_date, end_date=e_date)
                new_df = pd.concat([new_df, df])

                logger.info(f"Getting Upbit Candles, {s_date}  ~ {e_date} Done")
            result_df = time_span(new_df, span=span, base=base).iloc[1:, :]
            result_df.to_csv(save_file_name, index=True)

        return result_df

    def real_time_candle_days(self, days=100, start_date=None, end_date=None):
        start_timestamp = hun_date.now_timestamp(days)
        end_timestamp = hun_date.now_timestamp()

        path = "/api/v2/public/get_tradingview_chart_data"
        parameters = {
            "instrument_name" : self.market,
            "start_timestamp" : start_timestamp,
            "end_timestamp" : end_timestamp,
            "resolution" : "1D"
        }

        if start_date:
            parameters['resolution'] = 60
            parameters['start_timestamp'] = hun_date.millisecond(start_date)
            parameters['end_timestamp'] = hun_date.millisecond(end_date)

        page = requests.get(self.base_url + path, params=parameters)
        df = pd.DataFrame(page.json()['result'])
        df = self.__preprocessing(df)

        return df


    def __preprocessing(self, df):
        df['ticks'] = pd.to_datetime(df['ticks'], unit='ms') + timedelta(hours=9)
        df.rename(columns={"ticks": "date"}, inplace=True)
        df.index = df['date']
        df = df[['open', 'high', 'low', 'close', 'volume']]
        return df

class BybitCandle(Candles):
    def __init__(self, market):
        self.market = market
        self.base_url = "https://api.bybit.com"
        # pd.set_option('display.float_format', lambda x: '%.4f' % x)

    # def candle_60m_200(self):
    #     since = hun_date.seconds(hun_date.minus_hour(200))
    #     print(since)
    #     response = self.request_candle("bybit", 60, since)
    #     print(response)
    #
    # def __preprocessing(self, df):
    #     df['open_time'] = pd.to_datetime(df['open_time'], unit='s')
    #     df['open_time'] = df['open_time'] + timedelta(hours=9)
    #     df.rename(columns={"open_time": "date"}, inplace=True)
    #     df.index = df['date']
    #     df = df[['open', 'high', 'low', 'close', 'volume']]
    #     df['volume'] = df['volume'].astype(float)
    #     return df

    def candle_since(self, since, span='24h', base='9h'):
        self.today = hun_date.today_plus_1day()
        to_dates = DateInterval(since, self.today, 200)[0][0]

        save_file_name = super().save_file_name('bybit', since, span, base)

        try:
            result_df = pd.read_csv(save_file_name, index_col=0, parse_dates=True)

        except FileNotFoundError:
            new_df = pd.DataFrame()
            for to_date in to_dates:
                time.sleep(0.5)
                df = self.__request_form(60, to_date)
                new_df = pd.concat([new_df, df])

                logger.info(f"Getting Candles, {to_date} Done")

            result_df = time_span(new_df, span=span, base=base).iloc[1:, :]
            result_df.to_csv(save_file_name, index=True)
        return result_df

    def candle_60m(self, span=None, base=None):
        since = hun_date.minus_hour(199)
        candle_60m = self.__request_form(60, since)
        if span:
            candle_60m = time_span(candle_60m, span=span, base=base)
        return candle_60m

    def candle_days(self):
        since = hun_date.minus_day(199)
        candle_days = self.__request_form("D", since)
        return candle_days

    def __request_form(self, unit, since):
        path = "/v2/public/kline/list"
        params = {
            "symbol" : self.market,
            "interval" : unit,
            "from" : hun_date.seconds(since)
        }
        page = requests.get(self.base_url + path, params=params)
        df = pd.DataFrame(page.json()['result'])
        df = self.__preprocessing(df)
        return df


    def __preprocessing(self, df):
        df['open_time'] = pd.to_datetime(df['open_time'], unit='s')
        df['open_time'] = df['open_time'] + timedelta(hours=9)
        df.rename(columns={"open_time": "date"}, inplace=True)
        df.index = df['date']
        df = df[['open', 'high', 'low', 'close', 'volume']]
        df.loc[:, 'volume'] = df['volume'].astype(int)
        return df
