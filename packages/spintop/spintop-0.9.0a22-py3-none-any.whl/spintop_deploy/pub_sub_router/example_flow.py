from random import random

from prefect import task, Flow, case, Parameter
from prefect.tasks.control_flow import merge

from spintop_deploy.pub_sub_router.handlers import BigQueryJobHandler, GCSFileChangeHandler
from spintop_deploy.pub_sub_router.messages import BigQueryAuditLogMessage, GCSFileReferenceMessage


@BigQueryJobHandler.task()
def on_bq_message(message: BigQueryAuditLogMessage):
    return "This is a BQ message."

@GCSFileChangeHandler.task()
def on_gcs_file(message: GCSFileReferenceMessage):
    return "This is a gcs file."

with Flow("handle-message") as flow:
    message = Parameter('message')
    
    on_bq_message(message)
    on_gcs_file(message)