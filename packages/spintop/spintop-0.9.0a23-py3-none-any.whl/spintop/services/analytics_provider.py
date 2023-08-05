
from spintop.analytics.bigquery import AdvancedBigQueryAnalytics

class BigQueryAnalyticsProvider(object):
    def __init__(self, env, project_id):
        self.project_id = project_id
        self.env = env

    def analytics_target_factory(self, database_name, namespace=None):
        if namespace is None:
            namespace = self.project_id
        return AdvancedBigQueryAnalytics(uri=namespace, database_name=database_name, env=self.env)
