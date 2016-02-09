# -*- coding: utf-8 -*-
"""
Created on Fri Jan 08 13:41:33 2016

@author: koconnor
"""

import velmex
from xbox import xinputjoystick
import sys
import time
import threading


velmex.init()
speeds = [500,2000,6000]
guy = xinputjoystick()

for i in range (1,30):
    if guy.isupdatedalot():
        print guy.sticks[0]
        velmex.stop()
        velmex.setSpeed(1,speeds[abs(guy.sticks[0]/100000)])
        velmex.moveHome(1)
    time.sleep(1) 
    
velmex.end()