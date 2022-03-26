from flask import Flask, render_template

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

@app.route("/azuki/<i>")
def show_azuki(i):
    import sys
    sys.path.insert(0, "../..")
    from libnft.url.request import Asset
    from libnft.test import data_path
    #from PIL import Image
    #from io import BytesIO
    azuki_no = 10
    azuki = Asset(slug="azuki", idx=azuki_no)
    img_url = azuki.img_url
    return f"""
    <center>
    <img src="{img_url}" width=100>
    </center>
    """
    #azuki.get_img(out_file=data_path() / "azuki" / f"{azuki_no}.png")
    #im_bytes = azuki.get_img(out_file=data_path() / "azuki" / f"{azuki_no}.png")
    #im = Image.open(BytesIO(im_bytes))
    #im.show()


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)