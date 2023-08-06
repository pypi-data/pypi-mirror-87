from .compute_fund_daily_collection import FundDailyCollectionProcessor
from .compute_index_daily_collection import IndexDailyCollectionProcessor
from .compute_aic_daily_collection import AICDailyCollectionProcessor

class ViewDataProcessor(object):
    def __init__(self):
        self.fund_daily_collection_processor = FundDailyCollectionProcessor()
        self.index_daily_collection_processor = IndexDailyCollectionProcessor()
        self.aic_daily_collection_processor = AICDailyCollectionProcessor()

    def process_all(self, start_date, end_date):
        failed_tasks = []

        failed_tasks.extend(self.fund_daily_collection_processor.process())
        failed_tasks.extend(self.index_daily_collection_processor.process())
        failed_tasks.extend(self.aic_daily_collection_processor.process())

        return failed_tasks
