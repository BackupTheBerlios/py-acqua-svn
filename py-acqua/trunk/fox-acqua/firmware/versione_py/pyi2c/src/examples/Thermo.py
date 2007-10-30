#! /usr/bin/env python
#
# python I2C serial port SDA/SCL mapping
#
# (C)2006 Patrick Nomblot <pyI2C@nomblot.org>
# this is distributed under a free software license, see license.txt


import time
import logging
import sys

import I2C
import I2C.sensors

#---------------------------------------------------------------------------

if __name__ == '__main__':

    logging.basicConfig()
    log = logging.getLogger("I2C")
    log.setLevel(logging.INFO)
    log.info("----- Thermomettre I2C ---------")

    sondes ={'Kitchen' : 0x90,
             'Bedroom' : 0x92, 
             'Outside' : 0x94}
    
    busI2C = I2C.BusI2C('LPT1')
    sondeList=[]
    for name, address in sondes.items():
        try:
            sondeList.append(I2C.sensors.LM75(name, busI2C, address))
        except I2C.ProtocolError:
            log.warning('Sonde %s does not respond !'%name)                   

    
    while 1:
        time.sleep(1)
        for sonde in sondeList: 
            log.info("%s : %02.03f"%(sonde.id, sonde.getTemperature()))

