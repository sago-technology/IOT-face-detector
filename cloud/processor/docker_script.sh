#!/bin/bash
docker build --no-cache -t samueljgomez/processor-ec2:ubuntu -f Dockerfile .
sudo docker push samueljgomez/processor-ec2:ubuntu
sudo docker pull samueljgomez/processor-ec2:ubuntu
