__all__ = [
    "Timer",
    "log",
]

import logging as log
import datetime
FORMAT = "libnft - [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
log.basicConfig(format=FORMAT, level=log.DEBUG)


class Timer():
    
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = datetime.datetime.now()
        return self

    def __exit__(self, type, value, traceback):
        self.end = datetime.datetime.now()
        self.delta_t = self.end - self.start
        self.delta_ms = self.delta_t.total_seconds() * 1000
        log.info(f"timer : {self.name}, time elapsed (ms): {self.delta_ms}")