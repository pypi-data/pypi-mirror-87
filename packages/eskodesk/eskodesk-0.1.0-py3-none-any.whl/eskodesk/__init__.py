"""
Copyright 2020 Eskolare Negócios Digitais Ltda
"""
from eskodesk.client import Eskodesk
from eskodesk.exceptions import (
    EskodeskBadCredentials,
    EskodeskBadRequest,
    EskodeskClientError,
    EskodeskConnectTimeout,
    EskodeskException,
    EskodeskObjectAlreadyCreated,
    EskodeskObjectNotFound,
    EskodeskReadTimeout,
    EskodeskServerError,
    EskodeskTimeout,
)

VERSION = "0.1.0"

__version__ = VERSION

__all__ = [
    "Eskodesk",
    "EskodeskBadCredentials",
    "EskodeskBadRequest",
    "EskodeskClientError",
    "EskodeskConnectTimeout",
    "EskodeskException",
    "EskodeskObjectAlreadyCreated",
    "EskodeskObjectNotFound",
    "EskodeskReadTimeout",
    "EskodeskServerError",
    "EskodeskTimeout",
]
