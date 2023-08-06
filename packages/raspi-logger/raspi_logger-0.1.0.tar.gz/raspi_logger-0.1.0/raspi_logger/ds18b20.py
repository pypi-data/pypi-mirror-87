import os
import re
import glob
from datetime import datetime as dt

from .util import get_serial_number
from raspi_logger import keywords


def _get_sensors(path):
    return glob.glob(path + '28-*')


def _get_temperature(sensor_path):
    with open(sensor_path + '/w1_slave', 'r') as f: 
        c = f.read().split('\n')
    
    m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", c[1])
    if m:
        value = float(m.group(2)) / 1000.
    else:
        value = 'NaN'

    return value, '\n'.join(c)


def read_sensor(path='/sys/bus/w1/devices/', omit_sensor=False, omit_keyword=False, conf={}):
    data = []

    # get the Raspi serial number
    versions = get_serial_number()

    # get sensor config
    sensors = conf.get('sensors', {})

    for p in _get_sensors(path):
        temperature, hextemp = _get_temperature(p)

        d = dict(
            value=temperature,
            tstamp=dt.now().isoformat(),
            identifier=os.path.basename(p),
            rawData=hextemp,
            sensorName='DS18B20'
        )

        # extend
        if not omit_keyword:
            # get the sensor config
            if p in sensors:
                extra = sensors[p]
            elif '_all_' in sensors:
                extra = sensors['_all_']
            else:
                extra = {}
            in_soil = extra.get("in_soil", False)
        
            # add the correct variable and sensor information
            _uuid = keywords.SOIL_TEMPERATURE if in_soil else keywords.AIR_TEMPERATURE
            variable = dict(
            variableName='SOIL TEMPERATURE' if in_soil else 'AIR TEMPERATURE',
                gcmdURL=keywords.CONCEPT_URL.format(uuid=_uuid, fmt='xml'),
                gcmdUUID=_uuid
            )

            # update
            d.update(variable)

        if not omit_sensor:
            d.update(versions)            

        data.append(d)
    
    # return
    return data


if __name__ == '__main__':
    import fire
    fire.Fire(read_sensor)
