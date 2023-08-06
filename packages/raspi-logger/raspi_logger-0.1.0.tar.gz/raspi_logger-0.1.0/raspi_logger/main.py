from crontab import CronTab

from .util import config, parse_interval_to_seconds
from .logger import save_data


# maybe activate a a sensor protocol directly? for multiple cronjobs?
def activate(basecmd='python3 -m raspi_logger run'):
    cmt = 'raspi-logger-cron'
    # set the interval
    conf = config()
    interval = parse_interval_to_seconds(conf.get('loggerInterval', '15min'))
    if interval < 60:
        # less than a minute is not supported by crontab
        seconds = list(range(0, 60, interval))

        # get the crontab
        cron = CronTab(user=True)
        cmds = ['sleep %d;%s' % (s, basecmd) for s in seconds]
        jobs = [cron.new(command=cmd, comment=cmt) for cmd in cmds]
        for job in jobs:
            job.minute.every(1)
    else:
        job = cron.new(command=basecmd, comment=cmt)
        job.minute.every(int(interval / 60))
    
    # save 
    cron.write()

    # change config
    config(loggerCronjob='enabled')
    print('Saved.')


def deactivate(comment='raspi-logger-cron'):
    # disable the config first
    config(loggerCronjob='disabled')

    # get the crontab
    cron = CronTab(user=True)
    jobs = list(cron.find_comment(comment))

    # delete all
    for job in jobs:
        job.delete()
    
    cron.write()
    print('Stopped.')


def run():
    # first check if we should still log:
    conf = config()
    if conf.get('loggerCronjob', 'disabled')=='disabled':
        deactivate()
        return 

    # do the logging - TODO: here we could add a logic to handle more sensors
    save_data()
