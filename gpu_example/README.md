# GPU Example
This example uses the [NVIDIA GPU Optimized AMI](https://aws.amazon.com/marketplace/pp/prodview-7ikjtg3um26wq).

The startup script:
* installs an AWS Systems Manager Agent
* runs a PyTorch example
* copies the output to an S3 bucket
* shuts down the virtual machine (but does not delete it)

The configuration file defines:
* a GPU instance type
* the AMI
* the bucket