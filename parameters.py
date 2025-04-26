from enum import Enum

groundstation_location = (51.446, 5.485, 0)
interval = 120 # seconds
microstep = 20000 # amount of steps per full rotation
update_time = 1 # in days

class Direction(Enum):
    AZ = 1
    EL = 2
