import pandas as pd

from ...util.singleton import Singleton
from ..wrapper.mysql import ViewDatabaseConnector
from ..view.view_models import *


class ViewDataApi(metaclass=Singleton):
    @staticmethod
    def get_fund_daily_collection():
        with ViewDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(FundDailyCollection)
                df = pd.read_sql(query.statement, query.session.bind)
                df = df.rename(columns=FundDailyCollection.trans_columns())
                return df
            except Exception as e:
                print(e)
                return False

    @staticmethod
    def get_daily_index_collection():
        with ViewDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(IndexDailyCollection)
                df = pd.read_sql(query.statement, query.session.bind)
                df = df.rename(columns=IndexDailyCollection.trans_columns())
                return df
            except Exception as e:
                print(e)
                return False

    @staticmethod
    def get_daily_fund_automatic_investment():
        with ViewDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(AutomaticInvestmentCollection)
                df = pd.read_sql(query.statement, query.session.bind)
                df = df.rename(columns=AutomaticInvestmentCollection.trans_columns())
                return df
            except Exception as e:
                print(e)
                return False

