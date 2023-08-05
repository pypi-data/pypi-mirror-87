class UserError(Exception):
    """Base error class for errors which can be handled by the end user

    This is for error messages addressed to the end user.
    Errors which should be handled internally shall not be raised
    as this type of error.
    Use it only when you are sure it is has a end user readable message.
    All other errors should cause an ordinary traceback such that the
    cause can be debugged by the developers"""
