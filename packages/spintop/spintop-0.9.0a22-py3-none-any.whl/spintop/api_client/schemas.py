from marshmallow import Schema, fields

class ManyRecordsSchema(Schema):
    records = fields.List(fields.Dict())
    
class RecordsCountSchema(Schema):
    count = fields.Int()
    
class TokenSchema(Schema):
    token = fields.String()

class DashboardSchema(Schema):
    base_url = fields.String()
    url = fields.String()
    name = fields.String()
    sharing_token = fields.String()
    sharing_secret = fields.String()

class TopicSchema(Schema):
    key = fields.String()
    name = fields.String()
    path = fields.String()

records_schema = ManyRecordsSchema()
record_count_schema = RecordsCountSchema()
token_schema = TokenSchema()

dashboards_schema = DashboardSchema(many=True)
topics_schema = TopicSchema(many=True)

