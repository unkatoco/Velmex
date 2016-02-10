# -*- coding: utf-8 -*-
"""
Created on Tue Feb 09 10:59:14 2016

@author: koconnor
"""

<<<<<<< HEAD
=======
COM  = 1    # com port used to communicate with the microcontroller

'''
SERIAL COMMAND SUMMARY

    LSR         fire laser
    ARON        argon on
    AROFF       argon off
    WELD 1       weld schedule #1
    WELD 2       weld schedule #2
    WELD 3       weld schedule #3
    WELD 4       weld schedule #4
    WELD 5       weld schedule #5
    WELD 6       weld schedule #6
    WELD 7       weld schedule #7
    WELD 8       weld schedule #8

terminate with \n
'''

import serial
import time

ser = serial.Serial()


def init():
    global ser
    ser = serial.Serial(COM,9600);
    

def setWeldSchedule(schedule):
    ser.write('WELD '+str(schedule)+'\n')



def end():
    ser.close()
>>>>>>> refs/remotes/origin/master
