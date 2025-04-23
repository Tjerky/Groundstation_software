from stepper_control import make_step
from time import time
from logger import get_logger
from parameters import *

logger = get_logger()

def trace_path(path, current_pos, t_end, microstep, make_step, dir):
    t = time()

    degrees_per_step = 360/microstep

    while t < t_end:
        #TODO
        logger.info(f"Current position ({dir.name}) - {current_pos * degrees_per_step}")

        t = time()
        dangle = path(t) - current_pos

        if abs(dangle) > degrees_per_step:
            make_step(dangle/abs(dangle)) # why?

            current_pos += degrees_per_step*(dangle/abs(dangle))

    return current_pos

def trace_trajectory(trajectory, microstep, make_step, dir):
    v = 0
    a = 0

    current_pos = trajectory[0][1](trajectory[0][0])

    while time() < trajectory[0][0]:
        pass

    for i in range(len(trajectory) - 1):
        current_pos = trace_path(trajectory[i][1], current_pos, trajectory[i+1][0], microstep, make_step, dir)

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

    from find_trajectory import generate_next_trajectory

    trajectory = generate_next_trajectory('Delfi-N3xt', 1)

    print(trajectory)

    trace_trajectory(trajectory, 10000, make_step)

    print(steps)




