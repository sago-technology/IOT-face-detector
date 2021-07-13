#!/bin/bash
kubectl delete deployment mosquitto-deployment
kubectl delete deployment face-detector 
kubectl delete deployment logger
kubectl delete deployment forwarder
kubectl delete service mosquitto-service
