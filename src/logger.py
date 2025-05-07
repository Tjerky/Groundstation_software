import logging
from datetime import datetime
import pytz
from parameters import smb_server, smb_user, smb_password, smb_path
from smbclient import open_file, register_session

# Define a custom logging handler
class SMBFileHandler(logging.Handler):
    def __init__(self, smb_path, mode='a'):
        super().__init__()
        self.smb_path = smb_path
        self.mode = mode

    def emit(self, record):
        try:
            msg = self.format(record)
            with open_file(self.smb_path, mode=self.mode) as f:
                f.write(msg + '\n')
        except Exception:
            self.handleError(record)

_logger = None

def get_logger():
    global _logger
    if _logger is None:
        # Register the SMB session only once
        register_session(smb_server, username=smb_user, password=smb_password)

        logger = logging.getLogger("GlobalLogger")
        logger.setLevel(logging.INFO)

        smb_handler = SMBFileHandler(smb_path)

        formatter = logging.Formatter(
            '%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        smb_handler.setFormatter(formatter)

        logger.addHandler(smb_handler)
        _logger = logger

    return _logger

def format_position(position, angle_direction):
    now = datetime.now(tz=pytz.timezone('Europe/Amsterdam'))
    time_formatted = now.strftime('%Y-%m-%d %H:%M:%S')

    return f'{time_formatted} - {angle_direction}: {position}'
