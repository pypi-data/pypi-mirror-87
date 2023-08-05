from json import dumps
from google.cloud import tasks_v2 as tasks

class GoogleCloudTaskQueue(object):
    def __init__(self, project_id, gcp_region, gcp_queue_name, impersonate_service_account=None):
        self.client = tasks.CloudTasksClient()
        self.queue_path = self.client.queue_path(project_id, gcp_region, gcp_queue_name)
        self.impersonate_service_account = impersonate_service_account

    def enqueue_http_post(self, url, json=None):
        """queue_path = projects/PROJECT_ID/location/LOCATION_ID/queues/QUEUE_ID"""
        task = {
            "http_request": {  # Specify the type of request.
                "http_method": tasks.HttpMethod.POST,
                "url": url  # The full url path that the task will be sent to.
            }
        }

        if self.impersonate_service_account:
            task["http_request"]['oidc_token'] = {"service_account_email": self.impersonate_service_account}

        if json:
            task["http_request"]["headers"] = {"Content-type": "application/json"}
            task["http_request"]["body"] = dumps(json).encode()

        response = self.client.create_task(request={"parent": self.queue_path, "task": task})
        print("Created task {}".format(response.name))