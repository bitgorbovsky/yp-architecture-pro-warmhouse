'''
Common datastructures
'''

from dataclasses import dataclass

@dataclass(frozen=True, eq=True)
class DeviceID:
    provider: str
    protocol: str
    address: str
