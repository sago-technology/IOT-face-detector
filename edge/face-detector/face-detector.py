import numpy as np
import cv2
import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST="mosquitto-service"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="face-detector"

def on_connect_local(client, userdata, flags, rc): 
    print("connected to local broker with rc: " + str(rc))
 
local_mqttclient = mqtt.Client()
local_mqttclient.loop_start()
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_connect = on_connect_local

cam = cv2.VideoCapture(0, cv2.CAP_V4L2)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while(True):
    # Capture frame-by-frame
    ret, frame = cam.read()

    # Encode and send frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        face = gray[y:y+h, x:x+w]
        rc,png = cv2.imencode('.png', face)
        msg = png.tobytes()
        print(msg)
        try:
            local_mqttclient.publish(LOCAL_MQTT_TOPIC, msg, qos=0, retain=False)
        except Exception as e:
            print(e)

# Release capture when done
cap.release()
cv2.destroyAllWindows()
