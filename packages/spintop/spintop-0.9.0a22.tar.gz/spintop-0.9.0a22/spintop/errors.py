import warnings

class SpintopException(Exception):
    pass

class SpintopBaseException(BaseException):
    pass

class AuthUnauthorized(SpintopException):
    pass

class ExpiredAccessToken(SpintopException):
    pass

class SpintopWarning(UserWarning):
    pass

def spintop_warn(message):
    warnings.warn(message, SpintopWarning)