# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 12:25:28 2015

@author: NKiner
"""
import velmex
from xbox import xinputjoystick
import sys
import time
import threading

# Hey!
def listen(e):
    print 'listen'
    #sys.stdout.flush()
    for i in range(0,300):
        #print 'hey'
        if guy.isupdated():
            e.clear()
            print guy.sticks[0]
            #sys.stdout.write("\r"+str(guy.sticks[0]))#,guy.sticks[1],guy.sticks[2],guy.sticks[3], 
              #   guy.triggers[0],guy.triggers[1],guy.buttons))
            #sys.stdout.flush()

            velmex.setSpeed(guy.sticks[0])
            e.set()
        time.sleep(.1)

def goTime(e):
    #print 'go'
    for i in range(0,10000): #(guy.sticks[0]!=0):
        #print 'go'
        #if (e.isSet() and guy.sticks[0]!=0): 
            #print "go"
            #velmex.go()
        time.sleep(.002) # 9600 baud rate

print "hello?  world?"

velmex.init()
guy = xinputjoystick()
print 0
e = threading.Event()
print 1
#sys.stdout.flush()
print 2
t1 = threading.Thread(name='velmex',target=goTime,args=(e,))
t2 = threading.Thread(name='xbox',target=listen,args=(e,))
#sys.stdout.flush()

print "hey"
t1.start()
#sys.stdout.flush()
t2.start()

# This does weird things to my print statements :/
#t1.join()
#t2.join()
#velmex.close()


'''
while True:
    if guy.isupdated():    
        sys.stdout.write("\r %6d %6d %6d %6d %3d %3d %5d" % (guy.sticks[0],guy.sticks[1],guy.sticks[2],guy.sticks[3], 
             guy.triggers[0],guy.triggers[1],guy.buttons))
        velmex.setSpeed(1,guy.sticks[0]/4)
        sys.stdout.flush()
    #if (guy.sticks[0]!=0):
    #    velmex.go()
    time.sleep(0.02)
'''
        
         