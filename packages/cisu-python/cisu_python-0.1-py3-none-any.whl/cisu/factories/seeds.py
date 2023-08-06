import math

from faker import Faker
from datetime import datetime, timedelta
from random import uniform
from dataclasses import dataclass
from typing import Union, Tuple


@dataclass
class ClockSeed:
    start_date: datetime
    interval: timedelta
    factor: int = 5
    current_date: Union[None, datetime] = None

    def __post_init__(self):
        self.current_date = self.start_date

    def generate(self) -> datetime:
        self.current_date = self.start_date + (self.interval * uniform(0, self.factor))
        return self.current_date


@dataclass
class LocationSeed:
    latitude: float
    longitude: float
    height: float = 0
    factor: float = 5  # 1 km
    r_earth = 6378

    def generate(self) -> Tuple[float, float]:
        dy = self.factor * uniform(0, 1)
        dx = self.factor * uniform(0, 1)
        new_latitude = self.latitude + (dy / self.r_earth) * (180 / math.pi)
        new_longitude = self.longitude + (dx / self.r_earth) * (180 / math.pi) / math.cos(self.latitude * math.pi / 180)

        return new_latitude, new_longitude


faker = Faker(locale="fr_FR")
clock_seed = ClockSeed(datetime(2020, 1, 1), timedelta(minutes=2))
location_seed = LocationSeed(latitude=48.8811, longitude=2.5929)