import sys
sys.path.insert(0, "../..")
from libnft.url.request import Asset
from libnft.test import data_path
from PIL import Image
from io import BytesIO

azuki_no = 10
azuki = Asset(slug="azuki", idx=azuki_no)
#azuki.get_img(out_file=data_path() / "azuki" / f"{azuki_no}.png")
im_bytes = azuki.get_img(out_file=data_path() / "azuki" / f"{azuki_no}.png")
im = Image.open(BytesIO(im_bytes))
im.show()

