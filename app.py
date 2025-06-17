from flask import Flask, render_template
from db import get_latest_generators, get_latest_scraped_at
import pytz
from datetime import datetime

app = Flask(__name__)
finnish_tz = pytz.timezone("Europe/Helsinki")

@app.route("/")
def index():
    cramo_data = get_latest_generators("cramo_generators")
    ramirent_data = get_latest_generators("ramirent_generators")

    cramo_last_update = get_latest_scraped_at("cramo_generators")
    ramirent_last_update = get_latest_scraped_at("ramirent_generators")

    # Convert to Finnish time if present
    if cramo_last_update:
        cramo_last_update = cramo_last_update.replace(tzinfo=pytz.utc).astimezone(finnish_tz)
    if ramirent_last_update:
        ramirent_last_update = ramirent_last_update.replace(tzinfo=pytz.utc).astimezone(finnish_tz)

    return render_template(
        "index.html",
        cramo=cramo_data,
        ramirent=ramirent_data,
        cramo_last_update=cramo_last_update,
        ramirent_last_update=ramirent_last_update
    )

if __name__ == "__main__":
    app.run(debug=True)
