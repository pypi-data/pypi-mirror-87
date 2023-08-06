class ResponseErrorException(Exception):
    def __init__(self, status_code, msg):
        self.status_code = status_code
        self.msg = msg


class UnauthorizedException(Exception):
    pass


class TooManyRequestsException(Exception):
    pass


class ApiKeyNotFoundException(Exception):
    pass


class InvalidDateFormatException(Exception):
    def __init__(self, msg):
        self.msg = msg

