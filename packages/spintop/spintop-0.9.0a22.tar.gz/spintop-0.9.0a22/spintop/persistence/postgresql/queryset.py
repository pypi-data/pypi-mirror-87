import re
from sqlalchemy import or_, and_

from spintop.models.persistence import PersistenceIDRecord
from spintop.utils import AnonymousGetRecursive

from .models import top_level_fields

top_level_fields_names = {field.name_ for field in top_level_fields}

class PostgreSQLQuery(object):
    def __init__(self, query):
        self.orig_query = query

    def build_data_query(self, record_table):
        queries = []

        for key, value in self.orig_query.value_equals.items():
            # data is stored as test_record: 
            if key in top_level_fields_names:
                queries.append(getattr(record_table, key) == value)
            else:
                field = self._get_index_field(record_table, key)
                if isinstance(value, re.Pattern):
                    queries.append(field.astext.op("~")(value.pattern))
                elif isinstance(value, bool):
                    # False -> false
                    queries.append(field.astext == str(value).lower())
                else:
                    queries.append(field.astext == str(value))
        
        for key, value in self.orig_query.list_contains.items():
            raise NotImplementedError()

        for key, list_of_values in self.orig_query.value_equals_one_of.items():
            if key in top_level_fields_names:
                queries.append(getattr(record_table, key).in_(list_of_values))
            else:
                field = self._get_index_field(record_table, key)
                queries.append(field.astext.in_(list_of_values))

        return queries

    def _get_index_field(self, record_table, field_name):
        field = AnonymousGetRecursive(record_table.index)
        return field.get_recursive(field_name)