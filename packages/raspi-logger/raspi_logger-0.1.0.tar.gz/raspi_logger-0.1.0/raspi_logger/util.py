import os
import json


def get_serial_number():
    # dummy versions
    versions = dict(
        hardware='xxxxxxx',
        revision='0000000',
        serial='0000000000000000'
    )

    # open cpu info and read
    try:
        with open('/proc/cpuinfo', 'r') as info:
            for line in info:
                if line.startswith('Hardware'):
                    versions['hardware'] = line.split(':')[1].strip()
                elif line.startswith('Revision'):
                    versions['revision'] = line.split(':')[1].strip()
                elif line.startswith('Serial'):
                    versions['serial'] = line.split(':')[1].strip()

    except:
        versions = dict(
        hardware='ERRORxx',
        revision='ERROR00',
        serial='ERROR00000000000'
    )

    return versions


def parse_interval_to_seconds(s: str) -> int:
    s = s.lower()

    # Hours
    if 'hrs' in s:
        s = s.replace('hrs', 'h')
    if 'h' in s:
        s = s.replace('h', '')
        t = int(s)
        return t * 3600
    
    # Minutes
    if 'min' in s:
        s = s.replace('min', 'm')
    if 'm' in s:
        s = s.replace('m', '')
        t = int(s)
        return t * 60

    # Seconds
    if 'sec' in s:
        s = s.replace('sec', 's')
    if 's' in s:
        s = s.replace('s', '')
        return int(s)


def config(**kwargs) -> dict:
    CONF_FILE = os.path.join(os.path.dirname(__file__), 'CONFIG.JSON')
    
    # get the config
    with open(CONF_FILE, 'r') as f:
        conf = json.load(f)

    # check if we are in read or write mode
    if len(kwargs.keys()) == 0:
        return conf 
    else:
        conf.update(kwargs)

        # write
        with open(CONF_FILE, 'w') as f:
            json.dump(conf, f, indent=4)
        
        return conf