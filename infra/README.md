# Infrastructure

AWS CDK stack for the stocks serverless pipeline.

## Resources

- DynamoDB table named `top-movers`
- Ingestion Lambda for daily stock analysis
- EventBridge schedule for the ingestion Lambda
- API Lambda for reading mover history
- API Gateway REST API with `GET /movers`

## Deploy

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk deploy --parameters StockApiKey="$STOCK_API_KEY"
```

`StockApiKey` is marked `NoEcho` in CloudFormation and is passed to the ingestion Lambda as an environment variable.

## Useful Commands

- `cdk synth`
- `cdk diff`
- `cdk deploy --parameters StockApiKey="$STOCK_API_KEY"`
