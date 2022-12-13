import os
import yaml

from aws_cdk import (
    App, Environment
)

from app.ec2_instance_stack import EC2InstanceStack

# General configuration variables
config_yaml = yaml.load(
    open('ec2-config.yaml'), Loader=yaml.FullLoader)

# Specify Instance type
instance_type = config_yaml["instance_type"]

# Specify machine image by defining AMI name and owner
ami_name = config_yaml["ami_name"]
ami_owner = config_yaml["ami_owner"]

# Specify Bucket for input/output data
bucket_name = config_yaml["bucket_name"]

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
