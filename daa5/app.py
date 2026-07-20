import os

from flask import Flask, render_template

from minmax import run_demo

app = Flask(__name__)


@app.route("/")
def index():
    data = run_demo()
    return render_template("index.html", demo=data["demo"], performance=data["performance"])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
