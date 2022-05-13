
# Create EC2 Instance in new VPC with Systems Manager enabled
Started from the AWS example here:
https://github.com/aws-samples/aws-cdk-examples/tree/master/python/ec2/instance

This example includes:

* Own VPC with public subnet (following AWS Defaults for new accounts)
* Based on latest Amazon Linux 2
* System Manager replaces SSH (Remote session available trough the AWS Console or the AWS CLI.)
* Userdata executed from script in S3 (`configure.sh`).

## Setting up the environment
It is advisable to work in a virtual environment.
```
python -m venv .venv
```
If you are running on Windows (with Git Bash), activate the virtual environment with:
```
source .venv/Scripts/activate
```
otherwise:
```
source .venv/bin/activate
```
Now that you are in the environment, install the requirements:
```
pip install -r requirements.txt
```
Log into your AWS account using Single Sign On (SSO):
```
aws [--profile=optionalProfileName] sso login
```

## Useful commands

 * `cdk bootstrap`   initialize assets before deploy
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `aws ssm start-session --target i-xxxxxxxxx` remote session for shell access
