# External imports
from aws_cdk import (
    Stack,
    CfnOutput,
)
from constructs import Construct


class ExampleStack(Stack):
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
        # TODO: ADD CORE FUNCTIONALITIES

        # Create CloudFormation outputs
        self.generate_cloudformation_outputs()

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
            "SSMParameterName",
            value=self.example_ssm_parameter.parameter_name,
            description="Example SSM Parameter Name",
        )
