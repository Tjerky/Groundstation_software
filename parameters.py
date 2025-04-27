from enum import Enum
from pathlib import Path

groundstation_location = (51.446, 5.485, 0)
interval = 120 # seconds
microstep = 20000 # amount of steps per full rotation
update_time = 1 # in days

tle_data_file = Path('./tle_data/tle.txt')
satellites_file = Path('./tle_data/satellites.txt')

class Direction(Enum):
    AZ = 1
    EL = 2
