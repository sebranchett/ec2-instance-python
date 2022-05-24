#!/usr/bin/env python3
from aws_cdk import App, Environment
from aws_cdk.assertions import Template, Match
# from aws_cdk.assertions import Capture

from app.ec2_instance_stack import EC2InstanceStack

app = App()
ec2_stack = EC2InstanceStack(app, "ec2-instance", env=Environment(
                account="123456789012", region="eu-central-1"))

# Prepare the stack for assertions.
template = Template.from_stack(ec2_stack)


def test_synthesizes_properly():
    template.resource_count_is(type="AWS::EC2::Instance", count=1)
    template.resource_count_is(type="AWS::EC2::Subnet", count=3)
    template.resource_count_is(type="AWS::IAM::Policy", count=1)


def test_vpc():
    template.has_resource_properties(
        type="AWS::EC2::VPC",
        props={"CidrBlock": "10.0.0.0/16",
               "EnableDnsHostnames": True,
               "EnableDnsSupport": True,
               "InstanceTenancy": "default",
               "Tags": [{"Key": "Name",
                         "Value": "ec2-instance/VPC"}]
               }
    )


def test_ec2():
    template.has_resource_properties(
        "AWS::EC2::Instance",
        {"InstanceType": Match.string_like_regexp("t2.small")}
        )

    template.has_resource_properties(
        "AWS::EC2::Instance",
        {"AvailabilityZone": Match.string_like_regexp("dummy1a")}
        )

    template.has_resource_properties(
        "AWS::EC2::Instance",
        {"ImageId": Match.string_like_regexp("ami-")}
        )


def test_iam_policy():
    template.has_resource_properties(
        "AWS::IAM::Policy",
        {"PolicyName": Match.string_like_regexp("InstanceSSMDefaultPolicy")}
        )
