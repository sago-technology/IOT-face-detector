FROM alpine:latest
# this is needed to make sure we can see the log output
ENV PYTHONUNBUFFERED=1
WORKDIR /app
#RUN a command to intall the MQTT python client 
RUN apk add --no-cache python3
RUN apk add  py3-pip
RUN pip3 install paho-mqtt
# Copy your listener.py file into the container
COPY logger.py ./
#run listener.py
CMD python3 logger.py
