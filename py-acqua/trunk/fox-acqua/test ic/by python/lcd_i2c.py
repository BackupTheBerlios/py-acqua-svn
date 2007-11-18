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



#Collegamenti elettrici:
#IOG25 J7.13 as SCL
#IOG24 J7.21 as SDA. 

#RESISTENZE DI PULLUP SU I2C DI 1K !

#di fabbrica tt i pin sono configurati in ingresso

#PIN A0,A1,A2 A VCC
#RESET A VCC

#****************************************************

lcdMcp23016_id	= 0x20

# RIFLETTE IL LIVELLO LOGICO DEL PIN
# 1 = livello logico alto
# 0 = livelLo logico basso
GPIO0	= 0X00
GP07	= 7
GP06	= 6
GP05	= 5
GP04	= 4
GP03	= 3
GP02	= 2
GP01	= 1
GP00	= 0
GPI01	= 0X01
GP17	= 7
GP16	= 6
GP15	= 5
GP14	= 4
GP13	= 3
GP12	= 2
GP11	= 1
GP10	= 0
# ACCEDE AL VALORE DEI LATCH DI USCITA
# 1 = livello logico alto
# 0 = livelLo logico basso
OLAT0	= 0X02  #LATCH
OL07	= 7
OL06	= 6
OL05	= 5
OL04	= 4
OL03	= 3
OL02	= 2
OL01	= 1
OL00	= 0
OLAT1	= 0X03  #LATCH
OL17	= 7
OL16	= 6
OL15	= 5
OL14	= 4
OL13	= 3
OL12	= 2
OL11	= 1
OL10	= 0
# INVERTE LETTURA
# 1 = riflette il livello logico opposto a quello presente sul pin quando si legge GPIO
# 0 = lettura = stato del pin
IPOL0	= 0X04	
IP07	= 7
IP06	= 6
IP05	= 5
IP04	= 4
IP03	= 3
IP02	= 2
IP01	= 1
IP00	= 0
IPOL1	= 0X05
IP17	= 7
IP16	= 6
IP15	= 5
IP14	= 4
IP13	= 3
IP12	= 2
IP11	= 1
IP10	= 0
#REGISTRI
#x impostare direzione
# 1 = input
# 0 = output
IODIR0	= 0X06	
IO07	= 7
IO06	= 6
IO05	= 5
IO04	= 4
IO03	= 3
IO02	= 2
IO01	= 1
IO00	= 0
IODIR1	= 0X07	
IO17	= 7
IO16	= 6
IO15	= 5
IO14	= 4
IO13	= 3
IO12	= 2
IO11	= 1
IO10	= 0
# RIFLETTE I LIVELLI LOGICI DEI PIN IMPOSTATI COME INTERRUPT AL MOMENTO DEL CAMBIAMENTO DI STATO
# 1 = attivo alto
# 0 = attivo basso
INTCAP0	= 0X08	#SOLA LETTURA
ICP07	= 7
ICP06	= 6
ICP05	= 5
ICP04	= 4
ICP03	= 3
ICP02	= 2
ICP01	= 1
ICP00	= 0
INTCAP1	= 0X09	#SOLA LETTURA
ICP17	= 7
ICP16	= 6
ICP15	= 5
ICP14	= 4
ICP13	= 3
ICP12	= 2
ICP11	= 1
ICP10	= 0
# SETTA LA VELOCITÀ CON CUI CAMPIONA GLI INGRESSI IMPOSTATI COME INTERRUPT X GENERARE L'INTERRUPT
# 1 = lento (32ms)
# 0 = veloce (200us)
IOCON0	= 0X0A
IARES0	= 0
IOCON1	= 0X0B
IARES1	= 0

#***************
#LCD PIN
#**************

lcd_E		= GP00
lcd_RS	=	GP01
lcd_D4	=	GP02
lcd_D5	=	GP03
lcd_D6	=	GP04
lcd_D7	=	GP05
  


CLOCK_LOW_TIME        =    8
CLOCK_HIGH_TIME        =   8
START_CONDITION_HOLD_TIME = 8
STOP_CONDITION_HOLD_TIME  = 8
ENABLE_OUTPUT = 0x01
ENABLE_INPUT = 0x00
I2C_CLOCK_HIGH = 1
I2C_CLOCK_LOW = 0
I2C_DATA_HIGH = 1
I2C_DATA_LOW = 0


#I2C_DATA_LINE    =   1<<24
#I2C_CLOCK_LINE   =   1<<17

#ifndef IO_SETGET_INPUT
#define IO_SETGET_INPUT   0x12
#endif
#ifndef IO_SETGET_OUTPUT
#define IO_SETGET_OUTPUT  0x13
#endif

#define i2c_delay(usecs) usleep(usecs)


#-----------------------------
#FUNZIONI
#-----------------------------

