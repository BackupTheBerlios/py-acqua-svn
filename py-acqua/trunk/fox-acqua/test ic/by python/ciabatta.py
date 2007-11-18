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


#*********************************************************************
# 
#   TEST DELL'INTEGRATO MCP23008 
#
#*********************************************************************


#RESISTENZE DI PULLUP SU I2C DI 1K !

#di fabbrica tt i pin sono configurati in ingresso

#PIN A0,A1,A2 A MASSA
#RESET A VCC

#****************************************************

from i2c_py import *

#include "stdio.h"
#include "stdlib.h"

#include "unistd.h" 
#include "time.h"
#include "sys/ioctl.h"
#include "fcntl.h"     
#include "asm/etraxgpio.h"


myMcp23008_id	= 0x27

#REGISTRI
#x impostare direzione
# 1 = input
# 0 = output
IODIR	= 0X00	
IO7	= 7
IO6	= 6
IO5	= 5
IO4	= 4
IO3	= 3
IO2	= 2
IO1	= 1
IO0	= 0
# INVERTE LETTURA
# 1 = riflette il livello logico opposto a quello presente sul pin quando si legge GPIO
# 0 = lettura = stato del pin
IPOL	= 0X01 	
IP7	= 7
IP6	= 6
IP5	= 5
IP4	= 4
IP3	= 3
IP2	= 2
IP1	= 1
IP0	= 0
# INTERRUPT AD OGNI CAMBIAMENTO
#1 = abilitato
#	N.B.: bisogna configurare anche DEFVAL ed INTCON
# 0 = disabilitato
GPINTEN	= 0X02
GPINT7	= 7
GPINT6	= 6
GPINT5	= 5
GPINT4	= 4
GPINT3	= 3
GPINT2	= 2
GPINT1	= 1
GPINT0	= 0
# LIVELLO LOGICO A CUI SI GENERE L'INTERRUPT
#   l'interrupt si genera quando sul pin c'è un livello 
#  opposto a quello impostato nel bit associato di questo registro.
DEFVAL	= 0X03
DEF7	= 7
DEF6	= 6
DEF5	= 5
DEF4	= 4
DEF3	= 3
DEF2	= 2
DEF1	= 1
DEF0	= 0
#REGISTRO DI CONTROLLO DELL'INTERRUPT
# 1 = IL PIN È COMPARATO CON IL CORRISPONDENTE BIT IN DEFVAL
# 0 = IL PIN È COMPARATO CON LO STATO PRECEDENTE DELLO STESSO. (DEFVAL VIENE IGNORATO) 
INTCON	= 0X04
IOC7	= 7
IOC6	= 6
IOC5	= 5
IOC4	= 4
IOC3	= 3
IOC2	= 2
IOC1	= 1
IOC0	= 0
#CONFIGURAZIONE DEI REGISTRI DELL' I/O EXPANDER
IOCON	= 0X05
#7,6,3,0 NON PRESENTI
#LETTURA SEQUENZIALE
#1 = lettura sequenziale disabilitata, puntatore indirizzi non incrementato
#0 = lettura sequenziale abilitata, puntatore indirizzi incrementato
SREAD	= 5
#GESTISCE SLEW RATE DI SDA
# 1 = disabilitato
# 0 = abilitato
DISSLW	= 4
#CONFIGURA IL TIPO DI OUTPUT DEGLI 'INT' PIN
# 1 = open drain
# 0 = uscita del driver attiva
ODR	= 2
# SETTA LA POLARITÀ DELL'OUTPUT PIN 'INT'
# 1 = attivo a livello alto
# 0 = attivo a livello basso
INTPOL	= 1
# Imposta le resistenze di pull-up sugli ingressi
# 1 = se il pin è configurato come input, viene applicata la resistenza di pullup
# 0 = nessun pullup
GPPU	= 0X06
PU7	= 7
PU6	= 6
PU5	= 5
PU4	= 4
PU3	= 3
PU2	= 2
PU1	= 1
PU0	= 0
# Registro x abilitare gli interrupt
# 1 = interrupot abilitato
# 0 = interrupt disabilitato
INTF	= 0X07
INT7	= 7
INT6	= 6
INT5	= 5
INT4	= 4
INT3	= 3
INT2	= 2
INT1	= 1
INT0	= 0
# RIFLETTE I LIVELLI LOGICI DEI PIN IMPOSTATI COME INTERRUPT AL MOMENTO DEL CAMBIAMENTO DI STATO
# 1 = attivo alto
# 0 = attivo basso
INTCAP	= 0X08
ICP7	= 7
ICP6	= 6
ICP5	= 5
ICP4	= 4
ICP3	= 3
ICP2	= 2
ICP1	= 1
ICP0	= 0
# RIFLETTE IL LIVELLO LOGICO DEL PIN
# 1 = livello logico alto
# 0 = livelLo logico basso
GPIO	= 0X09
GP7	= 7
GP6	= 6
GP5	= 5
GP4	= 4
GP3	= 3
GP2	= 2
GP1	= 1
GP0 =	0
# ACCEDE AL VALORE DEI LATCH DI USCITA
# 1 = livello logico alto
# 0 = livelLo logico basso
OLAT	= 0X0A  #LATCH
OL7	= 7
OL6	= 6
OL5	= 5
OL4	= 4
OL3	= 3
OL2	= 2
OL1	= 1
OL0	= 0

