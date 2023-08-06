class BaseError(Exception):
    """
    Attributes:
        response_content: Response content from logic monitor
        response_status: Response status code. Basically HTTP status code
        msg: Error message
    """

    def __init__(
            self,
            response_content: str,
            response_status: int,
            msg: str
    ):
        self.response_content = response_content
        self.response_status = response_status
        self.msg = msg

    def __repr__(self):
        return f'{self.__class__.__name__}({self.msg})'

    def __str__(self):
        return self.__repr__()


class ResponseNotOkError(BaseError):
    pass


class SBError(BaseError):
    """ South bound call error """
    pass


class SBTimeoutError(BaseError):
    """ South bound timeout error """
    pass


class SBCancelledError(BaseError):
    """ South bound cancelled error """
    pass


class FactoryResetFailedError(BaseError):
    """ Factory reset failed """
    pass


class ACSDeleteError(Exception):
    """ Failed to delete from ACS """
    pass


class CPENotFoundError(Exception):
    """ If CPE not found on ACS """
    pass
