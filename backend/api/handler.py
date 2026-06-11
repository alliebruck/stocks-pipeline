import json
import os
from decimal import Decimal

import boto3

TABLE_NAME = os.getenv("TABLE_NAME", "top-movers")


def decimal_to_json(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)

    response = table.scan()
    items = response.get("Items", [])

    items = sorted(items, key=lambda item: item["date"], reverse=True)[:7]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(items, default=decimal_to_json),
    }

if __name__ == "__main__":
    print(lambda_handler({}, None))
