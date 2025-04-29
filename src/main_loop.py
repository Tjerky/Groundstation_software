from find_trajectory import *
from trace_trajectory import *
from que import read_next_command
from pytz import UTC
from datetime import datetime, timedelta
from parameters import *
from cl57t_raspberry_pi_stepper_drive.CL57TStepperDriver import *
from threading import Thread
from time import sleep
from logger import get_logger, get_logger_without_formatter
from update_tle_data import update_tle
import pytz

logger = get_logger()
logger_without_format = get_logger_without_formatter()
logger.info('Groundstation control started')

dt = timedelta(seconds=interval)

local_tz = pytz.timezone('Europe/Amsterdam')

last_updated = datetime.min

stepper_az = CL57StepperDriver(pin_en=16, pin_step=13, pin_dir=5, pin_homing_sensor=21,
                     microstepping_resolution=microstep)
stepper_az.set_movement_abs_rel(MovementAbsRel.ABSOLUTE)

make_az_step = generate_make_step(stepper_az)

stepper_el = CL57StepperDriver(pin_en=18, pin_step=1, pin_dir=24, pin_homing_sensor=1,
                     microstepping_resolution=microstep)
stepper_el.set_movement_abs_rel(MovementAbsRel.ABSOLUTE)

make_el_step = generate_make_step(stepper_el)

while True:
    now = datetime.now(tz=local_tz)

    if now - last_updated > timedelta(days=update_time):
        update_tle()
        last_updated = now

    begin, end, task = read_next_command()

    if begin - dt < now:

        if 'track' in task:
            # generate the full trajectory that needs to be followed
            satellite = task[5:]
            az_trajectory, el_trajectory = generate_full_trajectory(satellite, now)

            logger.info(f"Begin to track satellite {satellite}")

            # prepare the stepper motors to go to the starting positions
            begin_az = az_trajectory[0][1](az_trajectory[0][0])
            begin_el = el_trajectory[0][1](el_trajectory[0][0])

            stepper_az.run_to_position_steps_threaded(begin_az * microstep / 360)
            stepper_el.run_to_position_steps_threaded(begin_el * microstep / 360)

            stepper_az.wait_until_steps_done()
            stepper_el.wait_until_steps_done()

            # Execute the task, waiting is included in trace_trajectory
            az_trace_thread = Thread(target=trace_trajectory, args=(az_trajectory, microstep, make_az_step, 'AZ'))
            el_trace_thread = Thread(target=trace_trajectory, args=(el_trajectory, microstep, make_el_step, 'EL'))

            reset_shared_output()
            az_trace_thread.start()
            el_trace_thread.start()

            az_trace_thread.join()
            el_trace_thread.join()
            logger_without_format.info(shared_output.getvalue())

            logger.info(f"Satellite {satellite} has been successfully tracked")

        elif 'calibrate' in task:
            # do the calibration
            while now < begin:
                now = datetime.now(tz=UTC)

            logger.info("Starting calibration")
            stepper_az.do_homing()
            stepper_el.do_homing()
            logger.info("The antenna has been calibrated")

        else:
            logger.info(f"Unkown task in que: {task}")
            #raise ValueError('Unknown task in que')

    sleep(5)
