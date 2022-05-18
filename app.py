import os.path
import os

from aws_cdk.aws_s3_assets import Asset

from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_s3 as s3,
    App, Stack, Environment
)

from constructs import Construct

dirname = os.path.dirname(__file__)


class EC2InstanceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Specify Instance type
        # instance_type = ec2.InstanceType("t3.nano")
        instance_type = ec2.InstanceType("t2.small")

        # Specify AMI
        machine_image = ec2.MachineImage.lookup(
            name="Deep Learning Base AMI (Ubuntu 18.04) Version ??.?",
            owners=["amazon"])

        # Specify Bucket for output data
        output_bucket_name = "seb-results-of-calculations"

        # VPC
        vpc = ec2.Vpc(self, "VPC",
                      nat_gateways=0,
                      subnet_configuration=[ec2.SubnetConfiguration(
                                            name="public",
                                            subnet_type=ec2.SubnetType.PUBLIC)]
                      )

        # Instance Role and SSM Managed Policy and S3 Managed Policy
        role = iam.Role(self, "InstanceSSM",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(
                                "AmazonSSMManagedInstanceCore"))

        # Instance
        instance = ec2.Instance(self, "Instance",
                                instance_type=instance_type,
                                machine_image=machine_image,
                                vpc=vpc,
                                role=role
                                )

        # Script in S3 as Asset
        asset = Asset(self, "Asset",
                      path=os.path.join(dirname, "configure.sh"))
        local_path = instance.user_data.add_s3_download_command(
            bucket=asset.bucket,
            bucket_key=asset.s3_object_key
        )

        # Userdata executes script from S3
        instance.user_data.add_execute_file_command(
            file_path=local_path
            )
        asset.grant_read(instance.role)

        # Output data bucket permissions
        output_bucket = s3.Bucket.from_bucket_name(
                            self, id="Output Bucket",
                            bucket_name=output_bucket_name)
        output_bucket.grant_read_write(instance.role)


app = App()
# Looking up an AMI requires a context, because an AMI is region dependent.
# The env part below automatically creates a file 'cdk.context.json'.
# Remove 'cdk.context.json' if there is an update to image, account or region.
EC2InstanceStack(app, "ec2-instance", env=Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"]))

app.synth()
