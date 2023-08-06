
class CiscoMELoginError(Exception):
    """When an invalid login is detected."""

    def __init__(self, message):
        self.message = message

    pass


class CiscoMEConfigError(Exception):
    """When an invalid config is attempted."""

    def __init__(self, message):
        self.message = message

    pass


class CiscoMEPageNotFoundError(Exception):
    """When a 404 happens."""

    def __init__(self, message):
        self.message = message

    pass


class CiscoMEUnknownError(Exception):
    """When a general unknown exception happens."""

    pass
