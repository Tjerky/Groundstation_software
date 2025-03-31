from stepper_control import make_step
from time import time

def trace_path(path, current_pos, t_end, microstep, make_step):
    t = time()

    degrees_per_step = 360/microstep

    while t < t_end:
        t = time()
        dangle = path(t) - current_pos

        if abs(dangle) > degrees_per_step:
            make_step(dangle/abs(dangle))

            current_pos += degrees_per_step*(dangle/abs(dangle))

    return current_pos

def trace_trajectory(trajectory, microstep, make_step):
    v = 0
    a = 0

    while time() < trajectory[0][0]:
        pass

    for i in range(len(trajectory) - 1):
        trace_path(trajectory[i][1], trajectory[i][1], trajectory[i+1][0], microstep, make_step)

if __name__ == '__main__':
    steps = []
    def make_step(direction):
        steps.append([time(), direction])

    from find_trajectory import generate_next_trajectory

    trajectory = generate_next_trajectory('Delfi-N3xt', 1)

    print(trajectory)

    trace_trajectory(trajectory, 10000, make_step)

    print(steps)




