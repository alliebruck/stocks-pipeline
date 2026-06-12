# Top Stock Movers

A serverless stock analytics dashboard built with AWS and React that automatically tracks the daily largest stock movement across a predefined watchlist and displays the last seven trading days of results.

## Features

- Automatically identifies the stock with the largest daily percentage change from a watchlist.
- Stores historical results in Amazon DynamoDB.
- Displays the last seven trading days in an interactive React dashboard.
- Includes a trend visualization with a line chart.
- Highlights the biggest move and most frequent mover over the displayed period.
- Automatically updates through a scheduled EventBridge rule.
- Hosted as a static web application using AWS Amplify.

## Architecture

- Frontend: React + Vite
- Backend: AWS Lambda (Python)
- Database: Amazon DynamoDB
- API: Amazon API Gateway
- Scheduling: Amazon EventBridge
- Infrastructure as Code: AWS CDK
- Hosting: AWS Amplify

## Security

- API credentials are securely stored in AWS Secrets Manager.
- The ingestion Lambda retrieves secrets at runtime using IAM permissions instead of hardcoded values.
- API responses include appropriate HTTP status codes and cache-control headers.
- Sensitive credentials are excluded from source control.

## Project Structure

backend/
     api/
     ingestion/

frontend/
     src/

infra/
     AWS CDK Infrastructure

## Running Locally

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Infrastructure

```bash
cd infra
cdk deploy
```

## Dashboard

The dashboard provides:

- A 7-trading-day historical view of tracked stock movements.
- Interactive visualization of percentage changes.
- Summary statistics for the biggest move and most frequent mover.
- A detailed historical data table for analysis.

## Future Improvements

- GitHub Actions CI/CD for automated backend deployments.
- Additional analytics and historical filtering.
- Expanded watchlists and configurable tracking.
