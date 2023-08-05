from google.cloud import bigquery

from spintop.models import get_serializer
from spintop.services.bigquery.target_bigquery import emit_state, TargetBigQuery
from spintop.utils import repr_obj, utcnow_aware

from .base import AbstractSingerTarget, SingerMessagesFactory, REQUEST_ID
from .models import BigQueryAnalyticsResponse

class BigQuerySingerTarget(AbstractSingerTarget):
    add_null_to_fields = False

    def __init__(self, project_id, dataset_id, job_project_id=None, validate_records=False, truncate=False):
        super().__init__()
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.validate_records = validate_records
        self.truncate = truncate
        
        self.target_bigquery = TargetBigQuery.from_project_dataset_id(project_id=project_id, dataset_id=dataset_id, job_project_id=job_project_id)
        self.target_bigquery.try_create_dataset()

    def send_messages_dict(self, messages, request_id=None, stream_name=None):
        state = self.target_bigquery.persist_messages_job(messages, truncate=self.truncate, validate_records=self.validate_records)
        emit_state(state)
        return BigQueryAnalyticsResponse(
            count = len(messages),
            request_id = request_id,
            stream_name = stream_name,
            project_id = self.project_id,
            dataset_id = self.dataset_id
        )

    def __repr__(self):
        return repr_obj(self, ['project_id', 'dataset_id'])

class BigQueryAnalytics(BigQuerySingerTarget):
    def __init__(self, spintop_api=None, uri=None, database_name=None, env=None):
        try:
            job_project_id = env['GOOGLE_CLOUD_PROJECT']
        except KeyError:
            job_project_id = None
            
        super().__init__(project_id=uri, dataset_id=database_name, job_project_id=job_project_id)
        self._client = None

def query_analytics_response(resp, deserialize=True, client=None):
    if client is None:
        client = bigquery.Client()

    query = f"""
    SELECT * FROM `{resp.project_id}.{resp.dataset_id}.{resp.stream_name}` WHERE {REQUEST_ID}='{resp.request_id}'
    """
    query_job = client.query(query)  # Make an API request.
    
    records = list(dict(record) for record in query_job)

    if deserialize:
        records = [get_serializer('tabular').deserialize(r, partial=True) for r in records]

    return records