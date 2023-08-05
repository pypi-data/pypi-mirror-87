'''
Module for Singer literals and helpers.
'''
_PREFIX = '_sdc_'
RECEIVED_AT =      _PREFIX + 'received_at'
BATCHED_AT =       _PREFIX + 'batched_at'
SEQUENCE =         _PREFIX + 'sequence'
TABLE_VERSION =    _PREFIX + 'table_version'
PK =               _PREFIX + 'primary_key'
SOURCE_PK_PREFIX = _PREFIX + 'source_key_'
LEVEL_FMT =        _PREFIX + 'level_{}_id'
VALUE =            _PREFIX + 'value'


def parse_message_dict(obj):
    """Parse a message string into a Message object."""
    import singer
    import ciso8601

    from singer.messages import _required_key
    
    # We are not using Decimals for parsing here.
    # We recognize that exposes data to potentially
    # lossy conversions.  However, this will affect
    # very few data points and we have chosen to
    # leave conversion as is for now.
    msg_type = _required_key(obj, 'type')
    
    if msg_type == 'RECORD':
        time_extracted = obj.get('time_extracted')
        if time_extracted:
            try:
                time_extracted = ciso8601.parse_datetime(time_extracted)
            except:
                LOGGER.warning("unable to parse time_extracted with ciso8601 library")
                time_extracted = None


            # time_extracted = dateutil.parser.parse(time_extracted)
        return singer.RecordMessage(stream=_required_key(obj, 'stream'),
                             record=_required_key(obj, 'record'),
                             version=obj.get('version'),
                             time_extracted=time_extracted)


    elif msg_type == 'SCHEMA':
        return singer.SchemaMessage(stream=_required_key(obj, 'stream'),
                             schema=_required_key(obj, 'schema'),
                             key_properties=_required_key(obj, 'key_properties'),
                             bookmark_properties=obj.get('bookmark_properties'))

    elif msg_type == 'STATE':
        return singer.StateMessage(value=_required_key(obj, 'value'))

    elif msg_type == 'ACTIVATE_VERSION':
        return singer.ActivateVersionMessage(stream=_required_key(obj, 'stream'),
                                      version=_required_key(obj, 'version'))
    else:
        return None