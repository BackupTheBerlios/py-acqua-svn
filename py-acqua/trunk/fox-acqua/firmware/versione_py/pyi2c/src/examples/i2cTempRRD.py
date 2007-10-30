#!/usr/bin/python
# -*- coding: Latin-1 -*-

import sys
import os
import time

import I2C
import I2C.sensors

rrdFile='temperature.rrd'
rrdDir='/data/temperature'


os.chdir(rrdDir)
sondes = []
sondes.append(I2C.sensors.LM75('Desktop', I2C.BusI2C('LPT1')))


step=60
if not os .path.isfile(rrdFile):
    cmd='rrdtool create %s --start %d --step %d '%(rrdFile,int(time.time()), step)   # step 60 = 1 minute
    for sonde in sondes:
        cmd+='DS:%s:GAUGE:900:-120:120 '%sonde.id
        cmd+='RRA:AVERAGE:0.5:%d:%d '%(5,3600*24/(step*5))             # 1 day, average on 5 mn
        cmd+='RRA:AVERAGE:0.5:%d:%d '%(60,3600*24*7/(step*60))         # 7 days, average on 60 mn
        cmd+='RRA:AVERAGE:0.5:%d:%d '%(24*60,3600*24*365/(step*24*60)) # 365 days / average on 24h
        cmd+='RRA:MAX:0.5:%d:%d '%(24*60,3600*24*365/(step*24*60))     # daily max / 365 days 
        cmd+='RRA:MIN:0.5:%d:%d '%(24*60,3600*24*365/(step*24*60))     # min journalier / 365 jours 
        cmd+='RRA:MAX:0.5:%d:%d '%(5,3600*24/step*5)                   # 24 h
        cmd+='RRA:MIN:0.5:%d:%d '%(5,3600*24/step*5)                   # 24 h
    os.system(cmd)


def mesure():
    for sonde in sondes:
        t=sonde.getTemperature()
        print 'T = %d C'%t
        os.system('rrdtool update %s -t %s N:%s'%(rrdFile,sonde.id, t))


def updateGraphs():
    os.system('rm %s/*png'%rrdDir)
    l = {0:'daily',  -604800:'weekly', -2419200:'monthly', -31449600:'yearly'}
    for s,n in l.items():
        cmd  = 'rrdtool graph %s.png --title="%s" -s%d '%(n,n,s) 
        for sonde in sondes:
            cmd += 'DEF:%s=%s:%s:AVERAGE:step=60 -v"°C" -aPNG  '%(sonde.id, rrdFile, sonde.id)
            cmd += 'LINE1:%s#00DD00:"%s" '%(sonde.id,sonde.id)
        os.system(cmd)



if __name__ == '__main__':
    i=0
    while True:
        i+=1
        mesure()
        if i>10:
            updateGraphs()
            i=0
        time.sleep(15)


