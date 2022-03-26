import os
import pathlib
from ..utils import *

def data_path(*args):
    
    test_dir = "/Users/zche/cloud/code/github/0xplanet/libnft/test"
    if not os.path.exists(test_dir):
        test_dir = "/Users/zche/code/github/0xplanet/libnft/test"
    res = pathlib.Path(test_dir)
    res = res / "data"
    for _ in args:
        res = res / _
    return res