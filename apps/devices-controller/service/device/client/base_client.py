'''
Basic class for pseudoclients
'''

from service.device.client.common import DeviceID, DeviceMeta
from service.models.device_state import DeviceState
from service.device.client.device_emu import DeviceEmulator


class BaseDeviceClient:
    _supported_devices = {}
    __emulators: Dict[DeviceID, DeviceEmulator] = {}

    @classmethod
    def new_device_emulator(cls, device_id: DeviceID):
        emulator_class = cls.__emulators[device_id]
        emulator = emulator_class()
        self.__emulators[device_id] = emulator
        return emulator

    @classmethod
    def device_emulator(cls, device_id: DeviceID):
        return self.__emulators.get(device_id)

    @classmethod
    def dispose_device_emulator(cls, device_id: DeviceID):
        try:
            return self.__emulators.pop(device_id)
        except KeyError:
            return

    async def init(self, device_id: DeviceID, meta: DeviceMeta) -> DeviceState:
        emu = self.new_device_emulator(device_id)
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
