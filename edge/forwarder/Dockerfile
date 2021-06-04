FROM alpine:latest
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apk add python3 py3-pip
RUN pip3 install paho-mqtt
COPY ./forwarder.py ./
CMD python3 forwarder.py
