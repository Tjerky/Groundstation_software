from find_trajectory import *
from trace_trajectory import *
from que import read_next_command
from pytz import UTC
from datetime import datetime

while True:
    command = read_next_command()

    command_attributes = command.split(';')

    begin_time = datetime.fromisoformat(command_attributes[0])

    task = command_attributes[2]

    if 'track' in task:


    now = datetime.now(tz=UTC)

    print('Starting preparation to track')