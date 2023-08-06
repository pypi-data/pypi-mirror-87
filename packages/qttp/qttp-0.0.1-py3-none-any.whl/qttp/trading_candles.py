from qttp.tools.date_interval import DateInterval
from qttp.tools.date import HunDate
from qttp.tools.time_span import time_span
from qttp.tools.log import setup_custom_logger

from datetime import datetime, timedelta
import pandas as pd
import requests
import time
import os

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

class UpbitCandle(Candles):
    def __init__(self, market):
        self.market = market
        self.base_url = "https://api.upbit.com"

    def candle_since(self, since, span='24h', base='9h'):
        self.today = hun_date.today_plus_1day()
        to_dates = DateInterval(since, self.today, 200)[0][1]
        save_file_name = super().save_file_name('upbit', since, span, base)

        try:
            result_df = pd.read_csv(save_file_name, index_col=0)

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
            result_df = pd.read_csv(save_file_name, index_col=0)

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
            parameters['start_timestamp'] = hun_date.get_timestamp(start_date)
            parameters['end_timestamp'] = hun_date.get_timestamp(end_date)

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
