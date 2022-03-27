"""
A lowest-level module that provide utility for all other modules.
Only depend on base and 3rd-party libraries.
"""
from .logging import *
from pathlib import Path
import datetime
import glob


def today():

    return datetime.datetime.now().strftime("%Y%m%d")

def two_days_ago():
    """ for clearning cache
    """
    return (datetime.datetime.today() - datetime.timedelta(days=2)).strftime("%Y%m%d")


def rm_old(data_dir, hours=1):
    import os
    import time
    current_time = time.time()
    log.info(f"checking old files in {data_dir}")
    files = glob.glob(f"{data_dir}/**/*.png", recursive=True)
    log.info(f"globed: {files}")
    files = [_ for _ in files if os.path.isfile(_)]
    log.info(f"files found: {files}")
    for f in files:
        creation_time = os.path.getctime(f)
        if (current_time - creation_time) / 3600 >= hours:
            log.info(f'{f} is older than {hours} hours')
            os.remove(f)
            log.info(f'{f} removed'.format(f))