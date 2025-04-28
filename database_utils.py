from logger import get_logger
from parameters import satellites_file

logger = get_logger()

def validate_ids(satellite_ids):
    satellite_list = [sat_id.strip() for sat_id in satellite_ids.split(',') if sat_id.strip()]
    valid_satellites = [sat_id for sat_id in satellite_list if sat_id.isdigit() and (len(sat_id) == 5 or len(sat_id) == 6)]
    invalid_satellites = [sat_id for sat_id in satellite_list if sat_id not in valid_satellites]

    return valid_satellites, invalid_satellites

def check_existing(valid_satellites):
    with open(satellites_file, 'r') as f:
        all_satellites = {line.strip() for line in f.readlines()}
    present_satellites = [sat_id for sat_id in valid_satellites if sat_id in all_satellites]
    not_present = [sat_id for sat_id in valid_satellites if sat_id not in all_satellites]

    return present_satellites, not_present


def write_ids(valid_satellites):
    _, new_satellites = check_existing(valid_satellites)
    with open(satellites_file, 'a') as f:
        for sat_id in valid_satellites:
            if sat_id in new_satellites:
                f.write(sat_id + '\n')

    logger.info(f"Added satellites: {', '.join(new_satellites)}")


def delete_ids(valid_satellites):
    satellites_remove, _ = check_existing(valid_satellites)
    with open(satellites_file, 'r') as f:
        lines = f.readlines()

    updated_lines = [line for line in lines if line.strip() not in satellites_remove]

    with open(satellites_file, 'w') as f:
        f.writelines(updated_lines)

    logger.info(f"Deleted satellites: {', '.join(satellites_remove)}")

def list_ids():
    with open(satellites_file, 'r') as f:
        satellite_ids = [line.strip() for line in f.readlines()]

    logger.info(f"Satellites in the database: \n\t{', '.join(satellite_ids)}")
    print(f"Satellites in the database: \n\t{', '.join(satellite_ids)}")
