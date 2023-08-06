import fire

from .main import run, activate, deactivate
from .logger import stream


fire.Fire({
    'run': run,
    'log': run,
    'activate': activate,
    'start': activate,
    'deactivate': deactivate,
    'stop': deactivate,
    'stream': stream
})