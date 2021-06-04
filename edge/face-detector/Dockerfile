FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt install -y python3-dev python3-pip  python3-opencv vim-tiny  libopencv-dev
RUN pip3 install numpy 
RUN apt install -y mosquitto-clients
RUN pip3 install paho-mqtt
RUN pip3 install Cython

WORKDIR /app
COPY *.xml ./
COPY *.py ./
RUN chmod 700 *.*
CMD python3 text.py
