'''
Warmhouse HTTP Client
'''

from datetime import datetime
from random import random
from typing import Dict

from service.device.client.base_client import BaseDeviceClient
from service.device.client.device_emu import DeviceEmulator
from service.device.client.exceptions import WrongDeviceStateException
from service.models.device_state import DeviceState
from service.models.feature import Feature


class TemperatureSensorEmulator(DeviceEmulator):
    def start(self):
        pass

    def state(self) -> DeviceState:
        ts = int(datetime.now().timestamp())
        return DeviceState(
            status='online',
            timestamp=ts,
            features={
                'temperature': Feature(
                    type='float',
                    unit='celsium',
                    timestamp=ts,
                    value=round(random() * 70 - 35, 2)
                )
            }
        )

    def apply(self, state: DeviceState) -> bool:
        raise WrongDeviceStateException('this kind of device is not manageable')

    def stop(self):
        return True


class ThermostatEmulator(DeviceEmulator):
    def start(self):
        self.target_temperature = 22
        self.updated_at = int(datetime.now().timestamp())

    def state(self) -> DeviceState:
        return DeviceState(
            status='online',
            timestamp=ts,
            features={
                'temperature': Feature(
                    type='float',
                    unit='celsium',
                    timestamp=ts,
                    value=round(random() * 70 - 35, 2)
                ),
                'thermostat': Feature(
                    type='float',
                    unit='celsium',
                    timestamp=ts,
                    value=self.target_temperature
                )
            }
        )

    def apply(self, state: DeviceState) -> bool:
        if 'thermostat' not in state.features:
            raise WrongDeviceStateException("incorrect feature manupilation")
        self.target_temperature = state.features['thermostat'].value
        self.updated_at = int(datetime.now().timestamp())
        return True

    def stop(self):
        return True


class WarmHouseHTTPClient(BaseDeviceClient):
    @classmethod
    def supported_devices(cls):
        return {
            'temperature': TemperatureSensorEmulator,
            'thermostat': ThermostatEmulator
        }
