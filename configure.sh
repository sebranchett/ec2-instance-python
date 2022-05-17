#!/bin/sh
# Use this to install software packages
sudo apt-get update -y
echo 'docker here  ------------' > /tmp/output.txt
which docker >> /tmp/output.txt
echo 's3 buckets   ------------' >> /tmp/output.txt
aws s3 ls >> /tmp/output.txt
aws s3 cp /tmp/output.txt s3://seb-results-of-calculations
sudo shutdown -h now
