from flask import Flask, render_template, request
import pandas as pd
import requests

app = Flask(__name__)
API_KEY = "PRU9NNAVG86LZNBG"

def fetch_stock_data(symbols):
    stock_list = []

    for symbol in symbols:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if "Global Quote" in data:
            quote = data["Global Quote"]
            stock_list.append({
                "Symbol": quote["01. symbol"],
                "Price": float(quote["05. price"]),
                "Volume": int(quote["06. volume"]),
                "PE_Ratio": "-",
            })
    return pd.DataFrame(stock_list)

@app.route("/", methods=["GET"])
def home():
    symbols = ["TCS.BSE", "INFY.BSE", "RELIANCE.BSE", "HDFCBANK.BSE", "ITC.BSE"]  # NSE or BSE symbols
    df = fetch_stock_data(symbols)

    #df = pd.read_csv('stocks.csv')
    #df.dropna(subset=['Symbol', 'Names', 'Price', 'Volume', 'PE_Ratio'], inplace=True)

    min_price = request.args.get("min_price", type=float)
    min_pe = request.args.get("min_pe", type=float)
    min_volume = request.args.get("min_volume", type=float)
    if min_price is not None:
        df = df[df["Price"] >= min_price]
    if min_pe is not None:
        df = df[df["PE_Ratio"] >= min_pe]
    if min_volume is not None:
        df = df[df["Volume"] >= min_volume]
    #return render_template("index.html", table=(df.to_html(classes='table table-striped stock-table', index=False)))
    df_html = df.to_html(classes='table table-striped stock-table', index=False, table_id="stock-table")
    return render_template("index.html", table=df_html)


if __name__ == "__main__":
    app.run(debug=True)
