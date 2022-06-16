import os

from aws_cdk import (
    App, Environment
)

from app.ec2_instance_stack import EC2InstanceStack


# Specify Instance type
instance_type = "t2.small"

# Specify machine image by defining AMI name and owner
# ami_name = "Deep Learning Base AMI (Ubuntu 18.04) Version ??.?"
# ami_owner = "amazon"
# if left blank, revert to a default that doesn't need credentials
ami_name = ""
ami_owner = ""

# Specify Bucket for input/output data
bucket_name = "tudelft-results-of-calculations"

app = App()
# Looking up an AMI requires a context, because an AMI is region dependent.
# The env part below automatically creates a file 'cdk.context.json'.
# Remove 'cdk.context.json' if there is an update to image, account or region.
EC2InstanceStack(
    app, "ec2-instance",
    instance_type=instance_type,
    ami_name=ami_name,
    ami_owner=ami_owner,
    bucket_name=bucket_name,
    env=Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"]
    )
)

app.synth()
