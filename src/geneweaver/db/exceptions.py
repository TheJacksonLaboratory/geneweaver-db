from geneweaver.core.exc import GeneweaverError


class GeneweaverTypeError(GeneweaverError):
    """Exception raised when a type error occurs."""

    pass


class GeneweaverValueError(GeneweaverError):
    """Exception raised when a value error occurs."""

    pass
