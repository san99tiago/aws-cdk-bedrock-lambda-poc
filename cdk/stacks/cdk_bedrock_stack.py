# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_lambda,
    aws_iam,
    Duration,
    RemovalPolicy,
)
from constructs import Construct


class BedrockStack(Stack):
    """
    Class to create the infrastructure on AWS.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        main_resources_name_id: str,
        deployment_environment: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Input parameters
        self.construct_id = construct_id
        self.main_resources_name_id = main_resources_name_id
        self.deployment_environment = deployment_environment

        # Main methods for the deployment
        self.create_lambda_layers()
        self.create_lambda_functions()

        # Create CloudFormation outputs
        self.generate_cloudformation_outputs()

    def create_lambda_layers(self):
        """
        Create the Lambda layers that are necessary for the additional runtime
        dependencies of the Lambda Functions.
        """

        # Layer for "FastAPI" and "Mangum" Adapter libraries
        self.lambda_layer_fastapi = aws_lambda.LayerVersion(
            self,
            id="LambdaLayer-FastAPI",
            code=aws_lambda.Code.from_asset("lambda-layers/fastapi/modules"),
            compatible_runtimes=[
                aws_lambda.Runtime.PYTHON_3_11,
            ],
            description="Lambda Layer for Python with <fastapi> library",
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Layer for latest "boto3" version (to test new bedrock clients)
        self.lambda_layer_boto3 = aws_lambda.LayerVersion(
            self,
            id="LambdaLayer-boto3",
            code=aws_lambda.Code.from_asset("lambda-layers/boto3/modules"),
            compatible_runtimes=[
                aws_lambda.Runtime.PYTHON_3_11,
            ],
            description="Lambda Layer for Python with <boto3> library",
            removal_policy=RemovalPolicy.DESTROY,
        )

    def create_lambda_functions(self):
        """
        Create the Lambda Functions for the FastAPI server.
        """
        # Get relative path for folder that contains Lambda function source
        # ! Note--> we must obtain parent dirs to create path (that"s why there is "os.path.dirname()")
        PATH_TO_LAMBDA_FUNCTION_FOLDER = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "src",
            "lambdas",
        )
        self.lambda_fastapi_bedrock: aws_lambda.Function = aws_lambda.Function(
            self,
            "Lambda-FastAPI",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="main.handler",
            code=aws_lambda.Code.from_asset(PATH_TO_LAMBDA_FUNCTION_FOLDER),
            timeout=Duration.seconds(30),
            memory_size=128,
            environment={
                "ENVIRONMENT": self.deployment_environment,
                "LOG_LEVEL": "DEBUG",
            },
            layers=[
                self.lambda_layer_fastapi,
                self.lambda_layer_boto3,
            ],
            log_format=aws_lambda.LogFormat.JSON.value,
            application_log_level=aws_lambda.ApplicationLogLevel.DEBUG.value,
        )

        # Allow Lambda Function Role to interact with Bedrock
        self.lambda_fastapi_bedrock.add_to_role_policy(
            aws_iam.PolicyStatement(
                sid="BedrockFullAccess",
                effect=aws_iam.Effect.ALLOW,
                actions=[
                    "bedrock:*",
                ],
                resources=["*"],
            )
        )

        self.lambda_function_url = self.lambda_fastapi_bedrock.add_function_url(
            auth_type=aws_lambda.FunctionUrlAuthType.AWS_IAM,
        )

    def generate_cloudformation_outputs(self):
        """
        Method to add the relevant CloudFormation outputs.
        """

        CfnOutput(
            self,
            "DeploymentEnvironment",
            value=self.deployment_environment,
            description="Deployment environment",
        )

        CfnOutput(
            self,
            "LambdaFunctionUrl",
            value=self.lambda_function_url.url,
            description="URL to invoke Lambda Function",
        )
