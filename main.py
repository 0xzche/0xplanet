from flask import Flask, render_template, request, send_file, current_app, url_for, redirect
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from io import BytesIO
import sys, os
sys.path.insert(0, "../..")
from libnft.url.request import Asset
from libnft.utils import *
from apps import wallpaper
from base64 import b64encode
#from libnft.test import data_path
#CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']

app = Flask(__name__)
cache = {

}

name_to_slug = {
    "Azuki": "azuki",
    "0xZuki": "0xzuki",
    "Feline Fiendz": "felinefiendznft"
}


@app.route("/wallpaper", methods=["POST", "GET"])
def wallpaper_index():

    if request.method == 'POST':
        log.info(f"{request.form}")
        slug = name_to_slug.get(request.form["slug_name"])
        idx = request.form["idx"]
        if not idx:
            return render_template("wallpaper_index.html", warning="Please input a valid number (0~9999) !!")
        size = request.form["size"]
        h, w = size.split("(")[0].split(":")
        ratio = f"{h}by{w}"
        max_idx = wallpaper.get_info(slug)["idx_range"][-1]
        idx = str(min(max_idx, int(idx)))
        log.info(f"{slug}, {idx}, {ratio}")
        return redirect(url_for(f'wallpaper_out', slug=slug, idx=idx, ratio=ratio))
    return render_template("wallpaper_index.html")


@app.route("/wallpaper/<slug>/<idx>/<ratio>/img")
def wallpaper_img(slug, idx, ratio):

    h, w = ratio.split("by")
    ratio = float(h) / float(w)
    cache_key = (slug, idx, ratio)
    log.info(f"cached items: {cache.keys()}, cache id: {id(cache)}")
    if  cache_key in cache:
        log.info(f"retreiving image {cache_key} from cache....")
        new_img = cache[(slug, idx, ratio)]
    else:
        log.info(f"image {cache_key} not found in cache, creating new ....")
        if len(cache) > 50:
            log.info(f"cache too large btw, clearing...")
            cache.clear()
        asset = Asset(slug=slug, idx=idx)

        collection_info = wallpaper.get_info(slug)
        
        old_img_bytes = asset.get_img()
        old_img = Image.open(BytesIO(old_img_bytes))
        if old_img.size[0] > 1000:
            old_img = old_img.resize((1000, 1000))

        log.info(f"processing image")
        old_w, old_h = old_img.size
        new_w = old_w
        new_h = int(new_w * ratio)
        bg_color = old_img.getpixel((10, 10))
        new_img = Image.new("RGBA", size=(new_w, new_h), color=bg_color)

        n_slices = collection_info.get("n_slices")
        if n_slices:
            top_slice = old_img.crop((0, 0, old_w, old_h // n_slices)) 
            for i in range(int(n_slices * 1.3)):
                new_img.paste(top_slice, (0, i * old_h // n_slices))
        paste_anchor = (0, new_h - old_h)
        new_img.paste(old_img, paste_anchor)

        # write txt
        log.info(f"done processing image")
        font_name = collection_info["font"]
        font_path = Path(current_app.root_path) / "static" / "fonts" / f"{font_name}.ttf"
        font = ImageFont.truetype(str(font_path), int(new_h * collection_info["font_size"]) )
        txt = Image.new('RGBA', new_img.size, (255,255,255,0))
        drawer = ImageDraw.Draw(new_img)    
        drawer.text((new_w // 2, int((new_h - old_h) * 0.85) ), 
                    collection_info["title"],
                    fill=(0, 0, 0, 255), font=font, anchor="mm")
        new_img = Image.alpha_composite(new_img, txt)

        log.info(f"saving {cache_key} to cache")
        cache[(slug, idx, ratio)] = new_img
        log.info(f"cached items: {cache.keys()}, cache id: {id(cache)}")

        # ...
    image_io = BytesIO()
    new_img.save(image_io, format='PNG')
    image_io.seek(0)


    return send_file(
        image_io,
        as_attachment=False,
        mimetype='image/png'
    )


@app.route("/wallpaper/<slug>/<idx>/<ratio>")
def wallpaper_out(slug, idx, ratio):
    new_img_url = url_for("wallpaper_img", slug=slug, idx=idx, ratio=ratio)
    return render_template("wallpaper_out.html", 
                           new_img_url=new_img_url,
                           bg_color="rgb(0,0,0)")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)