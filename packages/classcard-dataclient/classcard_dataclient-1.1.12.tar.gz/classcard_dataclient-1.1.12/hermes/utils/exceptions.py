class ValidateError(Exception):
    def __init__(self, message):
        self.message = message


class RequestError(Exception):
    def __init__(self, message, code=None):
        self.message = message
        self.code = code
