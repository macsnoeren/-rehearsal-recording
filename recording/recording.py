import time
import threading

import re
import json
import random
from datetime import datetime, timezone
import dateutil
import paho.mqtt.client as mqtt # pip install paho-mqtt

from fsm import FSM 

"""
Author: Maurice Snoeren <macsnoeren(at)gmail.com>
Version: 0.1 beta (use at your own risk)
Date: 2021-08-31
"""

def start_pre():
    print("start_pre")

def start_loop():
    print("start_loop")

def start_post():
    print("start_post")

def test_pre():
    print("test_pre")

def test_loop():
    print("test_loop")

def test_post():
    print("test_post")


# MQTT client
mqtt = mqtt.Client()

#mqtt.username_pw_set("server", password="servernode")
mqtt.connect("test.mosquitto.org", 1883, 60)

mqtt.subscribe("_rrs_/commands", qos=0)

mqtt.on_connect = lambda client, userdata, flags, rc: mqtt_on_connect(client, userdata, flags, rc)
mqtt.on_disconnect = lambda client, userdata, rc:     mqtt_on_disconnect(client, userdata, rc)
mqtt.on_message    = lambda client, userdata, msg:    mqtt_on_message(client, userdata, msg)

def mqtt_on_connect(client, userdata, flags, rc):
    print("Connected with MQTT broker with result code " + str(rc) + ".")

def mqtt_on_disconnect(client, userdata, rc):
    print("Disconnected with MQTT broker with result code " + str(rc) + ".")

def mqtt_on_message(client, userdata, msg):
    print("got message: " + str(msg.topic) + ": " + str(msg.payload))

    #try:
    #    plJson = json.loads(msg.payload)
    #except:
    #    print("Error processing node data: " + msg.payload)
    #    return

mqtt.loop_start() # Start the loop thread of MQTT
print("Started")

mqtt.publish("_rrs_/device", json.dumps({"device": "device"}))

fsm = FSM()
fsm.add_state("START", start_pre, start_loop, start_post)
fsm.add_state("TEST", test_pre, test_loop, test_post)
fsm.set_state_start("START")
fsm.add_transition("START", "SIGNAL", "TEST")
fsm.add_transition("TEST",  "SIGNAL", "START")

while True:
    fsm.event("SIGNAL")
    time.sleep(5)    
    
#time.sleep(10)

mqtt.loop_stop() # Stop the loop thread of MQTT
print("Stopped")
