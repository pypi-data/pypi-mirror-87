import logging

CORE_LOGGER = logging.getLogger('sptp.deploy')

def _logger(name):
    return CORE_LOGGER.getChild(name)