CLOCK_LOW_TIME     =       8
CLOCK_HIGH_TIME      =     8
START_CONDITION_HOLD_TIME = 8
STOP_CONDITION_HOLD_TIME = 8
ENABLE_OUTPUT = 0x01
ENABLE_INPUT = 0x00
I2C_CLOCK_HIGH = 1
I2C_CLOCK_LOW = 0
I2C_DATA_HIGH = 1
I2C_DATA_LOW = 0


#I2C_DATA_LINE   =    1<<24
#I2C_CLOCK_LINE   =   1<<17

#ifndef IO_SETGET_INPUT
#define IO_SETGET_INPUT   0x12
#endif
#ifndef IO_SETGET_OUTPUT
#define IO_SETGET_OUTPUT  0x13
#endif

#define i2c_delay(usecs) usleep(usecs)

#*********************
#  MCP23008 ROUTINES
#*********************
def mcp23008_leggi(reg):
	i2c_start()
	i2c_outbyte(myMcp23008_id<<1)# accoda uno zero x dire scrivi
	i2c_outbyte(reg)
	i2c_start()
	i2c_outbyte((myMcp23008_id<<1)+1)#accoda un uno  x dire leggi 
	data=i2c_inbyte(0)
	i2c_stop()
	return data


def mcp23008_scrivi(registro, value):

	i2c_start()
	i2c_outbyte(myMcp23008_id<<1)
	i2c_outbyte(registro)
	i2c_outbyte(value)
	i2c_stop()

def mcp23008_ttOut():
	mcp23008_scrivi(IODIR,0)

def mcp23008_ttIn():
	mcp23008_scrivi(IODIR,0XFF)
	mcp23008_scrivi(GPPU,0xFF)#//pull-up su tutti
	


def mcp23008_scriviGpio(value):
	mcp23008_scrivi(IODIR,value)


def mcp23008_leggiGpio():

	gpio_level=mcp23008_leggi(GPIO)
	return gpio_level

if (i2c_open()<0):
	printf("Apertura del bus I2C fallita\n");
	#return 1
#pin_uscita()
print "pin uscita\n"
mcp23008_ttOut()
print "tutti i pin come out\n"
while 1:

	print("GESTIONE MCP23008\n")
	print("Operazioni possibili:\n")
	print("1:Scrittura del valore logico dei pin\n")
	print("5:Esci\n\n")
	scelta = raw_input("Scelta =\n")
	if (scelta=="1"):#{//scrittura
		print("1:Modifica tutta la porta GPIO\n")
		print("2:Un singolo pin x volta\n")
		scelta = raw_input("Scelta =\n")
		if (scelta=="1"):
			print("Inserisci il valore(0=off 255=on) a cui si dovranno portare tutti i pin\n")
			value = raw_input("Valore=")
			#controllare che sia impostato tt in uscita.
			mcp23008_scrivi(GPIO,value)
			print "tutti i pin"
			print GPIO
			print value
		if (scelta=="2"):
			print("Inserisci il numero del pin (0..7) e il valore (0..FF) a cui si dovrà portare\n")
			pin = raw_input("Pin =\n")
			level = raw_input("level=\n")
			#ping = raw_input("inserisci il ping=\n")
			# controllare che il pin sia impostato in uscita.
			value=mcp23008_leggiGpio()
			print "value 1 %s\n" %value
			value = int(level)<<int(pin)
			print "stampo value %s\n" %value
			#print "stampo ping %s\n" %ping
			mcp23008_scrivi(GPIO,pin)
			print "un pin"
			print GPIO
			print value

	else:
		pass
	if (scelta=="5"):
		i2c_close()
		sys.exit(0)
