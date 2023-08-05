from datetime import datetime

from spintop.persistence.base import PersistenceFacade

from ..models import PersistenceRecordCollection, Query, get_json_serializer, SerializedPersistenceRecord

from .schemas import records_schema, record_count_schema

from ..logs import _logger

logger = _logger('spintop-api.records')

class SpintopAPIPersistenceFacade(PersistenceFacade):
    def __init__(self, spintop_api=None, uri=None, database_name=None, message_publisher=None, env=None, **unused):
        
        if spintop_api is None:
            spintop_api = default_spintop_api(env, uri, database_name)

        self.spintop_api = spintop_api
        self.serializer = get_json_serializer()
        spintop_api.register_persistence_facade(self)
        super().__init__(self.serializer, messages=message_publisher)

    @property
    def session(self):
        return self.spintop_api.session

    def _create(self, records):
        logger.debug(f'Creating records at {self.spintop_api.api_url}')
        serialized = self._records_in_schema(records)
        return self.session.post(self.spintop_api.get_link('records.create'), json=serialized)
        
    def _records_in_schema(self, records):
        return records_schema.dump({'records': [record.as_dict() for record in records]})

    def _retrieve(self, query, limit_range=None, with_data=True):
        logger.debug(f'Retrieving records from {self.spintop_api.api_url}')
        if limit_range is None:
            limit_range = (0,500)
        query_dict = query.as_dict()
        if limit_range:
            query_dict['limit_range_inf'] = limit_range[0]
            query_dict['limit_range_sup'] = limit_range[1]
            
        query_dict['with_data'] = with_data

        resp = self.session.post(self.spintop_api.get_link('records.search'), json=query_dict)
        records = records_schema.load(resp.json())['records']
        return (SerializedPersistenceRecord(record) for record in records)
        
    def _count(self, query):
        query_dict = query.as_dict()
        resp = self.session.post(self.spintop_api.get_link('records.count'), json=query_dict)
        return record_count_schema.load(resp.json())['count']

    def _update(self, records):
        logger.debug(f'Updating records at {self.spintop_api.api_url}')
        serialized = self._records_in_schema(records)
        return self.session.put(self.spintop_api.get_link('records.update'), json=serialized)
    
    def _delete(self, query):
        logger.debug(f'Deleting records from {self.spintop_api.api_url}')
        query_dict = query.as_dict()
        return self.session.delete(self.spintop_api.get_link('records.delete'), json=query_dict)
        
    def __str__(self):
        return f'{self.__class__.__name__}(url={self.spintop_api.api_url})'

def default_spintop_api(env, uri=None, database_name=None):
    if uri is not None and database_name is not None:
        return env.spintop_factory(org_id=database_name)
    else:
        raise ValueError('uri + database_name parameters are required.')