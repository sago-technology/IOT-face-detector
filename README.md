## Objective:  
Build a lightweight containerized application and data pipeline using MQTT and Kubernetes that streams video from components running on the edge to the cloud.  Edge components include an NVIDIA Jetson and webcam that uses a face recognition algorithm to capture faces.  The .png captures are then sent to an EC2 instance on AWS and stored in S3 object storage. 

![image](https://user-images.githubusercontent.com/59423299/120256600-56cffa00-c243-11eb-87b7-6408918aa135.png)

## System Architecture Breakdown
### Edge
#### USB Camera
#### Jetson - Kubernetes
1. Face Detector 
	- system: ubuntu
	- files: 
		- Dockerfile
		- face-detector.py
		- face-detector.yaml 
		- haarcascade_frontalface_default.xml
2. Message Logger
	- system: alpine	
	- files:
		- Dockerfile
		- logger.py
		- logger.yaml
3. MQTT Forwarder
	- system: alpine
	- files:
		- forwarder.py
		- forwarder.yaml
4. MQTT Broker
	- system: alpine
	- files:
		- Dockerfile
		- mosquitto-deployment.yaml
		- mosquitto-service.yaml 

### Cloud
#### AWS EC2 Ubuntu t2.large
1. Image Processor 
	- system: ubuntu
	- files:
		- processor.py
		- processor-deployment.yaml
2. MQTT Broker
	- system: alpine
	- files:
		- Dockerfile
		- mosquitto-deployment.yaml
		- mosquitto-service.yaml 

#### S3 - Simple Storage System
1. sgomez-w251-hw03

## Sequence of Operations
### Edge
#### 1. Build Container - Example Using Shell Script
```
#!/bin/bash
docker build --no-cache -t samueljgomez/forwarder-edge:alpine -f Dockerfile .
docker push samueljgomez/forwarder-edge:alpine
```

#### 2. Deploy Containers Into Kubernetes
```
kubectl apply -f edge/broker/mosquitto-deployment.yaml
kubectl apply -f edge/broker/mosquitto-service.yaml
kubectl apply -f edge/face-detector/face-detector.yaml
kubectl apply -f edge/logger/logger.yaml
kubectl apply -f edge/forwarder/forwarder.yaml

# view nodes and pods
kubectl get nodes
kubectl get pods

# troubleshooting commands
kubectl logs -f <PodName>
kubectl exec -it <PodName> -- bash
kubectl delete deployment <deployment name>
kubectl delete service <service name>
```
### Cloud
#### 1. EC2 Setup
```
aws ec2 create-security-group --group-name PublicSG --description "Bastion Host Security group" --vpc-id <vpc-id>

aws ec2 authorize-security-group-ingress --group-id <PublicGroupID> --protocol tcp --port 22 --cidr 0.0.0.0/0

aws ec2 run-instances --image-id ami-0bcc094591f354be2 --instance-type t2.large --security-group-ids <YOUR_PUBLIC_GROUP_ID> --associate-public-ip-address --key-name <YOUR_KEY_NAME>

ssh -A ubuntu@ec2-34-239-169-230.compute-1.amazonaws.com

# install docker and login to dockerhub

# expose port mosquitto NodePort
aws ec2 authorize-security-group-ingress --group-id <PublicGroupID> --protocol tcp --port 32746 --cidr 0.0.0/0.0
```
#### 2. Create User Defined Network
```
# creating a network enables containers to access one another using container name
docker network create mqtt
```

#### 3. Build More Docker Containers
```
#!/bin/bash
docker build --no-cache -t samueljgomez/processor-ec2:ubuntu -f Dockerfile .
docker push samueljgomez/processor-ec2:ubuntu
```

#### 4. Mount S3 - not fun, but GREAT when it worked
```
'''
Create S3 bucket (sgomez-w251-hw03). Add IAM role to EC2 instance (s3MountBucket) using policy AmazonS3FullAccess.  
I also added the AmazonS3FullAccess to my user permissions
'''

# now back to the instance

# download s3fs-fuse to VI
sudo apt install s3fs

# follow these steps
echo ACCESS_KEY_ID:SECRET_ACCESS_KEY > ${HOME}/.passwd-s3fs
chmod 600 ${HOME}/.passwd-s3fs

# verify buckets
aws s3 ls

# this is where the magic happens--took hours to figure out
sudo s3fs sgomez-w251-hw03 /mnt/sgomez-w251-hw03/ -o iam_role="s3MountBucket" -o url="https://s3.us-west-1.amazonaws.com" -o endpoint=us-west-1 -o dbglevel=info -o curldbg -o allow_other -o use_cache=/tmp -o nonemptydoc
```
https://sgomez-w251-hw03.s3-us-west-1.amazonaws.com/face-57.png

![image](https://user-images.githubusercontent.com/59423299/120272820-84786b80-c262-11eb-992a-44cb9b22b56e.png)

#### 5. Run Containers
```
# run broker using user-defined network and expose port to outside 
docker run -it --rm --name broker --hostname broker --network mqtt -p 32746:1883 samueljgomez/mosquitto-ec2:alpine 

# run image processor using user-defined network and volume mount
docker run -it --rm --name processor --hostname processor --network mqtt -v /mnt/sgomez-w251-hw03:/mnt/sgomez-w251-hw03 samueljgomez/processor-ec2:ubuntu
```

### MQTT Overview
#### What is MQTT?

MQTT is a simple messaging protocol, designed for constrained devices with low-bandwidth. So, it’s the perfect solution for Internet of Things applications. MQTT allows you to send commands to control outputs, read and publish data from sensor nodes and much more.

#### Quality of Service
The Quality of Service (QoS) level is an agreement between the sender of a message and the receiver of a message that defines the guarantee of delivery for a specific message. There are 3 QoS levels in MQTT:

At most once (0)
At least once (1)
Exactly once (2).

***The QoS used in this project was 0.***. 

The following code reflects this statement:
```
local_mqttclient.publish(LOCAL_MQTT_TOPIC, msg, qos=0, retain=False)
```

Use QoS 0 when …  
	- You have a completely or mostly stable connection between sender and receiver. A classic use case for QoS 0 is connecting a test client or a front end application to an MQTT broker over a wired connection.
	- You don’t mind if a few messages are lost occasionally. The loss of some messages can be acceptable if the data is not that important or when data is sent at short intervals
	- You don’t need message queuing. Messages are only queued for disconnected clients if they have QoS 1 or 2 and a persistent session.  
	
Use QoS 1 when …  
	- You need to get every message and your use case can handle duplicates. QoS level 1 is the most frequently used service level because it guarantees the message arrives at least once but allows for multiple deliveries. Of course, your application must tolerate duplicates and be able to process them accordingly.
	- You can’t bear the overhead of QoS 2. QoS 1 delivers messages much faster than QoS 2.  
	
Use QoS 2 when …  
	- It is critical to your application to receive all messages exactly once. This is often the case if a duplicate delivery can harm application users or subscribing clients. Be aware of the overhead and that the QoS 2 interaction takes more time to complete.


![Screen Shot 2021-05-31 at 10 18 07 PM](https://user-images.githubusercontent.com/59423299/120270231-1631aa00-c25e-11eb-953f-334b952a8d83.png)

#### Topics  
In MQTT, the word topic refers to an UTF-8 string that the broker uses to filter messages for each connected client.  In this project, I used the topic ***"face-detector"***.  I chose this because it was obvious to describe the face-detector sensor (webcam and haarcascade_frontalface_default act as a sensor).  The topic is defined on the publisher and subscriber.  

```
# publisher code snippet
LOCAL_MQTT_HOST="mosquitto-service"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="face-detector

# subscriber code snipper
LOCAL_MQTT_HOST="18.144.11.212"
MQTT_PORT=1883
MQTT_TOPIC="face-detector"
```

