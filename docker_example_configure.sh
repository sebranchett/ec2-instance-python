#!/bin/sh
# Use this to install software packages
sudo apt-get update -y
echo 'docker here   ------------' > ~/output.txt
which docker >> ~/output.txt
echo 's3 buckets    ------------' >> ~/output.txt
aws s3 ls >> ~/output.txt
echo '--------------------------' >> ~/output.txt

cd ~
aws s3 cp s3://seb-results-of-calculations/docker_tar_image.tar .
echo 'files in home ------------' >> ~/output.txt
ls -l >> ~/output.txt
sudo docker load < docker_tar_image.tar
echo 'docker images ------------' >> ~/output.txt
sudo docker image ls >> ~/output.txt
echo '--------------------------' >> ~/output.txt

echo 'run test      ------------' >> ~/output.txt
sudo docker run --rm sebranchett/gpaw:one_processor_21.1.0 gpaw test >> ~/output.txt
echo '--------------------------' >> ~/output.txt

aws s3 cp ~/output.txt s3://seb-results-of-calculations
sudo shutdown -h now
