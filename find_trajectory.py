from pyorbital.orbital import Orbital
from datetime import datetime
from datetime import timedelta
import numpy as np
from parameters import groundstation_location

def find_next_orbit(satellite, dt, time=datetime.utcnow(), file=None):
    cube = Orbital(satellite, file)

    dt = timedelta(seconds=dt)

    underhorizon = True

    while underhorizon:
        az, el = cube.get_observer_look(time, *groundstation_location)

        underhorizon = el < 0

        time += dt

    trajectory_time = []
    trajectory_az = []
    trajectory_el = []

    while not underhorizon:
        az, el = cube.get_observer_look(time, *groundstation_location)

        # append a time, position. Time is converted to local time
        trajectory_time.append(time)
        trajectory_az.append(az)
        trajectory_el.append(el)

        underhorizon = el < 0

        time += dt

    return trajectory_time, trajectory_az, trajectory_el

def fit_trajectory(t, x, n):

    t0 = t[0]

    A = np.zeros((len(t), n+1))

    for i in range(n+1):
        A[:, i] = (t-t0)**i

    b = x.reshape((len(x), 1))

    coef = np.linalg.solve(np.dot(A.T, A), np.dot(A.T, b))

    def fit(t):
        x = 0
        for i in range(n+1):
            x += coef[i]*(t-t0)**i

        return x

    vel = np.zeros_like(t)
    acc = np.zeros_like(t)

    for i in range(n+1):
        if i > 0:
            vel += i*coef[i]*t**(i-1)
        if i > 1:
            acc += (i-1)*i*coef[i]*t**(i-2)

    max_vel = np.max(abs(vel))
    max_acc = np.max(abs(acc))

    return fit, coef

def max_vel_and_acc(coef, t):
    vel = np.zeros_like(t)
    acc = np.zeros_like(t)

    for i in range(len(coef)):
        if i > 0:
            vel += i * coef[i] * t ** (i - 1)
        if i > 1:
            acc += (i - 1) * i * coef[i] * t ** (i - 2)

    max_vel = np.max(abs(vel))
    max_acc = np.max(abs(acc))

    return max_vel, max_acc

def acceleration_path(coef, t0, acc):
    direction = coef[1]/abs(coef[1])
    # acceleration path
    path = lambda t: direction*acc*(t-t0)**2/2 + coef[1]*(t-t0) + coef[0]

    # needed acceleration time
    dt = abs(coef[1]/acc)
    # begin position
    x0 = path(-dt)

    # return the path, the begin time and begin position
    return path, t0-dt, x0

def decceleration_path(coef, te, t0, acc):
    vel = 0
    x = 0

    for i in range(len(coef)):
        x += coef[i]*(te-t0)**i
        if i > 0:
            vel += i*coef[i]*(te-t0)**(i-1)

    direction = vel/abs(vel)

    path = lambda t: -direction*acc*(t-te)**2/2 + vel*(t-te) + x

    dt = abs(vel/acc)
    xe = path(te+dt)

    # return the path, the end time and the end position
    return path, te+dt, xe

def generate_full_trajectory(satellite, time):
    t, az, el = find_next_orbit(satellite, time, 1, 'tle_data/Delfi-N3xt.txt')

    az_path, az_coef = fit_trajectory(t, az, 4)
    el_path, el_coef = fit_trajectory(t, el, 4)

    t0_track = t[0]
    te_track = t[-1]

    az_acceleration, t0_az_acceleration, az_0 = acceleration_path(az_coef, t0_track, 1)
    el_acceleration, t0_el_acceleration, el_0 = acceleration_path(el_coef, t0_track, 1)

    az_deceleration, te_az_deceleration, az_e = acceleration_path(az_coef, te_track, 1)
    el_deceleration, te_el_deceleration, el_e = acceleration_path(el_coef, te_track, 1)

    full_az_trajectory = [[t0_az_acceleration, az_acceleration],
                          [t0_track, az_path],
                          [te_track, az_deceleration],
                          [te_az_deceleration, 0]]

    full_el_trajectory = [[t0_el_acceleration, el_acceleration],
                          [t0_track, el_path],
                          [te_track, el_deceleration],
                          [te_el_deceleration, 0]]

    return full_az_trajectory, full_el_trajectory

if __name__ == '__main__':
    trajectory, _ = find_next_orbit('Delfi-N3xt', 1, 'tle_data/Delfi-N3xt.txt')

    import matplotlib.pyplot as plt

    plt.plot(np.array(trajectory).T[0, ::10], np.array(trajectory).T[1, ::10], 'o')

    t0 = trajectory[0][0]
    te = trajectory[-1][0]

    main_path, coef = fit_trajectory(np.array(trajectory).T[0], np.array(trajectory).T[1], 4)

    t = np.linspace(trajectory[0][0], trajectory[-1][0], 100)
    plt.plot(t, main_path(t))

    acc_path, tbegin, _ = acceleration_path(coef, t0, 0.001)

    t = np.linspace(tbegin, t0, 100)
    plt.plot(t, acc_path(t))

    decc_path, tend, _ = decceleration_path(coef, te, t0, 0.001)

    t = np.linspace(te, tend, 100)
    plt.plot(t, decc_path(t))

    plt.xlabel('time (s)')
    plt.ylabel('azimuthal angle (degrees)')

    plt.legend(['satellite orbit', 'main path antenna',
                'acceleration path antenna',
                'decceleration path antenna'])

    plt.show()
    