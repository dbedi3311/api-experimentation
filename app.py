from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/tileview")
def tile_view():
    return render_template("tileviewer.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
