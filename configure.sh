#!/bin/sh
# Use this to install software packages
sudo apt-get update -y
echo 'docker here   ------------' > /tmp/output.txt
which docker >> /tmp/output.txt
echo 's3 buckets    ------------' >> /tmp/output.txt
aws s3 ls s3://seb-results-of-calculations >> /tmp/output.txt
echo 'who am I      ------------' >> /tmp/output.txt
whoami >> /tmp/output.txt
echo 'current dir   ------------' >> /tmp/output.txt
pwd >> /tmp/output.txt
echo 'files in dir  ------------' >> /tmp/output.txt
ls -l >> /tmp/output.txt

aws s3 cp /tmp/output.txt s3://seb-results-of-calculations
sudo shutdown -h now
