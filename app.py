from flask import Flask, render_template
from db import get_latest_generators

app = Flask(__name__)

@app.route("/")
def index():
    cramo_data = get_latest_generators("cramo_generators")
    ramirent_data = get_latest_generators("ramirent_generators")
    return render_template("index.html", cramo=cramo_data, ramirent=ramirent_data)

if __name__ == "__main__":
    app.run(debug=True)