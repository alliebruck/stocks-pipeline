# Serverless Stock Analytics Pipeline

## Overview

This project is a serverless stock analytics platform built with AWS and React.

The system retrieves stock market data from the Polygon (Massive) API, calculates the daily top-performing stock from a predefined watchlist, stores the results in DynamoDB, and exposes the data through a REST API consumed by a React frontend.

## Architecture

```text
EventBridge
     ↓
Ingestion Lambda
     ↓
Polygon (Massive) API
     ↓
DynamoDB
     ↓
API Lambda
     ↓
API Gateway
     ↓
React Frontend
```

## Technologies Used

- AWS Lambda
- AWS DynamoDB
- AWS API Gateway
- AWS EventBridge
- AWS CDK
- Python
- React
- Vite
- Polygon (Massive) Stock API

## Features

- Daily stock data ingestion
- Automated scheduling with EventBridge
- Serverless backend architecture
- Infrastructure as Code using AWS CDK
- REST API endpoint
- React dashboard displaying the latest 7 winning stocks
- Environment variable-based API key management

## Project Structure

```text
backend/
frontend/
infra/
README.md
```

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

## Future Improvements

- AWS Secrets Manager integration
- Stock price visualizations
- Additional watchlist configuration
- CI/CD pipeline using GitHub Actions