class jpeError(Exception):
    pass

class calculationError(jpeError):
    pass

class modeError(jpeError):
    """
when a function or operation has multiple modes this error is caled if an invalid mode was passed
    """
    pass
