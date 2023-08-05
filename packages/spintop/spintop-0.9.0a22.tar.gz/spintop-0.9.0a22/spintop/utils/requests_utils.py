import uuid
import requests
import platform

from spintop import __version__

def spintop_session(user_agent=f'SPINTOP/{__version__} HOST/{platform.node()} MACHINEID/{uuid.getnode()}'):
    session = requests.Session()
    session.headers.update({'User-Agent': user_agent})
    return session