#*********************
#  MCP23016 ROUTINES
#*********************
def mcp23016_regLeggi(reg):
	i2c_start()
	i2c_outbyte(lcdMcp23016_id<<1)# accoda uno zero x dire scrivi
	i2c_outbyte(reg)
	i2c_start()
	i2c_outbyte((lcdMcp23016_id<<1)+1)# accoda un uno  x dire leggi 
	data=i2c_inbyte(0)
	i2c_stop()
	return data


def mcp23016_regScrivi(registro, value):
	i2c_start()
	i2c_outbyte(lcdMcp23016_id<<1)
	i2c_outbyte(registro)
	i2c_outbyte(value)
	i2c_stop()

def mcp23016_ttOut():
	mcp23016_reScrivi(IODIR0,0)
	mcp23016_regcrivi(IODIR1,0)

def mcp23016_ttIn():
	mcp23016_regScrivi(IODIR0,255)
	mcp23016_regScrivi(IODIR1,255)


def mcp23016_pinWriteLevel(GP,pin,level):
	value=mcp23016_leggiGpio(GP)
	value = level<<pin
	mcp23008_scrivi(GP,value)

def mcp23016_scriviGpio(GP,value):
	mcp23016_scrivi(IODIR0+GP,value)


def mcp23016_leggiGpio(GP):
	gpio_level=mcp23016_leggiGpio(GPIO0+GP)
	return gpio_level


def lcdMcpInit():
	pass
#init input x 5 pulsanti
#init output x fili al display


#*********************************************************************
# LCD functions
#*********************************************************************

#RS line
def lcd_rs(level) :
	mcp23016_pinWriteLevel(0,lcd_RS,level)
#E line
def lcd_e(level):
	mcp23016_pinWriteLevel(0,lcd_E,level)
#D4..7
def lcdD4(level):
	mcp23016_pinWriteLevel(0,lcd_D4,level)
def lcdD5(level):
	mcp23016_pinWriteLevel(0,lcd_D5,level)
def lcdD6(level):
	mcp23016_pinWriteLevel(0,lcd_D6,level)
def lcdD7(level):
	mcp23016_pinWriteLevel(0,lcd_D7,level)

def lcd_e_strobe():
	lcd_e(1)
	lcd_e(0)

# Send a nibble (4 bit) to LCD
def lcd_put_nibble(value):
	if (value&0x01):
		lcdD4(1)
	else:
		lcdD4(0)
	if (value&0x02):
		lcdD5(1)
	else:
		lcdD5(0);
	if (value&0x04):
		lcdD6(1)
	else:
		lcdD6(0)
	if (value&0x08):
		lcdD7(1)
	else:
		lcdD7(0)


# Send a char to LCD
# data: Ascii char or instruction to send
# mode: 0 = Instruction, 1 = Data
def  lcd_putc(data, mode):
	if (mode==1):
		lcd_rs(0)
	else:
		lcd_rs(1)
	
	a=(data>>4)&0x000F
	lcd_put_nibble(a)
	lcd_e_strobe()
	a=data&0x000F
	lcd_put_nibble(a)
	lcd_e_strobe()

# Lcd initialization
def  lcd_init():
#SETTA IO DELL'MCP
	lcd_rs(0)
	lcd_e(0)
	time.sleep(15)
	lcd_put_nibble(0x03)
	lcd_e_strobe()
	time.sleep(4)
	lcd_e_strobe()
	time.sleep(2)
	lcd_e_strobe()
	time.sleep(2)
	lcd_put_nibble(0x02)
	lcd_e_strobe()
	time.sleep(2)
	lcd_putc(0x28,0)
	time.sleep(1)
	lcd_putc(0x06,0)
	time.sleep(1)
	lcd_putc(0x0C,0)
	time.sleep(1)
	lcd_putc(0x01,0)
	time.sleep(1)


# Locate cursor on LCD
# row (0-2)
# col (1-39)
def  lcd_locate(row, col):
	lcd_putc((0x80+row*0x40+col),0)
	time.sleep(35)

# Clear LCD
def  lcd_clear(fd):
  lcd_putc(0x01,0)
  time.sleep(2)

# Lcd version of printf
def lcd_printf(format):#, ...):
 #va_list argptr
#char buffer[1024]
	print format
	va_start(argptr,format)
	print va_start
	vsprintf(buffer,format,argptr)
	va_end(argptr)
	for i in range (0, strlen(buffer)):
		lcd_putc(buffer[i],1)
		print("eccomi")
	
#*****************
#		MAIN
#*****************

if (i2c_open()<0):
	print("Apertura del bus I2C fallita\n")
	#return 1
while 1:
	print("GESTIONE MCP23016\n")
	print("Operazioni possibili:\n")
	print("1:TEST\n")
	print("2:Esci\n\n")
	#print("Scelta = ")
	scelta = raw_input("Scelta =")
	if (scelta=="1"):
		lcd_locate(0,0)
		lcd_printf("Ciao");
		printf("Frase  di prova scritta\n");	
	else:
		pass		
	if (scelta=="2"):
		i2c_close()
		sys.exit(0)
		 #return 1


#risp = raw_input("Come ti chiami? ")
#print "Ciao, %s, piacere di conoscerti" % risp 







