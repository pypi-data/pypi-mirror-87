from functools import lru_cache

from spintop.analytics.bigquery import BigQueryAnalytics
from .analytics_functions import create_dataset_functions

@lru_cache(100)
def _cached_create_dataset_functions(analytics):
    return create_dataset_functions(analytics)

class AdvancedBigQueryAnalytics(BigQueryAnalytics):

    @property
    def functions(self):
        # Cache so that self.functions always return the same object.
        return _cached_create_dataset_functions(self)