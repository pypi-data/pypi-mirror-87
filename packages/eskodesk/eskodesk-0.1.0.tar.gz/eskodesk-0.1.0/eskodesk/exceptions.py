class EskodeskException(Exception):
    pass


class EskodeskObjectAlreadyCreated(EskodeskException, ValueError):
    pass


class EskodeskClientError(EskodeskException):
    """
    Wrapper for 4xx errors
    """

    pass


class EskodeskBadRequest(EskodeskClientError):
    pass


class EskodeskBadCredentials(EskodeskClientError):
    pass


class EskodeskObjectNotFound(EskodeskClientError):
    pass


class EskodeskServerError(EskodeskException):
    """
    Wrapper for 5xx errors
    """

    pass


class EskodeskTimeout(EskodeskException):
    pass


class EskodeskConnectTimeout(EskodeskTimeout):
    pass


class EskodeskReadTimeout(EskodeskTimeout):
    pass
