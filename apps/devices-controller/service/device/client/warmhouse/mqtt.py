'''
WarmHouse MQTT Client
'''

from service.device.client.base_client import BaseDeviceClient
from service.device.client.device_emu import DeviceEmulator
from service.device.client.exceptions import WrongDeviceStateException
from service.models.device_state import DeviceState
from service.models.feature import Feature


class BulbEmulator(DeviceEmulator):
    def start(self):
        self.__switch = False
        self.__color = 'ffffff'

    def state(self) -> DeviceState:
        ts = int(datetime.now().timestamp())
        return DeviceState(
            status='online',
            timestamp=ts,
            features={
                'switch': Feature(
                    type='switch',
                    unit='on,off',
                    timestamp=ts,
                    value='on' if self.__switch else 'off'
                ),
                'color': Feature(
                    type='color',
                    unit='rgb',
                    timestamp=ts,
                    value=self.__color
                )
            }
        )

    def apply(self, state: DeviceState) -> bool:
        changed = False
        if 'switch' in state.features:
            value = state.features['switch'].value
            if value == 'on':
                self.__switch = True
            elif value == 'off':
                self.__switch = False
            else:
                raise WrongDeviceStateException('wrong value for feature "switch"')
            changed = True

        if 'color' in state.features:
            self.__color = state.features['color'].value
            changed = True

        if not changed:
            raise WrongDeviceStateException('wrong features requested')

        return changed

    def stop(self):
        return True


class LockEmulator:
    def start(self):
        self.__locked = False

    def state(self) -> DeviceState:
        ts = int(datetime.now().timestamp())
        return DeviceState(
            status='online',
            timestamp=ts,
            features={
                'lock': Feature(
                    type='switch',
                    unit='close,open',
                    timestamp=ts,
                    value='open' if self.__locked else 'close'
                )
            }
        )

    def apply(self, state: DeviceState) -> bool:
        changed = False
        if 'switch' in state.features:
            value = state.features['switch'].value
            if value == 'close':
                self.__locked = True
            elif value == 'open':
                self.__locked = False
            else:
                raise WrongDeviceStateException('wrong value for feature "switch"')
            changed = True

        if not changed:
            raise WrongDeviceStateException('wrong features requested')

        return changed

    def stop(self):
        return True


class WarmHouseMQTTClient(BaseDeviceClient):
    _supported_devices = {
        'bulb': BulbEmulator,
        'lock': LockEmulator
    }
