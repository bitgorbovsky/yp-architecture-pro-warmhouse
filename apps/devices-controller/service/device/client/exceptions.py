'''
Device Exceptions
'''


class DeviceException(Exception):
    '''
    Base class for all exceptions thrown by operations with devices.
    '''


class WrongDeviceStateException(DeviceException):
    '''
    This exceptions is being thrown by operations changinng device state.
    '''


class NotSupportedProvider(DeviceException):
    '''
    This exception is being thrown by operations where requested provider is
    not supported
    '''


class NotSupportedProtocol(DeviceException):
    '''
    This exception is being thrown by operations where requested protocol is
    not supported
    '''
