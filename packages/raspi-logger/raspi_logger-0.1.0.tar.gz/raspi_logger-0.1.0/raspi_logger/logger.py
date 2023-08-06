import os
from os.path import join as pjoin
import json
from datetime import datetime as dt
from time import time, sleep
from crontab import CronTab

from .ds18b20 import read_sensor
from .util import parse_interval_to_seconds, config
from .sqlite_backend import append_data


def _save_json_backend(path, new_data, conf):
    # create a new file per day
    if path is None:
        date = dt.now().date()
        fname = '%d_%d_%d_raw_log.json' % (date.year, date.month, date.day)

        # get path
        path = pjoin(conf.get('loggerPath', pjoin(os.path.expanduser('~'), 'logger')), fname)

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    # save data
    # get existing data
    try:
        with open(path, 'r') as f:
            old_data = json.load(f)
    except:
        old_data = []
    
    # append and save
    with open(path, 'w') as js:
        old_data.extend(new_data)
        json.dump(old_data, js, indent=4)


def save_data(path=None, dry=False, **kwargs):
    # get the config
    conf = config()

    # read the sensor data
    # TODO, here the protocols could be loaded from config.
    data = read_sensor(conf=conf, **kwargs)
    
    # in dry runs, only return the data
    if dry:
        return data

    if len(data) == 0:
        print('[ERROR]: recieved no data. Need better logging. Sorry.')
        return []
    
    # check the registered backends
    for name, c in conf.get('loggerBackends', {}).items():
        # check if the backend is currently enabled
        if c.get('enabled', True):
            if name == 'json':
                _save_json_backend(path, data, conf)
            elif name == 'sqlite3':
                append_data(data, conf, path)

    # return the data for reuse
    return data


def stream(interval=None, dry=False, **kwargs):
    # get the start time
    t1 = time()
    
    if interval is None:
        interval = config().get('loggerInterval', '1min')
    else:
        config(loggerInterval=interval)
    
    if isinstance(interval, str):
        interval = parse_interval_to_seconds(interval)
    
    data = save_data(dry=dry, **kwargs)

    # stringify
    outstr = json.dumps(data, indent=4)

    # print
    print(outstr)

    # sleep for the remaining time
    remain = interval - (time() - t1)
    if remain < 0:
        remain = 0
    sleep(remain)

    # call again
    stream(dry=dry, **kwargs)


if __name__=='__main__':
    import fire
    fire.Fire({
        'save': save_data,
        'stream': stream,
    })
