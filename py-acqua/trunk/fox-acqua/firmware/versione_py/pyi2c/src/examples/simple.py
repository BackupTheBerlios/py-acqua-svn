#! /usr/bin/env python
#
# python I2C serial port SDA/SCL mapping
#
# (C)2006 Patrick Nomblot <pyI2C@nomblot.org>
# this is distributed under a free software license, see license.txt


import I2C
import I2C.sensors


# I2C bus on serial com 2
i2cBus = I2C.BusI2C('COM2')

# LM75 I2C omponent on this I2C bus, default I2C address
sonde = I2C.sensors.LM75('Room temperature', i2cBus)

# print Temperature
print "T =  %02.03f C" % sonde.getTemperature()
