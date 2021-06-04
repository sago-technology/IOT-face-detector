#!/bin/bash
kubectl apply -f ~/github/w251-hw03/cloud/broker/mosquitto-deployment.yaml
kubectl apply -f ~/github/w251-hw03/cloud/broker/mosquitto-service.yaml
kubectl apply -f ~/github/w251-hw03/cloud/processor/processor-deployment.yaml
#kubectl apply -f ~/github/w251-hw03/cloud/listener/listener.yaml
