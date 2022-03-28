from argparse import ArgumentParser
import pandas as pd
from ast import arg
import os, json, glob
import pathlib
import requests
from selenium import webdriver
import datetime
# the 2 lines below are for printing logging messages 
import logging as log
log.basicConfig(level=log.INFO)
# the 3 lines below make browser invisible
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_options = Options()
chrome_options.add_argument("--headless")
#chrome_options.add_argument("--window-size=1920,1080")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'    
chrome_options.add_argument('user-agent={0}'.format(user_agent))

base_url_map = {
    "azuki": "https://opensea.io/assets/0xed5af388653567af2f388e6224dc7c4b3241c544/",
    "0xzuki": "https://opensea.io/assets/0x2eb6be120ef111553f768fcd509b6368e82d1661/",
    "felinefiendznft": "https://opensea.io/assets/0xacfa101ece167f1894150e090d9471aee2dd3041/",
}

def download_img(url=None, out_file=None):
    """ This function downloads an audio file from a url to a file. """
    file_ = requests.get(url)
    pathlib.Path(out_file).parent.mkdir(parents=True, exist_ok=True)
    log.info(f"downloading {url} to {out_file}")
    with open(str(out_file), "wb") as f:
        f.write(file_.content)

        
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


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--slug")
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--combine", action="store_true")
    parser.add_argument("--max-idx", type=int)
    args = parser.parse_args()
    slug = args.slug
    output_dir = pathlib.Path("/Users/zche/data/0xgenerator/database/") / slug
    root_url = pathlib.Path(base_url_map[slug])

    def download_single(num, driver, out_file=None):
        try:
            with Timer(f"{slug} {num}"):
                url = f"{root_url}/{num}"
                log.info(f"opening {url}")
                driver.get(url)
                with Timer(f"loading image of {slug} {num}"):
                    elem = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "Image--image")))
                img_url = elem.get_attribute("src")
                if out_file is not None:
                    os.system(f"""echo "{num},{img_url}" >> {out_file}""")
                    log.info(f"num = {num}, url = {img_url} written to {out_file}")
            return img_url
        except Exception as e:
            log.warning(f"noooo!!! failed getting {slug} {num}")
            log.warning(f"error: {e}")
            return None

    url_map = {}
    out_dir = f"/Users/zche/cloud/code/github/0xplanet/static/meta/img_url/"

    if args.start is not None and args.end is not None:
        log.info(f"downloading {slug} {args.start} to {args.end-1}")
        out_file = f"{out_dir}/{slug}.csv_{args.start}_{args.end}"
        os.system(f"touch {out_file}")
        os.system(f"echo num,img_url >> {out_file}")
        with webdriver.Chrome(options=chrome_options) as driver: # open a browser 
            for num in range(args.start, args.end):
                download_single(num, driver, out_file,)

    elif args.combine:
        files = glob.glob(f"{out_dir}/*.csv_*")
        df = []
        for f in files:
            df.append(pd.read_csv(f))
        df = pd.concat(df)
        log.info(f"num of entries: {len(df)}")
        df = df.drop_duplicates("num")
        log.info(f"num of unique entries: {len(df)}")

        combined_df = [df]
        with webdriver.Chrome(options=chrome_options) as driver: # open a browser 
            for num in range(args.max_idx):
                if num not in df["num"].values:
                    log.info(f"num {num} is missing... downloading now")
                    img_url = download_single(num, driver)
                    dfi = pd.DataFrame({"num": [num], "img_url": [img_url]})
                    combined_df.append(dfi)
        combined_df = pd.concat(combined_df)
        combined_file = f"{out_dir}/{slug}.csv"
        combined_df.sort_values("num").to_csv(combined_file, index=False)
        log.info(f"written to {combined_file}")

    else:
        raise