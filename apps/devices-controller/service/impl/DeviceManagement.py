'''
Device Controlling API
'''
from typing import Optional

from fastapi.responses import JSONResponse

from service.apis.default_api_base import BaseDefaultApi
from service.device.client import communicate_with
from service.device.client.base_client import BaseDeviceClient
from service.device.client.common import DeviceID
from service.device.client.exceptions import (
    DeviceException,
    DeviceConflict
)
from service.models.device_meta import DeviceMeta
from service.models.device_state import DeviceState
from service.models.success_message import SuccessMessage


class DeviceManagement(BaseDefaultApi):
    async def v1_connect_device(self, provider, protocol, address, meta: DeviceMeta):
        try:
            device_id = DeviceID(
                provider=provider,
                protocol=protocol,
                address=address
            )
            client: BaseDeviceClient = communicate_with(device_id)
            return await client.init(device_id, meta)
        except DeviceConflict as e:
            return JSONResponse(status_code=409, content={
                'message': e.args[0],
                'code': 409
            })
        except DeviceException as e:
            return JSONResponse(status_code=404, content={
                'message': e.args[0],
                'code': 404
            })

    async def v1_inspect_device(self, provider, protocol, address):
        try:
            device_id = DeviceID(
                provider=provider,
                protocol=protocol,
                address=address
            )
            client: BaseDeviceClient = communicate_with(device_id)
            result: Optional[DeviceState] = await client.state(device_id)
            if result is None:
                return JSONResponse(status_code=404, content={
                    'message': 'session for this device is not found',
                    'code': 404
                })
            return result
        except DeviceException as e:
            return JSONResponse(status_code=404, content={
                'message': e.args[0],
                'code': 404
            })

    async def v1_run_device(self, provider, protocol, address, state):
        try:
            device_id = DeviceID(
                provider=provider,
                protocol=protocol,
                address=address
            )
            client: BaseDeviceClient = communicate_with(device_id)
            ok = await client.apply(device_id, state)
            if not ok:
                return JSONResponse(status_code=404, content={
                    'message': 'could not apply a new state to device, '
                               'possibly device is not connected',
                    'code': 404
                })
            return SuccessMessage(message="state applied")
        except DeviceException as e:
            return JSONResponse(status_code=404, content={
                'message': e.args[0],
                'code': 404
            })

    async def v1_disconnect_device(self, provider, protocol, address):
        try:
            device_id = DeviceID(
                provider=provider,
                protocol=protocol,
                address=address
            )
            client: BaseDeviceClient = communicate_with(device_id)
            return await client.stop(device_id)
        except DeviceException as e:
            return JSONResponse(status_code=404, content={
                'message': e.args[0],
                'code': 404
            })
