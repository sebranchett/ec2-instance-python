#!/usr/bin/env python3
from aws_cdk import App, Environment
from aws_cdk.assertions import Template, Match

from app.ec2_instance_stack import EC2InstanceStack

app = App()
ec2_stack = EC2InstanceStack(
    app, "ec2-instance",
    instance_type="t2.small",
    ami_alias="",
    ami_name="Deep Learning Base AMI (Ubuntu 18.04) Version ??.?",
    ami_owner="amazon",
    bucket_name="tudelft-results-of-calculations",
    env=Environment(
        account="123456789012", region="eu-central-1"
    )
)

# Prepare the stack for assertions.
template = Template.from_stack(ec2_stack)


def test_synthesizes_properly():
    template.resource_count_is(type="AWS::EC2::Instance", count=1)
    template.resource_count_is(type="AWS::EC2::Subnet", count=1)
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
        {"InstanceType": Match.object_like({"Ref": "instancetypeparameter"})}
    )

    template.has_resource_properties(
        "AWS::EC2::Instance",
        {"AvailabilityZone": Match.string_like_regexp("dummy1a")}
    )

    template.has_resource_properties(
        "AWS::EC2::Instance",
        {"ImageId": Match.string_like_regexp("ami-")}
    )


def test_parameters():
    template.has_parameter(
        "instancetypeparameter",
        {"Default": Match.string_like_regexp("t2.small")}
    )

    template.has_parameter(
        "bucketparameter",
        {
            "Default": Match.string_like_regexp(
                "tudelft-results-of-calculations"
            )
        }
    )


def test_iam_policy():
    template.has_resource_properties(
        "AWS::IAM::Policy",
        {"PolicyName": Match.string_like_regexp("InstanceSSMDefaultPolicy")}
    )
