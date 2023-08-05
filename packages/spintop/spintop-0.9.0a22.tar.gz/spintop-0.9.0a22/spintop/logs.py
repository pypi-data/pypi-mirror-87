import logging
import warnings

CORE_LOGGER = logging.getLogger('sptp')
FORMAT = '%(relativeCreated)-10d[ms] %(name)-30s:%(levelname)-5s: %(message)s'

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(logging.Formatter(FORMAT))

def _logger(name):
    return CORE_LOGGER.getChild(name)

def setup_logging(verbose=False):
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    logging.basicConfig(format=FORMAT, level=logging.WARNING)
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    CORE_LOGGER.setLevel(level)
    
    # if STREAM_HANDLER not in CORE_LOGGER.handlers:
    #     CORE_LOGGER.addHandler(STREAM_HANDLER)

def deprecated(reason):
    warnings.warn(reason, DeprecationWarning)