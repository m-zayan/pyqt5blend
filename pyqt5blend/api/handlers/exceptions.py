__all__ = ['InvalidConfigurations', 'CoreGraphicsAPIError']


class InvalidConfigurations(Exception):

    def __init__(self, message):

        super().__init__(message)


class CoreGraphicsAPIError(Exception):

    def __init__(self, message):

        super().__init__(message)
