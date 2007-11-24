#Copyright (C) 2005, 2006 Luca Sanna - Italy
#http://pyacqua.altervista.org
#email: pyacqua@gmail.com  
#
#   
#Py-Acqua is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#Py-Acqua is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Py-Acqua; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#*************************************************

#***********************************************************************************
# 
#  TEST DEL LCD PILOTATO IN I2C DAL CHIP MCP230016. si mcp230016 con 16 i/o
#
#***********************************************************************************

import time
from i2c_py import *
from mcp23016 import *
from routine_lcd import *

#Collegamenti elettrici:
#IOG25 J7.13 as SCL
#IOG24 J7.21 as SDA. 

#RESISTENZE DI PULLUP SU I2C DI 1K !

#di fabbrica tt i pin sono configurati in ingresso

#PIN A0,A1,A2 A VCC
#RESET A VCC

#*****************
#		MAIN
#*****************


while 1:
	print("GESTIONE MCP23016\n")
	print("Operazioni possibili:\n")
	print("1:TEST\n")
	print("2:Pulsanti\n")
	print("3:Esci\n\n")
	#print("Scelta = ")
	scelta = raw_input("Scelta =")
	if (scelta=="1"):
		i2c_init()
		lcd_init()
		lcd_printf("Ciao")
		print("Frase  di prova scritta\n");
	else:
		pass	
	if (scelta=="2"):
		i2c_init()
		print("GPIO1= %s\n" %(mcp23016_regLeggi(id, mcp23016GPIO1)))
	else:
		pass
	if (scelta=="3"):
		i2c_close()
		sys.exit(0)
