import json, os
import pandas as pd
import requests
import pathlib
from requests.exceptions import RetryError
from flask import current_app
from ..utils import *

def get_with_retry(url, timeout=0.5, retry=5, fail=False, **kw):
    """ All kw feed into requests.get.
    """
    try_count = 0
    log.info(f"requesting from {url}")
    success = False
    while try_count < 10 and not success:
        try:
            response = requests.get(url, timeout=0.5, **kw)
            log.info(f"retry {try_count} succeeded")
            success = True
        except requests.exceptions.ReadTimeout:
            log.info(f"retry {try_count} failed")
            response = None
            try_count += 1
    if try_count > 10 and fail:
        raise RetryError(f"failed all {try_count} retries")
    return response
