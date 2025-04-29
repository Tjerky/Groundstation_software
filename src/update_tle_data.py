import requests
from logger import get_logger
from parameters import tle_data_file, satellites_file

logger = get_logger()

def load_satellite_tle(satellite_name, file_path=tle_data_file):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for i in range(0, len(lines), 3):
        curr_name = lines[i].strip()

        if curr_name == satellite_name:
            line1 = lines[i + 1].strip()
            line2 = lines[i + 2].strip()
            
            logger.info(f'Loaded TLE data for {satellite_name} successfully')

            return satellite_name, line1, line2
    
    logger.info(f'Satellite {satellite_name} not in database')


def update_tle():
    print('Retrieving data:')
    with open(satellites_file, 'r') as f:
        lines = f.readlines()

    with open(tle_data_file, 'w') as f:
        for i in range(len(lines)):
            norad_id = lines[i].strip()
            query = f'https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=TLE'

            r = requests.get(query)

            f.write(r.text.replace('\r', ''))

            print(f'update {query} [done]')

    print(f'Updated file: {tle_data_file}')
    logger.info('Updated TLE data')

if __name__ == "__main__":
    update_tle()
