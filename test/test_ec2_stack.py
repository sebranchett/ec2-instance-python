#!/usr/bin/env python3
from aws_cdk import App, Environment
from aws_cdk.assertions import Template
# from aws_cdk.assertions import Capture, Match

from app.ec2_instance_stack import EC2InstanceStack


def test_synthesizes_properly():
    app = App()
    ec2_stack = EC2InstanceStack(app, "ec2-instance", env=Environment(
                    account="123456789012", region="eu-central-1"))

    # Prepare the stack for assertions.
    template = Template.from_stack(ec2_stack)
    template.resource_count_is(type="AWS::EC2::Instance", count=1)
    template.resource_count_is(type="AWS::EC2::Subnet", count=3)
    template.resource_count_is(type="AWS::IAM::Policy", count=1)
