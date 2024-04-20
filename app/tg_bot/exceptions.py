class BaseException(Exception):
    """Base exception class."""
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        if self.message:
            return f"{self.__class__.__name__}: {self.message}"
        return f"{self.__class__.__name__}"

#====== API Exceptions ======

class ConnectionToEndpointError(BaseException):
    """Exception if we get error when try to get response."""


class ResponseDictError(BaseException):
    """Exception if we get non-dict response."""


class SendMessageError(BaseException):
    """
    Exception if we got an error 
    when try to send message to user.
    """


class DeserializationError(BaseException):
    """
    Exception if we got an error 
    when converting response.
    """


class CallbackQueryAnswerError(BaseException):
    """
    Exception if we got an error 
    when try to answer on query.
    """


class SendMessageError(BaseException):
    """
    Exception if we got an error 
    when try to send message.
    """


class ChangeMediaMessageError(BaseException):
    """
    Exception if we got an error when 
    try to change media message.
    """

#====== Database Exceptions ======

class CreateUserError(BaseException):
    """
    Exception if we got an error 
    when try to create user in database.
    """

class UpdateMessagesCountError(BaseException):
    """
    Exception if we got an error when try to 
    update user messages count database.
    """

class UpdateNavMovesCountError(BaseException):
    """
    Exception if we got error when try to 
    update nav_moves_count in database.
    """