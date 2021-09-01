"""
Author: Maurice Snoeren <macsnoeren(at)gmail.com>
Version: 0.1 beta (use at your own risk)
Date: 2021-08-31
"""

from time import sleep
from fsm_recording import FSMRecording 

fsm = FSMRecording()
while (True):
    fsm.loop()
    sleep(0.1)
    
