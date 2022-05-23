import os

from aws_cdk import (
    App, Environment
)

from app.ec2_instance_stack import EC2InstanceStack

app = App()
# Looking up an AMI requires a context, because an AMI is region dependent.
# The env part below automatically creates a file 'cdk.context.json'.
# Remove 'cdk.context.json' if there is an update to image, account or region.
EC2InstanceStack(app, "ec2-instance", env=Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"]))

app.synth()
