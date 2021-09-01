"""
Author: Maurice Snoeren <macsnoeren(at)gmail.com>
Version: 0.1 beta (use at your own risk)
Date: 2021-08-31
"""
import time
import threading

import re
import json
import random
from   datetime import datetime, timezone
import dateutil
import paho.mqtt.client as mqtt # pip install paho-mqtt

from fsm import FSM

class FSMRecording(FSM):
    """FSMRecording implements a finite state machine based on FSM."""
    
    def __init__(self):
        super().__init__()

        # Add the transitions to the FSM
        self.add_transition("START",  "READY",    "IDLE")
        self.add_transition("IDLE",   "INITIATE", "LINK")
        self.add_transition("LINK",   "TIMEOUT",  "IDLE")
        self.add_transition("LINK",   "READY",    "WAIT")
        self.add_transition("WAIT",   "TIMEOUT",  "IDLE")
        self.add_transition("WAIT",   "LOGOUT",   "IDLE")
        self.add_transition("WAIT",   "START",    "RECORD")
        self.add_transition("RECORD", "TIMEOUT",  "IDLE")
        self.add_transition("RECORD", "STOP",     "SAVE")
        self.add_transition("SAVE",   "READY",    "WAIT")       
        self.set_state_start("START")

        # MQTT client
        self.mqtt = mqtt.Client()

        #mqtt.username_pw_set("server", password="servernode")
        self.mqtt.connect("test.mosquitto.org", 1883, 60)

        self.mqtt.subscribe("_rrs_/event", qos=0)

        self.mqtt.on_connect    = lambda client, userdata, flags, rc: self.mqtt_on_connect(client, userdata, flags, rc)
        self.mqtt.on_disconnect = lambda client, userdata, rc:        self.mqtt_on_disconnect(client, userdata, rc)
        self.mqtt.on_message    = lambda client, userdata, msg:       self.mqtt_on_message(client, userdata, msg)

        self.mqtt.loop_start() # Start the loop thread of MQTT

    def mqtt_on_connect(self, client, userdata, flags, rc):
        print("Connected with MQTT broker with result code " + str(rc) + ".")
        self.event("READY")

    def mqtt_on_disconnect(self, client, userdata, rc):
        print("Disconnected with MQTT broker with result code " + str(rc) + ".")
        self.event("ERROR")

    def mqtt_on_message(self, client, userdata, msg):
        print("got message: " + str(msg.topic) + ": " + str(msg.payload))

        try:
            data = json.loads(msg.payload)

            if msg.topic == "_rrs_/event":
                if "event" in data:
                    self.event(data["event"], data)
        except:
            print("mqtt_on_message: json error: " + msg.payload)
            return

    def idle_pre(self, data, test):
        pass

    def idle_loop(self):
        print("idle")
        self.event("INITIATE", {"data": "data"})

    def link_pre(self, data):
        print(str(data))
