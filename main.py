from flask import Flask, render_template, request, send_file, current_app, url_for
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from io import BytesIO
import sys
sys.path.insert(0, "../..")
from libnft.url.request import Asset
from libnft.utils import *
#from libnft.test import data_path


app = Flask(__name__)

@app.route("/")
def index():
    return "<h1> aaa <h>"

@app.route("/integer/<i>")
def integer(i):
    i = "something"
    print(i)
    #return render_template("test.html", idx=i)
    return f"<h> {i} </h>"

@app.route("/wallpaper/<slug>/<i>", methods=["POST", "GET"])
def show_nft(slug, i):
    

    return render_template("wallpaper.html")

@app.route("/wallpaper/<slug>/<i>", methods=["POST", "GET"])
def show_nft(slug, i):
    #from PIL import Image
    #from io import BytesIO
    asset = Asset(slug=slug, idx=i)
    old_img_url = asset.img_url
    old_img_bytes = asset.get_img()
    old_img = Image.open(BytesIO(old_img_bytes))

    log.info(f"processing image")
    # enlarge filled with bg
    ratio = 16 / 9
    old_w, old_h = old_img.size
    new_w = old_w
    new_h = int(new_w * ratio)
    bg_color = old_img.getpixel((10, 10))
    new_img = Image.new("RGBA", size=(new_w, new_h), color=bg_color)
    paste_anchor = (0, new_h - old_h)
    new_img.paste(old_img, paste_anchor)

    # write txt
    log.info(f"done processing image")
    #font_path = Path(current_app.root_path) / "static" / "fonts" / "Death_Note_Font_by_Karlibell22.ttf"
    font_path = Path(current_app.root_path) / "static" / "fonts" / "AbrilFatface-Regular.ttf"
    font = ImageFont.truetype(str(font_path), 200)
    txt = Image.new('RGBA', new_img.size, (255,255,255,0))
    drawer = ImageDraw.Draw(new_img)    
    drawer.text((new_w // 2, (new_h - old_h) // 2), "0xZUKI", fill=(0, 0, 0, 255), font=font, anchor="mm")
    new_img = Image.alpha_composite(new_img, txt)

    log.info(f"done processing image")

    log.info(f"saving image")
    new_img_static_path_rel = f"wallpaper/cache/{slug}/{i}.png" # the relative path of the image under static
    new_img_path = Path(current_app.root_path) / "static" / new_img_static_path_rel
    new_img_path.parent.mkdir(parents=True, exist_ok=True)
    new_img.save(str(new_img_path))
    log.info(f"done saving image")

    new_img_url = url_for("static", filename=new_img_static_path_rel)
    return render_template("wallpaper.html", old_img_url=old_img_url, new_img_url=new_img_url)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)