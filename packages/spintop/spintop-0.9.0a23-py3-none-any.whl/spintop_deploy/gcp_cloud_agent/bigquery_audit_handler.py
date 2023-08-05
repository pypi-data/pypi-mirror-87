from google.cloud import bigquery

from spintop_deploy.pub_sub_router import BigQueryJobHandler, BigQueryAuditLogMessage, PubSubRouter
from spintop.models.serialization import get_json_serializer

def bigquery_audit_handler(spintop_client, bq_client=None):
    
    if bq_client is None:
        bq_client = bigquery.Client()

    serializer = get_json_serializer()
    @BigQueryJobHandler
    def handle_bq_message(message: BigQueryAuditLogMessage):
        if message.table_id == 'spintop_metadata':
            table_identifier = f'`{message.project_id}`.`{message.dataset_id}`.`{message.table_id}`'
            metadata_result = bq_client.query(f'SELECT * FROM {table_identifier}').result()
            metadata = None

            for index, row in enumerate(metadata_result):
                # Only one row expected.
                if index > 0:
                    raise ValueError(f'Metadata returned more rows than expected (1)')

                metadata = dict(row)
            
            if not metadata:
                raise ValueError('Unable to retrieve metadata (no rows returned)')

            metadata = serializer.serialize(metadata)
            spintop_client.update_spintop_metadata(metadata)

            return True
        else:
            return False

    router = PubSubRouter([handle_bq_message])
    return router.request_handler()
