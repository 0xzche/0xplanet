from requests.exceptions import RetryError
from ..utils import *
import json
import requests
import pathlib

base_url_map = {
    "azuki": "https://opensea.io/assets/0xed5af388653567af2f388e6224dc7c4b3241c544/",
    "0xzuki": "https://opensea.io/assets/0x2eb6be120ef111553f768fcd509b6368e82d1661/",
}


class Asset:

    def __init__(self, *, slug, idx):
        self._slug = slug
        self._idx = idx
        self._token_uri = self.get_token_uri()
        self._token_uri_json = self.get_token_uri_json()
        log.info(f"Initialized: collection {slug} number {idx}")

    def get_token_uri(self):
        base_url = {
            "azuki": "https://ikzttp.mypinata.cloud/ipfs/QmQFkLSQysj94s5GvTHPyzTxrawwtjgiiYS2TBLgrvw8CW/"
        }.get(self._slug)
        return f"{base_url}/{self._idx}"

    def get_token_uri_json(self):
        resp = get_with_retry(self._token_uri)
        asset_info = json.loads(resp.text)
        return asset_info

    @property
    def img_url(self):
        return self._token_uri_json["image"]

    def get_img(self, out_file=None):

        resp = get_with_retry(self.img_url)
        if out_file is not None:
            pathlib.Path(out_file).parent.mkdir(parents=True, exist_ok=True)
            log.info(f"downloading {self.img_url} to {out_file}")
            log.info(f"writing image to {out_file}")
            with open(str(out_file), "wb") as f:
                f.write(resp.content)
        self._img = resp.content
        return self._img
    

def get_with_retry(url, timeout=0.5, retry=5, fail=False):

    try_count = 0
    log.info(f"requesting from {url}")
    success = False
    while try_count < 10 and not success:
        try:
            response = requests.get(url, timeout=0.5)
            log.info(f"retry {try_count} succeeded")
            success = True
        except requests.exceptions.ReadTimeout:
            log.info(f"retry {try_count} failed")
            response = None
            try_count += 1
    if try_count > 10 and fail:
        raise RetryError(f"failed all {try_count} retries")
    return response