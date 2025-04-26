import pytz
from pyorbital.orbital import Orbital
from datetime import datetime, timedelta
from parameters import groundstation_location
from logger import get_logger

logger = get_logger()

def find_next_pass(satellite, time=datetime.utcnow(), file=None):
    cube = Orbital(satellite, 'tle_data/Delfi-N3xt.txt')

    dt = timedelta(seconds=1)

    underhorizon = True

    while underhorizon:
        az, el = cube.get_observer_look(time, *groundstation_location)

        underhorizon = el < 0

        time += dt

    begin_time = time

    az_begin, el_begin = cube.get_observer_look(begin_time, *groundstation_location)

    while not underhorizon:
        az, el = cube.get_observer_look(time, *groundstation_location)

        underhorizon = el < 0

        time += dt

    end_time = time
    az_end = az
    el_end = el

    return begin_time, end_time

def add_command(begin, end, command):
    if (begin.tzinfo is None) or (end.tzinfo is None):
        print('Warning: datetimes that were passed to add_command were naive, assuming UTC')
    else:
        begin = begin.astimezone(pytz.UTC)
        end = end.astimezone(pytz.UTC)

    with open('que.txt', 'r+') as f:
        que = f.readlines()

    found = False

    if len(que) == 0:
        found = True
        i = 0

    previous = datetime(2000, 1, 1)
    previous = pytz.UTC.localize(previous)

    for i in range(len(que)):
        next = datetime.fromisoformat(que[i].split(';')[0])
        if (previous < begin) and (end < next):
            found = True
            break

        previous = datetime.fromisoformat(que[i].split(';')[1])

    if found:
        que.insert(i, f'{begin};{end};{command};\n')
    elif previous < begin:
        que.append(f'{begin};{end};{command};\n')
    else:
        logger.info('Command could not be added to que, because another command is already added in that time.')
        print('Command could not be added to que, because another command is already added in that time.')
        #raise BaseException('Command could not be added to que, because another command is already added in that time.')

    with open('que.txt', 'w') as f:
        f.writelines(que)

def read_next_command():
    now = datetime.now(tz=pytz.UTC)

    with open('que.txt', 'r') as f:
        que = f.readlines()

    for i in range(len(que)):
        begin = datetime.strptime(que[i].split(';')[0], f'%Y-%m-%d %H:%M:%S.%f+%Z')
        if begin > now:
            break

    que = que[i:]

    with open('que.txt', 'w') as f:
        f.writelines(que)

    if len(que) == 0:
        return None

    que_items = que[0].split(';')
    begin = datetime.strptime(que_items[0], '%Y-%m-%d %H:%M:%S.%f+%Z')
    end = datetime.strptime(que_items[1], '%Y-%m-%d %H:%M:%S.%f+%Z')
    command = que_items[2]

    return begin, end, command

def delete_command(i):
    with open('que.txt', 'r') as f:
        que = f.readlines()

    que = que[:i] + que[i+1:]

    with open('que.txt', 'w') as f:
        f.writelines(que)

def get_command(i):
    with open('que.txt', 'r') as f:
        que = f.readlines()
    
    return que[i]

def list_que():
    with open('que.txt', 'r') as f:
        que = f.readlines()

    for i in range(len(que)):
        print('{index}: {item}'.format(index=i, item=que[i].replace(';', ' ')))


