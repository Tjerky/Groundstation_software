from que import *
from logger import get_logger
import pytz
from parameters import satellites_file

logger = get_logger()

possible_commands = ('list', 'add', 'delete', 'exit')

while True:
    task = input('What do you want to do (list/add/delete/exit): ')

    if task == 'list':
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
            satellite_id = input('Enter the NORAD ID of the satellite to remove: ').strip()
            
            with open(satellites_file, 'r') as f:
                lines = f.readlines()

            satellite_ids = [line.strip() for line in lines]

            if satellite_id in satellite_ids:
                updated_lines = [line for line in lines if line.strip() != satellite_id]
                with open(satellites_file, 'w') as f:
                    f.writelines(updated_lines)

                logger.info(f'Satellite with NORAD ID {satellite_id} added to the database')
            else:
                logger.info(f'Satellite {satellite_id} not found in database.')
                print(f'Satellite {satellite_id} not found in database.') 

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
            satellite_id = input('Enter the NORAD ID of the satellite to add: ').strip()
            
            with open(satellites_file, 'a') as f:
                f.write(satellite_id + '\n')
            
            logger.info(f'Satellite with NORAD ID {satellite_id} added to the database')
            
        else:
            print('Please enter a valid task.')

    elif task == 'exit':
        break

    else:
        print(f'{task} is not a valid command, try again)')
