import re
from collections.abc import Sequence

class MongoQuery():
    def __init__(self, model_query_or_queries):
        if not isinstance(model_query_or_queries, Sequence):
            model_query_or_queries = [model_query_or_queries]

        self.orig_queries = model_query_or_queries

    def build(self):
        if len(self.orig_queries) == 1:
            return self.build_one_query(self.orig_queries[0])
        else:
            return {"$or": [self.build_one_query(q) for q in self.orig_queries]}

    def build_one_query(self, orig_query):
        query = {}

        if orig_query is None:
            return query

        for key, value in orig_query.value_equals.items():
            query[key] = value
        
        for key, value in orig_query.list_contains.items():
            raise NotImplementedError()

        for key, list_of_values in orig_query.value_equals_one_of.items():
            query[key] = q_any_in_list(list_of_values)
        
        return query
    
def q_any_in_list(_list):
    return {'$in': _list}