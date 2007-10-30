#! /usr/bin/env python
#
# python I2C serial port SDA/SCL mapping
#
# (C)2006 Patrick Nomblot <pyI2C@nomblot.org>
# this is distributed under a free software license, see license.txt

import I2C
import I2C.sensors




def temperature(port, address=None):
    i2cBus = I2C.BusI2C(port)

    # check / find I2C component from I2C address 0x90
    I2Caddress = i2cBus.scan(0x90)

    sonde = I2C.sensors.LM75('Room temperature', i2cBus, I2Caddress)
    return sonde.getTemperature()




print 'Available interfaces : ', ','.join(I2C.interfaces)
for interface in I2C.interfaces:
    try:
        print 'Looking for I2C LM75 on', interface
        print "Found LM75 : T =  %02.03f C" % temperature(interface)
    except I2C.ProtocolError:
        print 'Nothing found !'
