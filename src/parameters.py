from pathlib import Path
from smbclient import register_session, open_file

groundstation_location = (51.446, 5.485, 0)
interval = 120 # seconds
microstep = 20000 # amount of steps per full rotation
update_time = 1 # in days

tle_data_file = Path('./tle_data/tle.txt')
satellites_file = Path('./tle_data/satellites.txt')
log_file = Path('./log_data/log.txt')

smb_server = ''
smb_user = ''
smb_password = ''
smb_path = ''