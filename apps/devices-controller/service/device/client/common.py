'''
Common datastructures
'''

from dataclasses import dataclass

@dataclass
class DeviceID:
    provider: str
    protocol: str
    address: str


@dataclass
class DeviceMeta:
    kind: str
    model: str
    serialnum: str
