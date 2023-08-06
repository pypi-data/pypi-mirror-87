# define base exception
# copyright (c) 2020 cisco Systems Inc., ALl rights reserved
# @author rks@cisco.com
class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidProjectFileException(Error):
    """Raised when the input project file is invalid """
    pass


class InvalidAttributeException(Error):
    """Raised when an invalid attribute is specified """

    def __init__(self, building):
        super()
        self.__building__ = building


class InvalidOperationException(Error):
    """Raised when an invalid operation is performed """

    def __init__(self, err):
        super()
        self.__error__ = err
