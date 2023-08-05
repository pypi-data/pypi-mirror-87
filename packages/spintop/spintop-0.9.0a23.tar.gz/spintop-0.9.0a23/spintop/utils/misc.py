import re
import socket
from contextlib import closing

from dateutil.tz import tzlocal
import pytz
from datetime import datetime

from collections.abc import Mapping
from contextlib import contextmanager
import cProfile, pstats, io

import yaml

try:
    import numpy as np
    isnan = np.isnan
except ImportError:
    isnan = lambda x: x is None

def utcnow_aware():
    dt = datetime.utcnow()
    return dt.replace(tzinfo=pytz.utc)

def is_aware(dt):
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None

PYTHON_IDENTIFIER = re.compile('^[A-Za-z_][A-Za-z0-9_]*$')
def is_valid_py_identifier(str):
    return bool(PYTHON_IDENTIFIER.search(str))

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def load_yaml_file(filename):
    with open(filename,'r') as readfile:
        data = readfile.read()
        return yaml.safe_load(data)
    
def write_yaml_file(filename, content):
    with open(filename,'w+') as writefile:
        yaml.dump(content, writefile)

def local_tz():
    return tzlocal()

def repr_obj(obj, attributes):
    attributes_str = ", ".join([f'{attr}={getattr(obj, attr)}' for attr in attributes])
    return f'{type(obj).__name__}({attributes_str})'

@contextmanager
def profiling(output_filename):
    pr = cProfile.Profile()
    pr.enable()
    try:
        yield
    finally:
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        with open(output_filename, 'w+') as profile_stream:
            ps = pstats.Stats(pr, stream=profile_stream).sort_stats(sortby)
            ps.print_stats()
            
class classproperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)

