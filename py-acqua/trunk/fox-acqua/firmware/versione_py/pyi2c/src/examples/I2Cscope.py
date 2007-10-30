#! /usr/bin/env python
#
# python I2C serial port SDA/SCL mapping
#
# (C)2006 Patrick Nomblot <pyI2C@nomblot.org>
# this is distributed under a free software license, see license.txt

import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))


import I2C
import I2C.sensors
import pyScope


i2cBus = I2C.BusI2C('LPT1')
sonde = None


def lm75():
    global sonde
    try:
        sonde = I2C.sensors.LM75('Room temperature', i2cBus, pauseBackground=0)
        scope.result.config(text="%s initialised"%sonde.id )
    except I2C.ProtocolError, msg:
        scope.result.config(text=msg)

def temperature():
    try:
        scope.result.config(text="T =  %02.03f C" % sonde.getTemperature())
    except I2C.ProtocolError, msg:
        scope.result.config(text=msg)



# make graph easier to read with colors
# -------------------------------------
scopeColors= {	'_start'    : '#00FF00', 
		'_send'     : '#CCCCFF',
		'_read'     : '#33FFFF',
		'_ack'      : '#00FFFF',
		'_sendAck'  : '#FFFF00',
		'_sendNack' : '#FF0000',
		'_stop'     : '#0000FF'}



scope = pyScope.multiChanelScope('I2C scope')
scope.connect(i2cBus.bus, 'write', ('scl', 'sda'), scopeColors)
scope.addAction('initialize LM75', lm75)
scope.addAction('read I2C temperature', temperature)
scope.result.config(text=" ")
scope.show()

