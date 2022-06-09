import os.path
import os

from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_s3 as s3,
    Stack
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
            owners=["amazon"]
        )

        # Specify Bucket for input/output data
        output_bucket_name = "tudelft-results-of-calculations"

        # VPC
        vpc = ec2.Vpc(
            self,
            "VPC",
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC
                    )
                ]
            )

        # Instance Role and SSM Managed Policy
        role = iam.Role(
            self,
            "InstanceSSM",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )

        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore"
                )
            )

        # Instance
        # Script in user data startup script
        with open("./configure.sh") as f:
            user_data = f.read()

        instance = ec2.Instance(
            self,
            "Instance",
            instance_type=instance_type,
            machine_image=machine_image,
            vpc=vpc,
            role=role,
            user_data=ec2.UserData.custom(user_data)
        )

        # Output data bucket permissions
        output_bucket = s3.Bucket.from_bucket_name(
            self, id="Output Bucket",
            bucket_name=output_bucket_name
        )
        output_bucket.grant_read_write(instance.role)
