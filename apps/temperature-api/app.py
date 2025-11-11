'''
Temperature sensor emulator
'''

from datetime import datetime
from random import random
from dataclasses import dataclass

from fastapi import FastAPI
from pydantic import BaseModel, field_serializer
import rfc3339


app = FastAPI()


@dataclass
class Location:
    t_low: int
    t_high: int
    sensor_id: str
    name: str

    @property
    def temperature(self) -> float:
        return round(random() * (self.t_high - self.t_low) + self.t_low, 2)


LOCATIONS = [
    Location(name='Living Room', t_low=18, t_high=25, sensor_id='1'),
    Location(name='Bedroom', t_low=20, t_high=24, sensor_id='2'),
    Location(name='Kitchen', t_low=22, t_high=26, sensor_id='3'),
    Location(name='Unknown', t_low=-35, t_high=35, sensor_id='0')
]


class TemperatureResponse(BaseModel):
    value: float
    unit: str
    timestamp: datetime
    location: str
    status: str
    sensor_id: str
    sensor_type: str
    description: str

    @field_serializer('timestamp', when_used='json')
    def timestamp_serializer(self, timestamp: datetime):
        return rfc3339.rfc3339(timestamp)



@app.get("/temperature")
def location_temperature(location: str):
    for place in LOCATIONS:
        if place.name == location:
            break
    return TemperatureResponse(
        value=place.temperature,
        unit='C',
        location=place.name,
        timestamp=datetime.now(),
        status='active',
        sensor_id=place.sensor_id,
        sensor_type='temperature',
        description='Temperatures sensor in ' + location
    )


@app.get("/temperature/{sensor_id}")
def sensor_temperature(sensor_id: str):
    for place in LOCATIONS:
        if place.sensor_id == sensor_id:
            break
    return TemperatureResponse(
        value=place.temperature,
        unit='C',
        location=place.name,
        timestamp=datetime.now(),
        status='active',
        sensor_id=place.sensor_id,
        sensor_type='temperature',
        description='Temperatures sensor in ' + place.name
    )
