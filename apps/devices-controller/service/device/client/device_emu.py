'''
Abstract base class for device emulator
'''

from abc import abstractmethod, ABC

from service.models.device_state import DeviceState


class DeviceEmulator(ABC):
    @abstractmethod
    def start(self):
        '''
        Device state initialization
        '''

    @abstractmethod
    def state(self) -> DeviceState:
        '''
        This methods returns state of device in terms of features
        '''

    @abstractmethod
    def apply(self, state: DeviceState) -> bool:
        '''
        This method applies a new state to device and returns
        boolean flag if it was successful or not.
        Throws WrongDeviceState exception if device is not manageable
        '''

    @abstractmethod
    def stop(self) -> bool:
        '''
        Just to show idea that communcation with device
        should be finished properly, with closing acquired
        resources and so on.
        '''
