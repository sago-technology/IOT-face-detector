import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST="mosquitto-service"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="face-detector"

def on_connect_local(client, userdata, flags, rc):
    print("connected to local broker with rc: " + str(rc))
    client.subscribe(LOCAL_MQTT_TOPIC)

def on_message(client,userdata, msg):
  print('See message received here!')
  try:
    print("message received! {} bytes ".format(len(msg.payload)))
  except:
    print("Unexpected error:", sys.exc_info()[0])

print("Create new instance")
local_mqttclient = mqtt.Client()

print("Bind call back function")
local_mqttclient.on_connect = on_connect_local

print("Connect to broker")
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

print("Receiving message...")
local_mqttclient.on_message = on_message

local_mqttclient.loop_forever()
