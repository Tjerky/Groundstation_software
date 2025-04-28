from que import *
from logger import get_logger
import pytz
from parameters import satellites_file
from update_tle_data import update_tle
from database_utils import *

logger = get_logger()

possible_commands = ('list', 'add', 'delete', 'exit')

while True:
    task = input('What do you want to do (list/add/delete/exit): ')

    if task == 'list':
        list_ids()
        tasks = list_que()
        logger.info("Listing the current tasks: \n" + task)

    elif task == 'delete':
        task = input('What task do you want to add (task/sat_from_db): ')

        if task == 'task':
            index = input('Enter task index to delete: ')

            try:
                delete_command(int(index))
                logger.info(f'Deleted task: \n\t{get_command(index)}')
            except ValueError:
                print('Index should be an integer')

        elif task == 'sat_from_db':
            satellite_ids = input('Enter the NORAD IDs of satellites you want to remove (comma-separated): ')
            valid_satellites, invalid_satellites = validate_ids(satellite_ids)

            if invalid_satellites:
                print(f"Warning: These entries are invalid and will be skipped: {', '.join(invalid_satellites)}")
            if valid_satellites:
                delete_ids(valid_satellites)
            

    elif task == 'add':
        task = input('What task do you want to add (track/calibrate/sat_to_db): ')

        if task == 'track':
            satellite = input('What satellite do you want to track: ').strip()

            begin = input('From what datetime should we look for the next pass? (YYYY-MM-DD hh:mm:ss) : ')

            begin = datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')

            begin = pytz.timezone('Europe/Amsterdam').localize(begin)

            begin, end = find_next_pass(satellite, begin)

            command = f'track {satellite}'

            add_command(begin, end, command)
            logger.info(f'Scheduled tracking of {satellite} to begin at {begin}.')

        elif task == 'calibrate':
            begin = input('When do you want to start calibrating? (YYYY-MM-DD hh:mm:ss): ')

            begin = datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')

            begin = pytz.timezone('Europe/Amsterdam').localize(begin)

            # TODO find how long calibration takes
            end = begin + timedelta(minutes=5)

            command = 'calibrate'

            add_command(begin, end, command)
            logger.info(f"Scheduled calibration at {begin}")

        elif task == 'sat_to_db':
            satellite_ids = input('Enter the NORAD IDs of satellites you want to add (comma-separated): ')
            valid_satellites, invalid_satellites = validate_ids(satellite_ids)

            if invalid_satellites:
                print(f"Warning: These entries are invalid and will be skipped: {', '.join(invalid_satellites)}")
            if valid_satellites:
                write_ids(valid_satellites)

            update_tle()

        else:
            print('Please enter a valid task.')

    elif task == 'exit':
        break

    else:
        print(f'{task} is not a valid command, try again)')
