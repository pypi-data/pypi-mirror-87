from spintop.analytics import AbstractSingerTarget, AnalyticsResponse
from spintop.models import get_json_serializer
from spintop.persistence.base import PersistenceFacade

from .persistence_facade import default_spintop_api

class SpintopAPIAnalytics(AbstractSingerTarget):
    
    def __init__(self, spintop_api=None, uri=None, database_name=None, env=None):
        super().__init__()

        if spintop_api is None:
            spintop_api = default_spintop_api(env, uri, database_name)

        self.spintop_api = spintop_api
        spintop_api.register_analytics(self)
        self.serializer = get_json_serializer()

    @property
    def session(self):
        return self.spintop_api.session

    def send_messages(self, messages_str, request_id=None, stream_name=None):
        return self._stream_named_analytics_endpoint('analytics.stream_update', messages_str, request_id=request_id, stream_name=stream_name)

    def update_named_stream(self, name, raw_data, stream_type=None):
        data = self.serializer.serialize_barrier(raw_data, validate=True)
        endpoint_name = f'analytics.{name}_update'
        return self._stream_named_analytics_endpoint(endpoint_name, data)

    def _stream_named_analytics_endpoint(self, endpoint_name, data, request_id=None, stream_name=None):
        response_data = self.session.put(self.spintop_api.get_link(endpoint_name), json=data).json()
        response = self.serializer.deserialize(response_data)
        return self.complete_response(response, request_id=request_id, stream_name=stream_name)