from . import libnft
from libnft.utils import *

slug_info = {

    "azuki": {
        "slug": "azuki",
        "title": "AZUKI",
        "bg_color_rgb": (103, 36, 34),
        "idx_range": list(range(10000)),
        "font": "WastingerDisplayFreePersonal-MVydr",
        "font_size": 0.07,
    },
    
    "0xzuki": {
        "slug": "0xzuki",
        "title": "0xZUKI",
        "bg_color_rgb": (255, 215, 0),
        "idx_range": list(range(10000)),
        "font": "WastingerDisplayFreePersonal-MVydr",
        "font_size": 0.07,
    },

    "felinefiendznft": {
        "slug": "felinefiendsnft",
        "title": "Feline Fiendz",
        "bg_color_rgb": (255, 215, 0),
        "idx_range": list(range(7777)),
        "font": "SudegnakNo2",
        "url_file": "meta/img_url//felinefiendznft.csv", # under static
        "font_size": 0.1,
        "n_slices": 12,
    }
   
}


def get_info(slug):

    if slug in slug_info:
        return slug_info[slug]
    else:
        log.info(f"slug {slug} not found in info {slug_info.keys()}")
        return None