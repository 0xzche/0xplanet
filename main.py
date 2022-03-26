from flask import Flask, render_template, request, send_file
import sys
sys.path.insert(0, "../..")
from libnft.url.request import Asset
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
    #from PIL import Image
    #from io import BytesIO
    asset = Asset(slug=slug, idx=i)
    img_url = asset.img_url
    """
    if request.method == "POST":
        send_file(img_url)
    """
    return render_template("wallpaper.html", img_url=img_url)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)