#!/bin/sh
# Use this to install software packages
sudo apt-get update -y
mkdir /tmp/home
echo 'docker here   ------------' > /tmp/home/output.txt
which docker >> /tmp/home/output.txt
echo 's3 buckets    ------------' >> /tmp/home/output.txt
aws s3 ls s3://seb-results-of-calculations >> /tmp/home/output.txt
echo '--------------------------' >> /tmp/home/output.txt

cd /tmp/home
echo 'current dir   ------------' >> /tmp/home/output.txt
pwd >> /tmp/home/output.txt
aws s3 cp s3://seb-results-of-calculations/docker_tar_image.tar .
echo 'files in home ------------' >> /tmp/home/output.txt
ls -l >> /tmp/home/output.txt
sudo docker load < docker_tar_image.tar
echo 'docker images ------------' >> /tmp/home/output.txt
sudo docker image ls >> /tmp/home/output.txt
echo '--------------------------' >> /tmp/home/output.txt

echo 'run test      ------------' >> /tmp/home/output.txt
sudo docker run --rm sebranchett/gpaw:one_processor_21.1.0 gpaw test >> /tmp/home/output.txt
echo '--------------------------' >> /tmp/home/output.txt

aws s3 cp /tmp/home/output.txt s3://seb-results-of-calculations
sudo shutdown -h now
