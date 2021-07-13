#!/bin/bash
kubectl apply -f broker/mosquitto-service.yaml
kubectl apply -f broker/mosquitto-deployment.yaml
kubectl apply -f face-detector/face-detector.yaml
kubectl apply -f logger/logger.yaml
kubectl apply -f forwarder/forwarder.yaml
kubectl get service
sleep 7
kubectl get pods
