"""Exceptions for the geneweaver db module."""
from geneweaver.core.exc import GeneweaverError


class GeneweaverTypeError(GeneweaverError):
    """Exception raised when a type error occurs."""

    pass


class GeneweaverValueError(GeneweaverError):
    """Exception raised when a value error occurs."""

    pass


class GeneweaverDoesNotExistError(GeneweaverError):
    """Exception raised when an object does not exist."""

    pass
