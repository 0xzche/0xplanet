




collection_info = {

    "azuki": {
        "slug": "azuki",
        "title": "AZUKI",
        "bg_color_rgb": (103, 36, 34),
        "idx_range": list(range(10000))
    },
    
    "0xzuki": {
        "slug": "0xzuki",
        "title": "0xZUKI",
        "bg_color_rgb": (255, 215, 0),
        "idx_range": list(range(10000))
    }
    
}


def get_info(slug):

    if slug in collection_info:
        return collection_info[slug]
    else:
        return None