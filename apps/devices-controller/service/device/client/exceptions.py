'''
Device Exceptions
'''


class DeviceException(Exception):
    '''
    Base class for all exceptions thrown by operations with devices.
    '''


class DeviceConflict(DeviceException):
    '''
    Exception for various conflicts with devices:
    already connected devices, inability to change state of device, ...
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

class NotSupportedDevice(DeviceException):
    '''
    This exception is being thrown by operations when
    type of requested devices is not supported by this provder and protocol.
    '''
