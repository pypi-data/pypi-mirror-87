from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union

from spintop.models import PersistenceRecord, PersistenceIDRecord, BaseDataClass

class SpintopEnvMessage(BaseDataClass):
    env: Optional[Dict[str, Optional[Any]]]

    def create_message_env(self, local_env):
        """Create a copy of the local env with the attributes contained in this message"""
        env = self.env
        if env is None:
            env = {}
        return local_env.copy(**env)

    @classmethod
    def from_message(cls, other_env_message, **kwargs):
        obj = cls(env=other_env_message.env, **kwargs)
        return obj

class PersistenceRecordMessage(SpintopEnvMessage):
    record: Optional[PersistenceRecord]

class PersistenceRecordsUpdateMessage(SpintopEnvMessage):
    updated_ids: List[PersistenceIDRecord]
    update_all: bool = False

    def merge(self, other):
        return self.__class__(
            env=self.env,
            update_all=self.update_all or other.update_all,
            updated_ids=self.updated_ids + other.updated_ids
        )

    @classmethod
    def create(cls, **kwargs):
        defaults = dict(
            updated_ids = [],
            update_all = False,
            env = None
        )
        defaults.update(kwargs)
        return cls(**defaults)
