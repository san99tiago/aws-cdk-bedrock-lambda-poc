# External imports
import aws_cdk as core
import aws_cdk.assertions as assertions

# Own imports
from cdk.stacks.cdk_bedrock_stack import BedrockStack


app: core.App = core.App()
stack: BedrockStack = BedrockStack(
    app,
    "test",
    "test",
    "test",
)
template: assertions.Template = assertions.Template.from_stack(stack)


def test_app_synthesize_ok():
    app.synth()


def test_lambda_function_created():
    match = template.find_resources(
        type="AWS::Lambda::Function",
    )
    assert len(match) == 1
