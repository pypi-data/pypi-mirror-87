import os
import itertools
from functools import wraps

from spintop.errors import SpintopException
from spintop.utils import AnonymousGetRecursive


from pymongo import UpdateOne, MongoClient, ASCENDING, DESCENDING
from pymongo.errors import BulkWriteError

from .queryset import MongoQuery

def db_from_mongo_uri(uri, database_name):
    client = MongoClient(uri)
    return client[database_name]

class DuplicateKeyError(SpintopException):
    def __init__(self, unique_fields):
        super().__init__(f'Feature {unique_fields} is not unique.')

def parse_write_error(raw_details):
    if raw_details.get('code') == 11000:
        return DuplicateKeyError(raw_details.get('keyValue'))
    else:
        return SpintopException(str(raw_details))

class MongoOperations(object):
    def __init__(self, mongo_collection, grouped_by=None):
        self.ops = mongo_collection
        self.grouped_by = grouped_by
        
    def count(self, query, grouped_by=None):
        grouped_by = self._grouped_by_or_default(grouped_by)
        query_dict = MongoQuery(query).build()
        distinct_values = set()
        for doc in self.ops.find(query_dict, projection=[grouped_by], batch_size=5000):
            gettable_doc = AnonymousGetRecursive(doc)
            distinct_values.add(gettable_doc.get_recursive(grouped_by))
        return len(distinct_values)

    def count_total(self, query):
        return self.count(query, grouped_by='_id')

    def find(self, query, limit_range=None):
        query_dict = MongoQuery(query).build()
        pipeline = self._grouped_by_test_uuid_pipeline(query_dict)

        if limit_range:
            pipeline += [
                {"$skip": limit_range[0]},
                {"$limit": limit_range[1] - limit_range[0]}
            ]

        all_grouped = self.ops.aggregate(pipeline, allowDiskUse=True)
        return itertools.chain.from_iterable(grouped.get('documents', []) for grouped in all_grouped)

    def _grouped_by_or_default(self, grouped_by):
        if grouped_by is None:
            grouped_by = self.grouped_by if self.grouped_by else '_id'
        return grouped_by

    def _grouped_by_test_uuid_pipeline(self, query_dict, grouped_by=None):
        grouped_by = self._grouped_by_or_default(grouped_by)
        return [
            { "$match": query_dict },
            { "$group": {
                "_id": f"${grouped_by}",
                "documents": { "$push":  "$$ROOT" }
            }},
            { "$sort": {'_id': 1}}
        ]
        
    def insert_many(self, objs):
        try:
            return self.ops.insert_many(objs)
        except BulkWriteError as all_errors:
            errors = [parse_write_error(e) for e in all_errors.details.get('writeErrors', [])]

            if len(errors) == 1:
                raise errors[0]
            elif len(errors) > 1:
                messages = ['Multiple write errors occured'] + [str(e) for e in errors]
                raise SpintopException('\n'.join(messages))
            else:
                # Weird...
                raise
            
    
    def update_many(self, objs, obj_query=lambda obj: {'_id': obj['_id']}):
        updates = [
            UpdateOne(obj_query(obj), {'$set': obj, '$inc': {'version': 1}}, upsert=True) for obj in objs
        ]
        return self.ops.bulk_write(updates)
    
    def delete_many(self, query):
        query_dict = MongoQuery(query).build()
        return self.ops.delete_many(query_dict)
        
    def create_index(self, fields_and_direction, unique=False):
        self.ops.create_index(fields_and_direction, unique=unique)

    def collection_stats(self):
        return self.ops.database.command('collstats', self.ops.name)