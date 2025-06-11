from flask import Flask, render_template
from db import get_latest_generators
from title_utils import normalize_title

app = Flask(__name__)

@app.route("/")
def index():
    cramo_data = get_latest_generators("cramo_generators")
    ramirent_data = get_latest_generators("ramirent_generators")

    # Normalize titles for both datasets (row[1] is title)
    cramo_data = [
        (row[0], normalize_title(row[1]), *row[2:]) for row in cramo_data
    ]
    ramirent_data = [
        (row[0], normalize_title(row[1]), *row[2:]) for row in ramirent_data
    ]

    return render_template("index.html", cramo=cramo_data, ramirent=ramirent_data)

if __name__ == "__main__":
    app.run(debug=True)