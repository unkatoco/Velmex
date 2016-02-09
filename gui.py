# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:51:44 2015

@author: koconnor
"""

import sys
from PyQt4 import QtGui, QtCore
from functools import partial
import velmex

windowHeight = 80
windowWidth = 100

stepSize = 1                # can be reset through interface
axis = [0,0,0]              # current position, reset at startup
axisName = ['X','Y','Z']

steps = 7                    # number of discreet values available on the slider
                            # follows the pattern 1,2,5,10,20,50...
                            # might look weird if <7

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        velmex.init()                       # open serial port
        for i in range (0,3):               # read startup motor positions
            axis[i] = velmex.getPos(i+1)

        self.initUI()
        
        
    def initUI(self):
        
        self.resize(windowWidth, windowHeight)
        self.center()
        self.setWindowTitle('Velmex')
         
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(10)
        for i in range (0,steps-1):
            grid.setColumnMinimumWidth(i,int(windowWidth/steps))
            grid.setColumnStretch(i,1)
         
        self.positionBox = []
        
        # sets up an identical set of controls for each axis
        for i in range (0,3):
            
             plus = QtGui.QPushButton('+', self)
             minus = QtGui.QPushButton('-', self)
             plus.clicked.connect(partial(self.buttonHandler, i))
             minus.clicked.connect(partial(self.buttonHandler, i))
        
             self.positionBox.append(QtGui.QLineEdit((str(axis[i])),self))
             self.positionBox[i].textChanged.connect(partial(self.posChanger, i))
            # self.positionBox[i].setFixedWidth(35)
             
             plus.setMinimumSize(25,25)
             minus.setMinimumSize(25,25)
             grid.addWidget(minus, i,1)
             grid.addWidget(plus, i,4)
             grid.addWidget(self.positionBox[i], i,2,1,2)
             
             lbl = QtGui.QLabel('     '+axisName[i])
             #lbl.setFont(QtGui.QFont('Arial',14, QtGui.QFont.Bold))
             grid.addWidget(lbl,i,0)  # X,Y,Z labels
                          
                   
        # step size text box
        self.ssBox = QtGui.QLineEdit(str(stepSize))
        self.ssBox.textChanged.connect(self.stepChanger)  
        self.ssBox.setFixedWidth(35)
        
        # slider, sets step size
        slide = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slide.setRange(0,steps-1)     
        slide.setTickPosition(3)
        slide.setTickInterval(1)
        slide.setPageStep(1)
        slide.valueChanged.connect(self.slideHandler)

        slbl = QtGui.QLabel('Step \nSize:')
        #slbl.setFont(QtGui.QFont('Arial',13, QtGui.QFont.Bold))

        grid.addWidget(slide, 3,0,2,steps)
        grid.addWidget(self.ssBox, 2,5,1,2)
        grid.addWidget(slbl,1,5,1,2)

        # labels for tick mark values        
        for i in range(0,steps):
            grid.addWidget(QtGui.QLabel(str((abs((i%3)*3-1))*10**int(i/3))),4,i)

 
        # "Set Home" button
        btn = QtGui.QPushButton('Set Home', self)   
        btn.clicked.connect(self.setHome)
        btn.setToolTip('Sets current position to zero')      
        grid.addWidget(btn, 5,1,1,3)
        
        # "Home All" button
        hBtn = QtGui.QPushButton('Home All', self)   
        hBtn.clicked.connect(self.home)
        hBtn.setToolTip('Sends all motors to their zero position')      
        grid.addWidget(hBtn, 5,4,1,3)
        
        # "Fire Laser" button
        laserBtn = QtGui.QPushButton('Fire Laser',self)
        grid.addWidget(laserBtn,6,1,1,3                                                 )
        
        self.show()
    
    def center(self):        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def closeEvent(self,event):
        velmex.end()                # close serial port
        event.accept()              # close window

           
    # called when a + or - button is presses
    def buttonHandler(self,j):
        global axis
        sender = self.sender()
        
        if sender.text() == '+':            # increment axis
            axis[j] += stepSize
            velmex.moveFor(j+1,stepSize)
        else:                               # decrement axis
            axis[j] -= stepSize
            velmex.moveFor(j+1,-1*stepSize)
            
        if velmex.limit():
            QtGui.QMessageBox.critical(self, "Warning","Limit switch encountered")
            axis[j] = velmex.getPos(j+1)
            
        self.positionBox[j].setText(str(axis[j]))
        
    # called when the stepsize slider is moved    
    def slideHandler(self,val):
        global stepSize
        val = (abs((val % 3)*3-1))*10**(val/3)  # bullshit algebra to map ticks to desired values
        stepSize = val
        self.ssBox.setText(str(val))        
        
    # called when a value is manually entered into the stepsize text box    
    def stepChanger(self,val):
        global stepSize        
        try:
            val = int(val)
            stepSize = int(val)  # reset step size
            #self.slide[j].setValue(int(2*math.log10(val)))
        except ValueError:
            if (val==''):           # if the box is empty, do nothing
                return
            # if they entered something other than an integer, show an error message
            QtGui.QMessageBox.critical(self, "ERROR","Please enter a positive integer")

    # called when a value is manually entered into the position text box    
    def posChanger(self,j,val):
        j = int(j)                      # axis index
        try:
            val = int(val)
            velmex.moveTo(j+1,val)      # move to entered position
        except ValueError:
            if (val==''):               # if the box is empty, do nothing
                return
            # if they entered something other than an integer, show an error message
            QtGui.QMessageBox.critical(self, "ERROR","Please enter an integer")

    # called when "Set Home" button is pressed
    def setHome(self):
        velmex.setHome()
        for i in range (0,3):
            axis[i] = 0
            self.positionBox[i].setText(str(axis[i]))

    # called when "Home All" button is pressed
    def home(self):
        velmex.homeAll()
        for i in range (0,3):
            axis[i] = 0
            self.positionBox[i].setText(str(axis[i]))
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    if app is None:
        app = QtGui.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    Dialog = QtGui.QDialog()
    #ui = Ui_Dialog()
    #ui.setupUi(Dialog)
    #Dialog.show()
    app.exec_()

   # sys.exit(app.exec_())


if __name__ == '__main__':
    main()