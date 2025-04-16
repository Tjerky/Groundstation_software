import requests

sources = [
    "http://www.celestrak.com/NORAD/elements/cubesat.txt",
    "http://www.celestrak.com/NORAD/elements/weather.txt",
    "http://www.celestrak.com/NORAD/elements/science.txt"
]

file = 'tle.txt'

print('Retrieving data:')
with open(file, 'w') as f:
    for source in sources:
        r = requests.get(source)

        f.write(r.text.replace('\r', ''))

        print(f'from {source} [done]')

print(f'Updated file: {file}')
