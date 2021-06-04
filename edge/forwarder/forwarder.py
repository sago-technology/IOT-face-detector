import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST="mosquitto-service"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="face-detector"

REMOTE_MQTT_HOST="54.153.36.197"
REMOTE_MQTT_PORT=32746
REMOTE_MQTT_TOPIC="face-detector"


def on_connect_local(client, userdata, flags, rc):
    print("connected to local broker with rc: " + str(rc))
    client.subscribe(LOCAL_MQTT_TOPIC)


def on_message(client, userdata, msg):
  print("into on_message to be publish")
  try:
    print("message received! {} bytes ".format(len(msg.payload)))
    # if we wanted to re-publish this message, something like this should work
    msg = msg.payload
    remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0, retain=False)
  except:
    print("Unexpected error:", sys.exc_info()[0])

print("Creating local instance")
local_mqttclient = mqtt.Client()

print("Bind call back function")
local_mqttclient.on_connect = on_connect_local

print("Connect to local broker")
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

print("Creating remote instance")
remote_mqttclient = mqtt.Client()

print("Connect to remote broker")
remote_mqttclient.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)

print("Publishing message...")
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()
