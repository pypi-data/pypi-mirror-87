import prefect
import time

from concurrent.futures import ThreadPoolExecutor

from prefect.cli.execute import _execute_flow_run
from prefect.utilities.graphql import GraphQLResult
from prefect.environments.storage import GCS, S3, Azure, Local, GitHub, GitLab, Webhook
from prefect.serialization.storage import StorageSchema

class ServerlessAgent(prefect.agent.local.LocalAgent):
    def __init__(self, *args, **kwargs):
        kwargs['max_polls'] = kwargs.get('max_polls', 3)
        kwargs['hostname_label'] = False
        super().__init__(*args, **kwargs)

    def trigger_flow_id(self, flow_id, **kwargs):
        self.client.create_flow_run(flow_id=flow_id, **kwargs)

    def run_flow_id(self, flow_id, **kwargs):
        self.trigger_flow_id(flow_id, **kwargs)
        self.run_once()

    def run_once(self):
        self.client.attach_headers({"X-PREFECT-AGENT-ID": self._register_agent()})

        with ThreadPoolExecutor(max_workers=1) as executor:
            flow_executed = self.agent_process(executor)
            if not flow_executed:
                time.sleep(2)
                flow_executed = self.agent_process(executor)
            
            if not flow_executed:
                raise RuntimeError('Flow did not execute.')

    def deploy_flow(self, flow_run: GraphQLResult) -> str:
        """
        Deploy flow runs on your local machine as Docker containers

        Args:
            - flow_run (GraphQLResult): A GraphQLResult flow run object

        Returns:
            - str: Information about the deployment

        Raises:
            - ValueError: if deployment attempted on unsupported Storage type
        """
        self.logger.info("Deploying flow run {}".format(flow_run.id))  # type: ignore

        if not isinstance(
            StorageSchema().load(flow_run.flow.storage),
            (Local, Azure, GCS, S3, GitHub, GitLab, Webhook),
        ):
            self.logger.error(
                "Storage for flow run {} is not a supported type.".format(flow_run.id)
            )
            raise ValueError("Unsupported Storage type")

        prefect.context.flow_run_id = flow_run.id
        prefect.context.flow_id = flow_run.flow.id
        prefect.config.logging.log_to_cloud = str(self.log_to_cloud).lower()
        prefect.config.engine.flow_runner.default_class = "prefect.engine.cloud.CloudFlowRunner"
        prefect.config.engine.task_runner.default_class = "prefect.engine.cloud.CloudTaskRunner"

        _execute_flow_run()

        return "OK"