'''
Devices API implementation
'''

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from service.apis.default_api_base import BaseDefaultApi
from service.repository import devices


class DevicesAPI(BaseDefaultApi):
    async def v1_get_all_devices(self):
        return await devices.select()

    async def v1_get_devices_of_provider(self, provider):
        return await devices.select(provider=provider)

    async def v1_get_devices_of_provider_and_protocol(self, provider, protocol):
        return await devices.select(provider=provider, protocol=protocol)

    async def v1_get_device_info(self, provider, protocol, address):
        device = await devices.get(provider, protocol, address)
        if not device:
            return JSONResponse(status_code=404, content={
                'message': 'no device with such identifier',
                'code': 404
            })

        return device

    async def v1_register_device(self, provider, protocol, device):
        try:
            return await devices.new(provider, protocol, device)
        except devices.InvalidDeviceData:
            return JSONResponse(
                status_code=400,
                content={"message": "incorrect device data"}
            )
        except devices.DeviceConflict:
            return JSONResponse(
                status_code=409,
                content={"message": "device with such identifiers exists"}
            )

    async def v1_update_device_info(self, provider, protocol, address, device_update):
        updated = await devices.update(provider, protocol, address, device_update)
        if not updated:
            return JSONResponse(status_code=404, content={
                'message': 'no device with such identifier',
                'code': 404
            })

        return updated

    async def v1_unregister_device(self, provider, protocol, address):
        ok = await devices.delete(provider, protocol, address)
        if ok:
            return JSONResponse(
                status_code=200,
                content={"message": "device deleted"}
            )
        return JSONResponse(
            status_code=404,
            content={"message": "not found"}
        )
