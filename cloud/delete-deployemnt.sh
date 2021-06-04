#!/bin/bash
kubectl delete deployment mosquitto-deployment
kubectl delete deployment processor-deployment
kubectl delete service mosquitto-service
#kubectl delete deployment listener
