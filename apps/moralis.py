from . import *
import requests
from libnft import log
from libnft.url.request import get_with_retry
from libnft.meta import get_slug_info




if __name__ == "__main__":

    
    headers = {
        'accept': 'application/json', 
        'X-API-Key': 'yNj2WqJmwcrQPIYlFuPBVUmpmvRmzDPywgOxaTaPCfT7J6XX1h6PZVzFH53sPyis',
    }
    url = "https://deep-index.moralis.io/api/v2/nft/0xED5AF388653567Af2F388E6224dC7C4b3241C544/owners?chain=eth&format=decimal&limit=100"
    response = get_with_retry(url, headers=headers)
    log.info(f""" 
    {response.text}
             """)