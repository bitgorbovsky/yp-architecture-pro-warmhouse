'''
Basic class for pseudoclients
'''
from abc import ABC, abstractmethod
from typing import Dict
from service.device.client.common import DeviceID
from service.device.client.device_emu import DeviceEmulator
from service.models.device_meta import DeviceMeta
from service.models.device_state import DeviceState
from service.device.client.exceptions import NotSupportedDevice, DeviceConflict


class BaseDeviceClient(ABC):
    @classmethod
    @abstractmethod
    def supported_devices() -> Dict[str, DeviceEmulator.__class__]:
        pass

    def __init__(self):
        self.__supported_devices = self.supported_devices()
        self.__emulators: Dict[DeviceID, DeviceEmulator] = {}

    def new_device_emulator(self, device_id: DeviceID, meta: DeviceMeta):
        emulator_class = self.__supported_devices.get(meta.kind)
        if emulator_class is None:
            raise NotSupportedDevice("this type of device is not supported by "
                                     "provider for chosen protocol")

        if device_id in self.__emulators:
            raise DeviceConflict("device is already run")

        emulator = emulator_class()
        self.__emulators[device_id] = emulator
        return emulator

    def device_emulator(self, device_id: DeviceID):
        return self.__emulators.get(device_id)

    def dispose_device_emulator(self, device_id: DeviceID):
        try:
            return self.__emulators.pop(device_id)
        except KeyError:
            return

    async def init(self, device_id: DeviceID, meta: DeviceMeta) -> DeviceState:
        emu = self.new_device_emulator(device_id, meta)
        emu.start()
        return emu.state()

    async def state(self, device_id: DeviceID) -> DeviceState:
        emu = self.device_emulator(device_id)
        if not emu:
            return

        return emu.state()

    async def apply(self, device_id: DeviceID, state: DeviceState) -> bool:
        emu = self.device_emulator(device_id)
        if not emu:
            return False

        return emu.apply(state)

    async def stop(self, device_id: DeviceID) -> bool:
        emu = self.dispose_device_emulator(device_id)
        if not emu:
            return False

        return emu.stop()

    def onChange(callback):
        pass
