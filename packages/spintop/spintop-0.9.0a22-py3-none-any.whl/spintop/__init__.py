import pkgutil
res = pkgutil.get_data('spintop', 'VERSION')
__version__ = res.decode().strip()

from .env import Spintop
