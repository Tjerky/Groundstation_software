import logging
import os
from datetime import datetime
import pytz
from parameters import log_file

def get_logger(name="GroundStationLogger", logfile=log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        # Create directory if needed
        log_dir = os.path.dirname(logfile)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(level)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger

def get_logger_without_formatter(name="GroundStationLogger1", logfile=log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        # Create directory if needed
        log_dir = os.path.dirname(logfile)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(level)

        logger.addHandler(file_handler)

    return logger


def format_position(position, angle_direction):
    now = datetime.now(tz=pytz.timezone('Europe/Amsterdam'))
    time_formatted = now.strftime('%Y-%m-%d %H:%M:%S')

    return f'{time_formatted} - {angle_direction}: {position}'
