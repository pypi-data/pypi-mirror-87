""" openhiven.py related Exceptions """


__all__ = (
        'HivenException', 'HivenConnectionError', 'Forbidden',
        
        'Forbidden', 'FaultyInitialization', 'InvalidClientType',
        'InvalidToken', 'UnableToClose', 'NoneClientType',
            
        'GatewayException', 'WSConnectionError', 'HTTPError',
        'UnableToCreateSession', 'HTTPFaultyResponse', 'HTTPRequestError',
        
        'CommandException')


class HivenException(Exception):
    """`openhivenpy.exception.HivenException`

    Base Exception in the openhivenpy library!
    
    All other exceptions inherit from this base class
    
    """
    def __init__(self, *args):
        if args:
            self.msg = "".join([str(arg) for arg in args])
        else:
            self.msg = f"{self.__name__}, Exception occurred in the package openhivenpy"
            
        super().__init__(self.msg)     
        
    def __str__(self):
        return self.msg

    def __call__(self):
        return self.__class__.__name__


class HivenConnectionError(HivenException):
    """`openhivenpy.exception.HivenConnectionError`
    
    The connection to Hiven failed to be kept alive or started!
    
    """
    def __init__(self, *args):
        if args:
            arg = "".join([str(arg) for arg in args])
        else:
            arg = "The connection to Hiven failed to be kept alive or started!"
        super().__init__(arg)


class Forbidden(HivenException):
    """`openhivenpy.exception.Forbidden`

    The client was forbidden to execute a certain task or function
    
    """
    def __init__(self, *args):
        if args:
            arg = "".join([str(arg) for arg in args])
        else:
            arg = "The client was forbidden to execute a certain task or function!"
        super().__init__(arg)


class FaultyInitialization(HivenException):
    """`openhivenpy.exception.FaultyInitialization`
    
    The object was not initialized correctly and values were faulty passed or are entirely missing!
    
    """
    def __init__(self, *args):
        if args:
            arg = "".join([str(arg) for arg in args])
        else:
            arg = "The object was not initialized correctly and values were faulty passed or are entirely missing!"
        super().__init__(arg)


class InvalidClientType(HivenException):
    """`openhivenpy.exception.InvalidClientType`
    
    Invalid client type was passed resulting in a failed initialization!
    
    """
    def __init__(self, *args):
        if args:
            arg = "".join([str(arg) for arg in args])
        else:
            arg = "Invalid client type was passed resulting in a failed initialization!"
        super().__init__(arg)


class InvalidToken(HivenException):
    """`openhivenpy.exception.InvalidToken`
    
    Invalid Token was passed!
    
    """
    def __init__(self, *args):
        if args:
            arg = "".join([str(arg) for arg in args])
        else:
            arg = "Invalid Token was passed!"
        super().__init__(arg)


class GatewayException(HivenConnectionError):
    """`openhivenpy.exception.GatewayException`
       
    General Exception in the Websocket!
    
    """
    def __init__(self, *args):
        if args:
            arg = "".join([str(arg) for arg in args])
        else:
            arg = "Exception occurred in the running Websocket!"
        super().__init__(arg)


class HTTPError(HivenConnectionError):
    """`openhivenpy.exception.HTTPError`
       
    Base Exception for exceptions in the HTTPClient and overall requesting
    
    """    
    def __init__(self, code="Unknown", *args):
        if args:
            arg = "".join([str(arg) for arg in args])
        else:
            arg = f"Failed to process HTTP request! Code: {code}"
        super().__init__(arg) 


class HTTPRequestError(HTTPError):
    """`openhivenpy.exception.HTTPRequestError`
       
    General Exception while handling requests
    
    """    
    def __init__(self, *args):
        if args:
            arg = "".join([str(arg) for arg in args])
        else:
            arg = f"Request failed due to an exceptions occurring while handling!"
        super().__init__(arg) 


class HTTPFaultyResponse(HTTPError):
    """`openhivenpy.exception.HTTPRequestError`
       
    Response was in wrong format or expected data was not received
    
    """    
    def __init__(self, *args):
        if args:
            arg = "".join([str(arg) for arg in args])
        else:
            arg = f"Response was in wrong format or expected data was not received!"
        super().__init__(arg)


class UnableToCreateSession(HTTPError):
    """`openhivenpy.exception.UnableToCreateSession`
       
    Was unable to create HTTPClient session and request init client data!
    
    """    
    def __init__(self, *args):
        if args:
            arg = "".join([str(arg) for arg in args])
        else:
            arg = f"Was unable to create HTTPClient session and request init client data!"
        super().__init__(arg)


class UnableToClose(GatewayException):
    """`openhivenpy.exception.UnableToClose`
    
    The client is unable to close the connection to Hiven!
    
    """
    def __init__(self, *args):
        if args:
            arg = "".join([str(arg) for arg in args])
        else:
            arg = "The client is unable to close the connection to Hiven!"
        super().__init__(arg)


class WSConnectionError(GatewayException):
    """`openhivenpy.exception.WSConnectionError`
    
    An Exception occurred while trying to establish/keep the connection alive to Hiven!
    
    """
    def __init__(self, *args):
        if args:
            arg = "".join([str(arg) for arg in args])
        else:
            arg = "The Websocket was unable to establish/keep the connection alive to Hiven!"
        super().__init__(arg)


class NoneClientType(Warning):
    """`openhivenpy.exception.NoneClientType`
    
    A None Type was passed in the Initialization!
    
    """    
    def __init__(self, *args):
        if args:
            msg = "".join([str(arg) for arg in args])
        else:
            msg = "A None Type was passed in the Initialization!"
        super().__init__(msg)
        
# Command Exceptions #


class CommandException(HivenException):
    """`openhivenpy.exception.CommandException`
    
    General Exception while executing a command function on Hiven!
    
    """
    def __init__(self, *args):
        if args:
            arg = str(args[0]) + "".join([str(arg) for arg in args])
        else:
            arg = "An Exception occurred while executing a command function on Hiven!"
        super().__init__(arg)
