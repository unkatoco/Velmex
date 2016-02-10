# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 10:31:40 2015

@author: koconnor

Creates a .exe file
"""


from distutils.core import setup
import py2exe
 
setup(windows=['gui.py'],options={"py2exe" : {"includes" : ["sip","PyQt4"]}})