from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_s3 as s3,
    Stack, CfnParameter
)

from constructs import Construct


class EC2InstanceStack(Stack):

    def __init__(
        self, scope: Construct, id: str,
        instance_type: str,
        ami_name: str,
        ami_owner: str,
        bucket_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

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
