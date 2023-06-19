#!/bin/bash

# Install SSM agent, so you can log in. This us the Ubuntu version
# See https://repost.aws/knowledge-center/install-ssm-agent-ec2-linux#
mkdir /tmp/ssm
cd /tmp/ssm
wget https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/debian_amd64/amazon-ssm-agent.deb
sudo dpkg -i amazon-ssm-agent.deb
sudo systemctl enable amazon-ssm-agent

sudo shutdown -h now
