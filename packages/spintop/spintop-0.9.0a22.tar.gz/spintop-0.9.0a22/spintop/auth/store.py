import os
from .schemas import credentials_schema

from spintop.utils import write_yaml_file, load_yaml_file

class CredentialsStore(object):
    def store(self, credentials):
        raise NotImplementedError()

    def retrieve(self):
        raise NotImplementedError()
    
    def delete(self):
        raise NotImplementedError()

class InMemoryCredentialsStore(object):
    def __init__(self):
        self.credentials = None

    def store(self, credentials):
        self.credentials = credentials

    def retrieve(self):
        return self.credentials
    
    def delete(self):
        self.credentials = None

class FilePathCredentialsStore(object):
    def __init__(self, credentials_filepath): # Do not change param name for module compat
        self.filepath = credentials_filepath

    def store(self, credentials):
        credentials = credentials_schema.dump(credentials)
        write_yaml_file(self.filepath, credentials)

    def retrieve(self):
        try:
            content = load_yaml_file(self.filepath)
        except FileNotFoundError:
            return None
        else:
            return credentials_schema.load(content)
    
    def delete(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)