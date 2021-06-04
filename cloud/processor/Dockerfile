FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python3-dev python3-pip python3-opencv libopencv-dev vim mosquitto-clients 
RUN pip3 install paho-mqtt
RUN pip3 install numpy
RUN pip3 install boto3
WORKDIR /app

COPY processor.py ./
CMD ["python3","processor.py"]
