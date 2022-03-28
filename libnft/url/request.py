import json, os
import pandas as pd
import requests
import pathlib
from requests.exceptions import RetryError
from flask import current_app
from ..utils import *

slug_info = {
    "azuki": {
        "opensean_url": "https://opensea.io/assets/0xed5af388653567af2f388e6224dc7c4b3241c544/{idx}",
        "token_uri": "https://ikzttp.mypinata.cloud/ipfs/QmQFkLSQysj94s5GvTHPyzTxrawwtjgiiYS2TBLgrvw8CW/{idx}",
    },
    "0xzuki": {
        "token_uri": "https://metadata.0xzuki.com/{idx}",
        "opensea_url": "https://opensea.io/assets/0x2eb6be120ef111553f768fcd509b6368e82d1661/",
    },
    "felinefiendznft": {
        "token_uri": "https://fiendz.io/metadata/{idx}.json",
        "img_url_file": "meta/img_url//felinefiendznft.csv", 
    },
}

class Asset:

    def __init__(self, *, slug, idx):
        self._slug = slug
        self._idx = idx
        self._token_uri = self.get_token_uri()
        self._token_uri_json = self.get_token_uri_json()
        log.info(f"Initialized: collection {slug} number {idx}")

    @property
    def is_supported(self):
        return self._slug in slug_info

    def get_token_uri(self):
        if not self.is_supported:
            raise NotImplementedError(f"{self._slug} is not supported right now. Supported collections: {list(slug_info.keys())}")
        base_uri = slug_info[self._slug]["token_uri"]
        return base_uri.format(idx = self._idx)

    def get_token_uri_json(self):
        resp = get_with_retry(self._token_uri)
        asset_info = json.loads(resp.text)
        return asset_info

    @property
    def img_url(self):
        img_url = self._token_uri_json["image"]
        log.info(f"image: {img_url}")
        if slug_info[self._slug].get("img_url_file", None):  # first check if we have downloaded the img_url to file
            img_url_file = slug_info[self._slug].get("img_url_file", None)
            log.info(f"reading img_url from file {img_url_file}")
            img_url_df = pd.read_csv(f"{current_app.root_path}/static/{img_url_file}").rename(
                columns={"num": "idx"}).set_index("idx")
            img_url = img_url_df.loc[int(self._idx)]["img_url"]
            log.info(f"img_url from file: {img_url}")
        elif img_url.startswith("ipfs"): # this does not work
            hash_ = img_url.split("/")[-1]
            log.info(f"extracted hash {hash_}")
            if not hash_ or not hash_.startswith('Qm'):
                raise ValueError(f"invalid hash {hash_}")
            img_url = "http://127.0.0.1:8080/ipfs/" + hash_
            log.info(f"url from ipfs hash: {img_url}")
        return img_url

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
            #h = {"Accept-Encoding": "identity"}
            response = requests.get(url, timeout=0.5)#, stream=True, headers=h)
            log.info(f"retry {try_count} succeeded")
            success = True
        except requests.exceptions.ReadTimeout:
            log.info(f"retry {try_count} failed")
            response = None
            try_count += 1
    if try_count > 10 and fail:
        raise RetryError(f"failed all {try_count} retries")
    return response
