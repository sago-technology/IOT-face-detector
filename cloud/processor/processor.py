import paho.mqtt.client as mqtt
import boto3
import cv2 as cv
import numpy as np
import math

s3client = boto3.client('s3')

LOCAL_MQTT_HOST="broker"
MQTT_PORT=1883
MQTT_TOPIC="face-detector"

counter = 0

def on_connect_local(client, userdata, flags, rc):
    print("connected to local broker with rc: " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client,userdata, msg):
    print("Let's save some images...")
    global counter
    try:
        print("message received! {} bytes".format(len(msg.payload)))
        # now we need to write the msg to s3
        msg = np.frombuffer(msg.payload, dtype='uint8')
        img = cv.imdecode(msg, flags=1)
        print(img.shape)
        img_name = "face-" + str(counter) + ".png"
        print(f"{img_name}")
        counter+= 1
        cv.imwrite('/mnt/sgomez-w251-hw03/'+img_name, img)
        print("got msg")
    except Exception:
        print("Unexpected error:", sys.exec_info()[0])


print("Create new instance")
local_mqttclient = mqtt.Client()

print("Bind call back function")
local_mqttclient.on_connect = on_connect_local

print("Connect to broker")
local_mqttclient.connect(LOCAL_MQTT_HOST, MQTT_PORT, 60)

print("Saving images!")
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()
