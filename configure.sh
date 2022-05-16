#!/bin/sh
# Use this to install software packages
pwd > /tmp/seb.txt
which grep >> /tmp/seb.txt
echo $HOME >> /tmp/seb.txt
echo 'Now try s3 ------------' >> /tmp/seb.txt
aws s3 ls >> /tmp/seb.txt
aws s3 cp /tmp/seb.txt s3://seb-results-of-calculations
