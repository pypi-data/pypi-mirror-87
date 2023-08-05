import pandas as pd
import numpy as np
import time
from typing import Optional
from .calculator import Calculator
from ...constant import FundFactorType
from ...util.singleton import Singleton

START_DATE = '2005-01-01'
END_DATE = '2020-11-05'
BUCKET_NAME = 'tl-fund-factors'

class Factor(Calculator, metaclass=Singleton):
    
    def __init__(self, f_name: str, f_type: str=FundFactorType, f_level: str='basic'):
        self.f_name = f_name
        self.s3_file_name = f'{f_name}.parquet'
        self.f_type = f_type
        self.f_level = f_level
        self.s3_uri = f's3://{BUCKET_NAME}/{self.f_level}/' + self.s3_file_name
        self.factor: Optional[pd.DataFrame] = None

    def get(self) -> Optional[pd.DataFrame]:
        if self.factor is None:
            self.load()
        return self.factor

    def save(self) -> bool:
        if self.factor is None:
            return False
        self.factor.to_parquet(self.s3_uri, compression='gzip')
        print(f' upload to s3 success {self.f_name} {self.s3_uri}')
        return True

    def load(self):
        try:
            t0 = time.time()
            self.factor: pd.DataFrame = pd.read_parquet(self.s3_uri)
            t1 = time.time()
            print(f'\t[time][{self.f_level}] fetch factor: {self.f_name} from s3 cost {round(t1 - t0, 4)}')
        except Exception as e:
            print(f'retrieve data from s3 failed, (err_msg){e}; try to re-calc {self.f_name}')
            self.calc()
        return self.factor

    def data_reindex_daily_trading_day(self, data, tradingday):
        # 日线因子交易日对齐
        td = pd.to_datetime(data.index)
        td = [i.date() for i in td]
        data.index = td
        data = data.reindex(data.index.union(tradingday.index))
        data = data.ffill().reindex(tradingday.index)
        return data

    def data_reindex_daily_trading_day_not_fill(self, data, tradingday):
        td = pd.to_datetime(data.index)
        td = [i.date() for i in td]
        data.index = td
        data = data.reindex(data.index.union(tradingday.index))
        data = data.reindex(tradingday.index)
        return data

    def data_resample_monthly_ret(self, df, rule='1M', min_count=15):
        df = df.set_axis(pd.to_datetime(df.index), inplace=False).resample(rule).sum(min_count=min_count)
        df.index = [i.date() for i in df.index]
        df.index.name = 'datetime'
        return df

    def data_resample_weekly_ret(self, df, rule='1W', min_count=3):
        df = df.set_axis(pd.to_datetime(df.index), inplace=False).resample(rule).sum(min_count=min_count)
        df.index = [i.date() for i in df.index]
        df.index.name = 'datetime'
        return df

    def data_resample_monthly_nav(self, df, rule='1M'):
        df = df.set_axis(pd.to_datetime(df.index), inplace=False).resample(rule).last()
        df.index = [i.date() for i in df.index]
        df.index.name = 'datetime'
        return df

    def data_resample_weekly_nav(self, df, rule='1W'):
        df = df.set_axis(pd.to_datetime(df.index), inplace=False).resample(rule).last()
        df.index = [i.date() for i in df.index]
        df.index.name = 'datetime'
        return df
