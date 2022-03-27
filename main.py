from flask import Flask, render_template, request, send_file, current_app, url_for, redirect
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from io import BytesIO
import sys
sys.path.insert(0, "../..")
from libnft.url.request import Asset
from libnft.utils import *
from apps import wallpaper
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

@app.route("/wallpaper", methods=["POST", "GET"])
def wallpaper_index():

    if request.method == 'POST':
        slug = request.form["slug"].lower()
        idx = request.form["idx"]
        if not idx:
            return render_template("wallpaper_index.html", warning="Please input a valid number (0~9999) !!")
        size = request.form["size"]
        log.info(f"{request.form}")
        return redirect(url_for(f'wallpaper_out', slug=slug, idx=idx, size=size))
    return render_template("wallpaper_index.html")


@app.route("/wallpaper/<slug>/<idx>")
def wallpaper_out(slug, idx):
    #from PIL import Image
    #from io import BytesIO
    asset = Asset(slug=slug, idx=idx)
    size = request.args.get("size")
    h, w = size.split("(")[0].split(":")
    ratio = float(h) / float(w)


    collection_info = wallpaper.get_info(slug)
    
    old_img_url = asset.img_url
    old_img_bytes = asset.get_img()
    old_img = Image.open(BytesIO(old_img_bytes))

    log.info(f"processing image")
    # enlarge filled with bg
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
    font = ImageFont.truetype(str(font_path), 250)
    txt = Image.new('RGBA', new_img.size, (255,255,255,0))
    drawer = ImageDraw.Draw(new_img)    
    drawer.text((new_w // 2, (new_h - old_h) // 2), 
                collection_info["title"],
                fill=(0, 0, 0, 255), font=font, anchor="mm")
    new_img = Image.alpha_composite(new_img, txt)

    log.info(f"done processing image")

    log.info(f"saving image")
    cache_dir = "/tmp"
    new_img_static_path_rel = f"wallpaper/cache/{today()}/{slug}/{idx}.png" # the relative path of the image under static
    new_img_path = Path(cache_dir) / "static" / new_img_static_path_rel
    #rm_old(Path(cache_dir) / "static")

    new_img_path.parent.mkdir(parents=True, exist_ok=True)
    new_img.save(str(new_img_path))
    log.info(f"done saving image")

    #new_img_url = url_for("static", filename=new_img_static_path_rel)
    new_img_url = new_img_path

    return render_template("wallpaper_out.html", 
                           old_img_url=old_img_url, 
                           new_img_url=new_img_url,
                           #bg_color="rgb(" + ",".join([str(_) for _ in page_bg_color[:3]]) + ")"
                           bg_color="rgb(0,0,0)",
                           )



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)