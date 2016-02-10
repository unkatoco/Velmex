# -*- coding: utf-8 -*-
"""
Functions for communicating with Velmex VP9000 controller

***NOTE THAT MOTORS ARE NOT 0-INDEXED***

"""

import serial
ser = serial.Serial()
motors = ['X','Y','Z','T' ]

def init():
    global ser
    # because they hate us, velmex uses communication protocals for their different controllers
    # for now just comment out the appropriate line
    ser = serial.Serial(0, 9600, bytesize=7 , parity='E', stopbits=2, timeout=.1) # vp9000
  #  ser = serial.Serial(0, 9600, bytesize=8 , parity='E', stopbits=1, timeout=.1) # vxm
    ser.write("F")  # enable online mode
    ser.write("C")  # clear current program


def moveFor (motor, distance):
    global ser
    ser.write("C")  # clear current program
    ser.write("I" + str(motor) + "M" + str(distance) + ",") # send movement command
    ser.write("R")  # run current program
    return

def moveTo (motor, destination):
    global ser
    ser.write("C")  # clear current program
    ser.write("IA" + str(motor) + "M" + str(destination) + ",") # send movement command
    ser.write("R")  # run current program
    return;

# send all motors to their zero positions
def homeAll():
    ser.write("C")  # clear current program
    for i in range (1,5):
        ser.write("IA" + str(i) + "M" + str(0) + ",") # send movement commands
    ser.write("R")  # run current program
    return
    
# sets registers to zero at current position
# I don't know why this kills the front panel display on the vp9000
def setHome():
    global ser
    ser.write("N")
    return
    
# returns the position of motor m    
def getPos (m):
    global ser
    wait()                   # wait for motors to finish moving
    ser.readline();          # clear current buffer
    ser.write(motors[m-1])   # query for position
    pos = ser.readline()
    sign=1                   # extract sign
    if pos[0]=='-':
        sign=-1
    pos = int(''.join([x for x in pos if x.isdigit()])) # parseint
    return sign*pos
   
# returns True if a motor just hit a limit switch
def limit():
    return (ser.readline()=='O')
 
# send motor to positive limit switch  
# TODO: see if this works if there are actual limit switches
def moveHome(motor):
    ser.write("C") 
    ser.write("I"+str(motor)+"M-0,")
    ser.write("R")    
    
# run current program
# CAUTION: only use if you're keeping track of what you just sent to the velmex
def go():
    ser.write("R")
    
def stop():
    ser.write("D")
   
# delay until current program is done   
def wait():
    global ser
    ser.readline()                  # clear current buffer
    ser.write('V')                  # query for velmex's status 
    while (ser.readline()=="B"):    # if busy,
        ser.write("V")              # keep waiting
    return
    
def end():
    global ser
    ser.write('Q')      # quit online mode
    ser.close()         # close serial port




