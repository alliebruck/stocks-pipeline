import os
import time
import json
from decimal import Decimal
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

import boto3
from dotenv import load_dotenv

load_dotenv()

WATCHLIST = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]

MARKET_DATES = [
    "2026-06-02",
    "2026-06-03",
    "2026-06-04",
    "2026-06-05",
    "2026-06-08",
    "2026-06-09",
    "2026-06-10",
]

API_KEY = os.getenv("STOCK_API_KEY")
TABLE_NAME = "top-movers"


def calculate_percent_change(open_price, close_price):
    return ((close_price - open_price) / open_price) * 100


def fetch_stock_data(ticker, market_date):
    url = (
        f"https://api.polygon.io/v1/open-close/{ticker}/{market_date}"
        f"?adjusted=true&apiKey={API_KEY}"
    )

    try:
        with urlopen(url, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        raise Exception(f"HTTP error for {ticker} on {market_date}: {e.code}")
    except URLError as e:
        raise Exception(f"URL error for {ticker} on {market_date}: {e.reason}")

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


def save_to_dynamodb(item):
    table = boto3.resource("dynamodb").Table(TABLE_NAME)
    table.put_item(Item=item)


def backfill_date(market_date):
    stocks = []

    for ticker in WATCHLIST:
        print(f"Fetching {ticker} for {market_date}...")

        try:
            stock = fetch_stock_data(ticker, market_date)
            stocks.append(stock)
        except Exception as e:
            print(f"Error: {e}")

        # avoid free-tier rate limits
        time.sleep(15)

    if not stocks:
        print(f"No data found for {market_date}")
        return

    winner = find_top_mover(stocks)

    item = {
        "date": market_date,
        "ticker": winner["ticker"],
        "percent_change": Decimal(str(round(winner["percent_change"], 2))),
        "closing_price": Decimal(str(winner["close"])),
    }

    save_to_dynamodb(item)
    print(f"Saved {market_date}: {item}")


if __name__ == "__main__":
    if not API_KEY:
        raise ValueError("Missing STOCK_API_KEY in .env")

    for market_date in MARKET_DATES:
        backfill_date(market_date)