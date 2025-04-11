from flask import Flask, render_template, request, send_file
import pandas as pd
import requests
from io import StringIO


app = Flask(__name__)
API_KEY = "PRU9NNAVG86LZNBG"

@app.route("/")  # This serves the landing page
def landing_page():
    return render_template("landing.html")


@app.route("/screener", methods=["GET"])  # This serves the actual screener
def screener_page():
    df = pd.read_csv("stocks.csv")

    min_price = request.args.get("min_price", type=float)
    min_pe = request.args.get("min_pe", type=float)
    min_volume = request.args.get("min_volume", type=float)

    if min_price is not None:
        df = df[df["Price"] >= min_price]
    if min_pe is not None:
        df = df[df["PE_Ratio"] >= min_pe]
    if min_volume is not None:
        df = df[df["Volume"] >= min_volume]

    if df.empty:
        df_html = "<p class='text-danger'>No data available after applying filters.</p>"
    else:
        df_html = df.to_html(classes='table table-striped stock-table', index=False, table_id="stock-table")

    return render_template("index.html", table=df_html)



if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

