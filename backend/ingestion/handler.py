import os
import time
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()

WATCHLIST = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]
API_KEY = os.getenv("STOCK_API_KEY")

def calculate_percent_change(open_price, close_price):
    return ((close_price - open_price) / open_price) * 100

def fetch_stock_data(ticker):
    url = (
        f"https://api.polygon.io/v1/open-close/{ticker}/2025-06-02"
        f"?adjusted=true&apiKey={API_KEY}"
    )

    response = requests.get(url, timeout=10)
    data = response.json()

    if response.status_code != 200:
        raise Exception(f"API error for {ticker}: {data}")

    open_price = data["open"]
    close_price = data["close"]

    return {
        "ticker": ticker,
        "open": open_price,
        "close": close_price,
        "percent_change": calculate_percent_change(open_price, close_price),
    }

def find_top_mover(stocks):
    return max(stocks, key=lambda stock: abs(stock["percent_change"]))

def main():
    if not API_KEY:
        raise ValueError("Missing STOCK_API_KEY in .env file")

    stocks = []
    

    for ticker in WATCHLIST:
        print(f"Fetching {ticker}...")
        try:
            stock = fetch_stock_data(ticker)
            stocks.append(stock)
            time.sleep(15)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(15)

    winner = find_top_mover(stocks)

    result = {
        "date": str(date.today()),
        "ticker": winner["ticker"],
        "percent_change": round(winner["percent_change"], 2),
        "closing_price": winner["close"],
    }

    print(result)

if __name__ == "__main__":
    main()