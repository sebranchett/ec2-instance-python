#!/bin/bash
# Use this to install software packages
if VERB="$( which apt-get )" 2> /dev/null; then
   sudo apt-get update -y
elif VERB="$( which yum )" 2> /dev/null; then
   sudo yum update -y
else
   echo "WARNING: Could not update the system" >&2
fi

# Install SSM agent, so you can log in. This us the Ubuntu version
# See https://repost.aws/knowledge-center/install-ssm-agent-ec2-linux#
mkdir /tmp/ssm
cd /tmp/ssm
wget https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/debian_amd64/amazon-ssm-agent.deb
sudo dpkg -i amazon-ssm-agent.deb
sudo systemctl enable amazon-ssm-agent

# Clone a PyTorch example
cd /tmp
git clone https://github.com/sebranchett/delftblue-gpu-apptainer-pytorch.git
cd delftblue-gpu-apptainer-pytorch

# Run the PyTorch example. Be patient, it takes a while. The VM will enter Stopped state on completion
sudo docker run --gpus all --rm -v "$PWD":/workspace/test nvcr.io/nvidia/pytorch:22.10-py3 /bin/sh -c "cd test;python < quickstart.py > quickstart.log"

aws s3 cp quickstart.log s3://tudelft-results-of-calculations
sudo shutdown -h now
