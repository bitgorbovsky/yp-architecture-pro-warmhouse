'''
Device Communicator
'''

from service.device.client.warmhouse.http import WarmHouseHTTPClient
from service.device.client.warmhouse.mqtt import WarmHouseMQTTClient
from service.device.client.common import DeviceID
from service.device.client.exceptions import NotSupportedProtocol, NotSupportedProvider


__clients = {
    'warmhouse': {
        'http': WarmHouseHTTPClient(),
        'mqtt': WarmHouseMQTTClient()
    }
}


def communicate_with(device_id: DeviceID):
    provider = __clients.get(device_id.provider)
    if not provider:
        raise NotSupportedProvider(f'provider {device_id.provider} is not supported')

    client = __clients.get(device_id.protocol)
    if not client:
        raise NotSupportedProtocol(f'provider {device_id.provider} does not support'
                                   f'protoctol {device_id.protocol}')

    return client
