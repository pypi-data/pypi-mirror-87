from typing import Optional
from collections.abc import Mapping

from .base import BaseDataClass, model_property

NO_VERSION = 'none'

class VersionIDRecord(BaseDataClass):
    id: Optional[str]
    version: Optional[str]
    
    @classmethod
    def create(cls, id_or_dict, version=None):
        if isinstance(id_or_dict, cls):
            return id_or_dict
        if isinstance(id_or_dict, Mapping):
            id = id_or_dict.get('id', None)
            version = id_or_dict.get('version', None)
        else:
            id = id_or_dict
            
        if version is None:
            version = NO_VERSION
            
        return cls(
            id=id,
            version=version
        )
        
    def match(self, other):
        id_match = self.id == other.id if self.id is not None else True
        version_match = self.version == other.version if self.version is not None else True
        return id_match and version_match

    def __str__(self):
        if self.version and self.version != NO_VERSION:
            return f'{self.id}-{self.version}'
        elif self.id:
            return str(self.id)
        else:
            return 'default'

TestbenchIDRecord = VersionIDRecord

DutIDRecord = VersionIDRecord

class OutcomeData(BaseDataClass):
    """An outcome is the result of a quality check. """

    fields_docs_ = dict(
        message="""
    A string that represents the outcome message. These should be 
    re-used as much as possible as they are extensively used as unique 
    tags to identify types of failures. The standard message is an 
    empty string.
        """,
        is_pass="""
    Whether or not the quality check passed. When a quality check
    does not exist or does not apply, this should be set to True.
        """,
        state="""
    A status that relates to the state this outcome should be associated
    with in the production line. There shouldn't be that many different 
    states in a specific production line. 
    
    The standard state, i.e. when in normal production, is an empty string. 

    Typical examples includes: 
        retry: When this failure lead to a retry of a quality check
        issue: When this failure lead to the opening of an issue.
        """
    )

    message: str = ''
    is_pass: bool = True
    state: str = ''

    @classmethod
    def fields_docstring(cls):
        return dict(
        )

    @property
    def is_skip(self):
        return self._get_bool_state_prop('skip')

    @is_skip.setter
    def is_skip(self, value):
        return self._set_bool_state_prop('skip', value)

    @property
    def is_abort(self):
        return self._get_bool_state_prop('abort')

    @is_abort.setter
    def is_abort(self, value):
        return self._set_bool_state_prop('abort', value)
        
    @property
    def is_ignore(self):
        return self._get_bool_state_prop('ignore')

    @is_ignore.setter
    def is_ignore(self, value):
        return self._set_bool_state_prop('ignore', value)

    def _get_bool_state_prop(self, state_str):
        return self.state == state_str
    
    def _set_bool_state_prop(self, state_str, value):
        if value:
            self.state = state_str
        else:
            self.state = ''

    def __bool__(self):
        return self.is_pass and not self.is_abort

    @classmethod
    def create(cls, outcome):
        if outcome is None:
            outcome = True
            
        if isinstance(outcome, cls):
            pass # already correct type
        elif isinstance(outcome, bool):
            outcome = cls(is_pass=outcome)
        elif isinstance(outcome, Mapping):
            outcome = cls(**outcome)
        else:
            raise TypeError((
    'Outcome (%s) should either be a boolean that indicates if this test passed or failed, ' 
    'or a dictionnary of one or more of the following attributes: %s'
            ) % (outcome, [f.name for f in cls.dataclass_fields()]))
        return outcome

    def impose_upon(self, other_outcome):
        if not self.is_ignore:
            # Pass propagates by falseness. False will propagate up, not True
            other_outcome.is_pass = other_outcome.is_pass and self.is_pass

            # Abort propagates by trueness. True will propagate up, not False
            other_outcome.is_abort = other_outcome.is_abort or self.is_abort

            # Abort propagates by trueness. True will propagate up, not False
            other_outcome.is_skip = other_outcome.is_skip or self.is_skip
