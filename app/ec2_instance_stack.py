from typing import Sequence
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_s3 as s3,
    Stack
)

from constructs import Construct


class EC2InstanceStack(Stack):

    def __init__(
        self, scope: Construct, id: str,
        instance_type: str,
        ami_name: str,
        ami_owner: Sequence[str],
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
        # Look up machine image
        machine_image = ec2.MachineImage.lookup(
            name=ami_name,
            owners=ami_owner
        )

        # Script in user data startup script
        with open("./configure.sh") as f:
            user_data = f.read()

        instance = ec2.Instance(
            self,
            "Instance",
            instance_type=ec2.InstanceType(instance_type),
            machine_image=machine_image,
            vpc=vpc,
            role=role,
            user_data=ec2.UserData.custom(user_data)
        )

        # Results data bucket permissions
        results_bucket = s3.Bucket.from_bucket_name(
            self, id="Results Bucket",
            bucket_name=bucket_name
        )
        results_bucket.grant_read_write(instance.role)
