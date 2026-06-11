import json
import os
import time
from datetime import date, timedelta
from decimal import Decimal
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

import boto3


WATCHLIST = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]
TABLE_NAME = os.getenv("TABLE_NAME", "top-movers")
API_KEY = os.getenv("STOCK_API_KEY")

def get_market_date():
    today = date.today()
    candidate = today - timedelta(days=1)

    # If today is Monday, use previous Friday
    if today.weekday() == 0:
        candidate = today - timedelta(days=3)

    # If today is Sunday, use previous Friday
    elif today.weekday() == 6:
        candidate = today - timedelta(days=2)

    # If today is Saturday, use previous Friday
    elif today.weekday() == 5:
        candidate = today - timedelta(days=1)

    return candidate.isoformat()

def calculate_percent_change(open_price, close_price):
    return ((close_price - open_price) / open_price) * 100


def fetch_stock_data(ticker):
    # Using fixed date for now because current-day market data may not always be available
    market_date = get_market_date()

    url = (
        f"https://api.polygon.io/v1/open-close/{ticker}/{market_date}"
        f"?adjusted=true&apiKey={API_KEY}"
    )

    try:
        with urlopen(url, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        raise Exception(f"HTTP error for {ticker}: {e.code}")
    except URLError as e:
        raise Exception(f"URL error for {ticker}: {e.reason}")

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


def save_to_dynamodb(result):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=result)


def lambda_handler(event, context):
    if not API_KEY:
        raise ValueError("Missing STOCK_API_KEY environment variable")

    stocks = []

    for ticker in WATCHLIST:
        print(f"Fetching {ticker}...")
        try:
            stock = fetch_stock_data(ticker)
            stocks.append(stock)
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

        time.sleep(15)

    if not stocks:
        raise Exception("No stock data was fetched successfully.")

    winner = find_top_mover(stocks)

    result = {
        "date": get_market_date(),
        "ticker": winner["ticker"],
        "percent_change": Decimal(str(round(winner["percent_change"], 2))),
        "closing_price": Decimal(str(winner["close"])),
    }

    save_to_dynamodb(result)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Top mover saved successfully",
            "result": {
                "date": result["date"],
                "ticker": result["ticker"],
                "percent_change": float(result["percent_change"]),
                "closing_price": float(result["closing_price"]),
            }
        })
    }


if __name__ == "__main__":
    print(lambda_handler({}, None))