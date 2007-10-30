#! /usr/bin/env python

import datetime, time
import I2C
import I2C.sensors
import pylab
import matplotlib
          

i2c=I2C.BusI2C('COM2')
i2c.bus.setSpeed(2000)
sonde=(I2C.sensors.LM75('kitchen', i2c))

line=None
X=[]
Y=[]

print 'Starting graphic interface, please wait ...'
pylab.ion()
while 1:
    t,h = sonde.getTemperature(), time.time()
    if t:
        X.append(matplotlib.dates.date2num(datetime.datetime.now()))    
        Y.append(t)  
        line, = pylab.plot_date(X, Y, fmt='-')
        pylab.title('Temp')
        pylab.xlabel('Date')
        pylab.ylabel('Temperature in %s (Celcius)'%sonde.id)

    if line:
        pylab.draw()
        time.sleep(10)



    
