class EdflowException(Exception):

    def __init__(self, message=""):
        self.message = message if message else 'Some Exception Occured'
        super().__init__(message)

    def __str__(self):
        return str(self.message)


class FieldRequiredException(EdflowException):

    def __init__(self, message=""):
        super().__init__(message)


class EmailExistException(EdflowException):

    def __init__(self, message=""):
        super().__init__(message)


class WrongCredentialsException(EdflowException):

    def __int__(self, message=""):
        super().__init__(message)


class EmailNotVerifiedException(EdflowException):

    def __int__(self, message=""):
        super().__init__(message)


class UnauthorizedException(EdflowException):

    def __init__(self, message=""):
        super().__init__(message)
