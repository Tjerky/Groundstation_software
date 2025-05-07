from stepper_control import make_step
from time import time
from logger import format_position
from parameters import *
from pytz import UTC
from datetime import datetime
from shared import *

def trace_path(path, current_pos, t_end, microstep, make_step, angle_direction):
    t = time()

    degrees_per_step = 360/microstep

    while t < t_end:
        t = time()
        dangle = path(t) - current_pos

        if abs(dangle) > degrees_per_step:
            make_step(dangle/abs(dangle))

            current_pos += degrees_per_step*(dangle/abs(dangle))
            
            with output_lock:
                shared_output.write(format_position(current_pos, angle_direction))

    return current_pos

def trace_trajectory(trajectory, microstep, make_step, angle_direction):

    current_pos = trajectory[0][1](trajectory[0][0])

    while time() < trajectory[0][0]:
        pass

    for i in range(len(trajectory) - 1):
        current_pos = trace_path(trajectory[i][1], current_pos, trajectory[i+1][0], microstep, make_step, angle_direction)

def generate_make_step(stepper):
    def make_step(direction):
        if stepper._direction != direction:
            stepper.set_direction_pin(direction)

        stepper.make_a_step()

    return make_step

if __name__ == '__main__':
    steps = []
    def make_step(direction):
        steps.append([time(), direction])
        print(f'{time()}')

    from find_trajectory import generate_full_trajectory

    trajectory_az, trajectory_el = generate_full_trajectory('ISS (ZARYA)', datetime.now(tz=UTC))

    print(trajectory_az)

    trace_trajectory(trajectory_az, 10000, make_step, 1)
    print(steps)

