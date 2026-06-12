from aws_cdk import (
    CfnParameter,
    Stack,
    RemovalPolicy,
    Duration,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_events as events,
    aws_events_targets as targets,
    aws_secretsmanager as secretsmanager,
)

from constructs import Construct

class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        movers_table = dynamodb.Table(
            self,
            "TopMoversTable",
            table_name="top-movers",
            partition_key=dynamodb.Attribute(
                name="date",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        api_lambda = _lambda.Function(
            self,
            "ApiLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("../backend/api"),
            environment={
                "TABLE_NAME": movers_table.table_name,
            },
        )
        movers_table.grant_read_data(api_lambda)

        api = apigateway.RestApi(
            self,
            "TopMoversApi",
            rest_api_name="Top Movers Service",
        )

        stock_api_secret = secretsmanager.Secret.from_secret_name_v2(
            self,
            "StockApiKeySecret",
            "stock-api-key",
        )

        ingestion_lambda = _lambda.Function(
            self,
            "IngestionLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("../backend/ingestion"),
            timeout=Duration.minutes(3),
            environment={
                "TABLE_NAME": "top-movers",
                "STOCK_API_SECRET_NAME": "stock-api-key",
            },
        )

        stock_api_secret.grant_read(ingestion_lambda)

        movers_table.grant_write_data(ingestion_lambda)

        daily_rule = events.Rule(
            self,
            "DailyStockIngestionRule",
            schedule=events.Schedule.cron(
                minute="0",
                hour="8",
            ),
        )

        daily_rule.add_target(targets.LambdaFunction(ingestion_lambda))

        movers_resource = api.root.add_resource("movers")

        movers_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(api_lambda),
        )
