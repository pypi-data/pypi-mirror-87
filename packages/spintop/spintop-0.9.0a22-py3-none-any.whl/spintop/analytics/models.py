from spintop.models import BaseDataClass

class AnalyticsResponse(BaseDataClass):
    count: int = 0
    request_id: str = None
    stream_name: str = None

class BigQueryAnalyticsResponse(AnalyticsResponse):
    project_id: str = None
    dataset_id: str = None

    def query(self, deserialize=True):
        # import here to not require bigquery unless imported.
        from .bigquery import query_analytics_response
        return list(query_analytics_response(self, deserialize=deserialize))