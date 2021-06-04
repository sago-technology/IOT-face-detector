#!/bin/bash
docker build -t samueljgomez/forwarder-edge:alpine -f Dockerfile .
docker push samueljgomez/forwarder-edge:alpine
