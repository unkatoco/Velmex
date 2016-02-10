# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import ctypes
import numpy as np
import copy
from numba import jit

# define required ctype sturcts, structs according to
# http://msdn.microsoft.com/en-gb/library/windows/desktop/ee417001%28v=vs.85%29.aspx

class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ('buttons', ctypes.c_ushort),  # wButtons
        ('left_trigger', ctypes.c_ubyte),  # bLeftTrigger
        ('right_trigger', ctypes.c_ubyte),  # bLeftTrigger
        ('l_thumb_x', ctypes.c_short),  # sThumbLX
        ('l_thumb_y', ctypes.c_short),  # sThumbLY
        ('r_thumb_x', ctypes.c_short),  # sThumbRx
        ('r_thumb_y', ctypes.c_short),  # sThumbRy
    ]

class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ('packet_number', ctypes.c_ulong),  # dwPacketNumber
        ('gamepad', XINPUT_GAMEPAD),  # Gamepad
    ]

class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]

# connect to windows xinput dll may need to alter depending on available version
xinput = ctypes.windll.xinput9_1_0  
#xinput = ctypes.windll.xinput1_3

# define ctype XInputSetState function
XInputSetState = xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
XInputSetState.restype = ctypes.c_uint

ERROR_DEVICE_NOT_CONNECTED = 1167
ERROR_SUCCESS = 0

#dictionary to decode buttons. Gave some buttons multiple valid names, just 'cause
buttondict = {'dpad_up':1,
                'dpad_down':2,
                'dpad_left':4,
                'dpad_right':8,
                'up':1,
                'down':2,
                'left':4,
                'right':8,
                'start':16,
                'back':32,
                'l_stick':64,
                'r_stick':128,
                'l':256,
                'r':512,
                'a':4096,
                'b':8192,
                'x':16384,
                'y':32768,
                'left_button':256,
                'right_button':512,
                'a_button':4096,
                'b_button':8192,
                'x_button':16384,
                'y_button':32768}

@jit(cache=True,nopython=True)
def applydeadband(valarray,deadband):
    "function to scale joystick deadband, with some numba jit for speed boost"
    signarray=np.sign(valarray)
    valarray=np.abs(valarray)-deadband
    valarray[valarray<0]=0
    return valarray*signarray

class xinputjoystick(object):
    """
    class for xbox or other xinput joystick. Selects joystick id 0 by defualt,
    otherwise pass 0-3 into constructor
    """
    def __init__(self,joystickid=0):
        self.state = XINPUT_STATE()
        self.stickdeadzone=5000
        self.triggerdeadzone=5
        self.sticks = np.array([0,0,0,0])
        self.triggers = np.array([0,0])
        self.buttons = 0
        self._oldpacket = 0
        self._oldsticks = self.sticks.copy()
        self._oldtriggers = self.triggers.copy()
        self._oldbuttons = self.buttons
        self.getstate()
        
              
    def getstate(self):
        """
        backs up prior state, gets new state, and applies deadband to sticks
        and triggers. Stores results in sticks (4 element np array in format
        [leftx,lefty,rightx,righty]),triggers (2 element np array [left,right])
        and buttons (16 bit integer, each bit is a button state)
        """
        self._oldpacket = self.state.packet_number
        self._oldsticks = self.sticks.copy()
        self._oldtriggers = self.triggers.copy()
        self._oldbuttons = self.buttons
        res = xinput.XInputGetState(0, ctypes.byref(self.state))
        if res == ERROR_SUCCESS:
            if self.state.packet_number > self._oldpacket:
                #print(hex(self.state.gamepad.buttons))
                self.sticks = np.array([self.state.gamepad.l_thumb_x, self.state.gamepad.l_thumb_y,
                           self.state.gamepad.r_thumb_x, self.state.gamepad.r_thumb_y])
                self.triggers = np.array([self.state.gamepad.left_trigger, 
                                          self.state.gamepad.right_trigger])
                self.buttons = self.state.gamepad.buttons
                self.sticks = applydeadband(self.sticks,self.stickdeadzone)
                self.triggers = applydeadband(self.triggers, self.triggerdeadzone)
                self.packet = self.state.packet_number
            return
        if res == ERROR_DEVICE_NOT_CONNECTED:
            raise RuntimeError(
                "Error %d device not connected" % (res))
    def isupdated(self):
        "Gets state then returns True if state has changed from previous"
        self.getstate()
        return (np.any(self._oldsticks != self.sticks) or 
            np.any(self._oldtriggers != self.triggers) or self.buttons != self._oldbuttons)
                    
    # for testing                
    def isupdatedalot(self):
        self.getstate()
        return abs(self._oldsticks[0]-self.sticks[0])>8000                    
                    
    def ispressed(self,key):
        """
        use buttondict to decode button, return true if that button pressed
        Invalid key does NOT throw an error, just returns false
        Does not recheck state, uses most recent status
        """
        
        if (self.buttons & b0uttondict.get(key,0)): return True
        else: return False        
        
    def set_vibration(self, left_motor, right_motor):
        "Control the speed of both motors seperately"
        left_motor=np.clip(left_motor,0,1)
        right_motor=np.clip(right_motor,0,1)       
        vibration = XINPUT_VIBRATION(
            int(left_motor * 65535), int(right_motor * 65535))
        XInputSetState(0, ctypes.byref(vibration))              
                
                
                