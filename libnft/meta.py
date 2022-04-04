import pandas as pd
_collection_info = {
    "azuki": {
        "slug": "azuki",
        "contract_addr": "0xed5af388653567af2f388e6224dc7c4b3241c544", 
        "opensean_url": "https://opensea.io/assets/0xed5af388653567af2f388e6224dc7c4b3241c544/{idx}",
        "token_uri": "https://ikzttp.mypinata.cloud/ipfs/QmQFkLSQysj94s5GvTHPyzTxrawwtjgiiYS2TBLgrvw8CW/{idx}",
    },
    "0xzuki": {
        "slug": "0xzuki",
        "contract_addr": "0x2eb6be120ef111553f768fcd509b6368e82d1661", 
        "token_uri": "https://metadata.0xzuki.com/{idx}",
        "opensea_url": "https://opensea.io/assets/0x2eb6be120ef111553f768fcd509b6368e82d1661/",
    },
    "felinefiendznft": {
        "slug": "felinefiendznft",
        "token_uri": "https://fiendz.io/metadata/{idx}.json",
        "img_url_file": "meta/img_url//felinefiendznft.csv", 
    },
    "loser-club-official": {
        "slug": "loser-club-official",
        "token_uri": "https://api.loserclub.io/ipfs/QmVKHeqzbTVKzp88prnXwz3MdDMyMMEDjpGzL5aARriUbD/{idx}.json"
    },
    "boredapeyachtclub": {
        "slug": "boredapeyachtclub",
        "contract_addr": "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",
    },
    "clonex": {
        "slug": "clonex",
        "contract_addr": "0x49cf6f5d44e70224e2e23fdcdd2c053f30ada28b",
    },
    "doodles-official": {
        "slug": "doodles-official",
        "contract_addr": "0x49cf6f5d44e70224e2e23fdcdd2c053f30ada28b",
    }
}

def get_slug_info(slug):

    df = pd.DataFrame.from_dict(_collection_info, orient="index")
    return df.set_index("slug").loc[slug]


if __name__ == "__main__":


    x = get_slug_info("azuki")
    print(x)