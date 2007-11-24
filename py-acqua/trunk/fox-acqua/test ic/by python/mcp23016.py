#*********************
#  MCP23016 ROUTINES
#*********************

from i2c_py import *

#from routine_lcd import *
id = 0x40
# RIFLETTE IL LIVELLO LOGICO DEL PIN
# 1 = livello logico alto
# 0 = livelLo logico basso
mcp23016GPIO0	= 0X00
mcp23016GPIO1	= 0X01
mcp23016GP7	= 7
mcp23016GP6	= 6
mcp23016GP5	= 5
mcp23016GP4	= 4
mcp23016GP3	= 3
mcp23016GP2	= 2
mcp23016GP1	= 1
mcp23016GP0	= 0

# ACCEDE AL VALORE DEI LATCH DI USCITA
# 1 = livello logico alto
# 0 = livelLo logico basso
mcp23016OLAT0	= 0X02  #LATCH
mcp23016OLAT1	= 0X03  #LATCH
mcp23016OL7	= 7
mcp23016OL6	= 6
mcp23016OL5	= 5
mcp23016OL4	= 4
mcp23016OL3	= 3
mcp23016OL2	= 2
mcp23016OL1	= 1
mcp23016OL0	= 0

# INVERTE LETTURA
# 1 = riflette il livello logico opposto a quello presente sul pin quando si legge GPIO
# 0 = lettura = stato del pin
mcp23016IPOL0	= 0X04 	
mcp23016IPOL1	= 0X05 	
mcp23016IP7	= 7
mcp23016IP6	= 6
mcp23016IP5	= 5
mcp23016IP4	= 4
mcp23016IP3	= 3
mcp23016IP2	= 2
mcp23016IP1	= 1
mcp23016IP0	= 0

#x impostare direzione
# 1 = input
# 0 = output
mcp23016IODIR0	= 0X06
mcp23016IODIR1 =	0X07
mcp23016IODIRIO7	= 7
mcp23016IODIRIO6	= 6
mcp23016IODIRIO5	= 5
mcp23016IODIRIO4	= 4
mcp23016IODIRIO3	= 3
mcp23016IODIRIO2	= 2
mcp23016IODIRIO1	= 1
mcp23016IODIRIO0	= 0

# RIFLETTE I LIVELLI LOGICI DEI PIN IMPOSTATI COME INTERRUPT AL MOMENTO DEL CAMBIAMENTO DI STATO
# 1 = attivo alto
# 0 = attivo basso
mcp23016INTCAP0 = 0X08
mcp23016INTCAP1	= 0X09
mcp23016ICP7	= 7
mcp23016ICP6	= 6
mcp23016ICP5	= 5
mcp23016ICP4	= 4
mcp23016ICP3	= 3
mcp23016ICP2	= 2
mcp23016ICP1	= 1
mcp23016ICP0	= 0

#CONFIGURAZIONE DEI REGISTRI DELL' I/O EXPANDER
mcp23016IOCON0	= 0X0A
mcp23016IOCON1	= 0X0B
mcp23016INTPOL	= 1	# INTERRUPT ACTIITY RESOLUTION

###################
### per lcd
###################
P_UP		= 1
P_DOWN	=	2
P_LEFT	=	3
P_RIGHT	=	4
P_OK	=	5

lcd_port	= 0X00 #GP0
lcd_E		= 3
lcd_RS	=	2
lcd_D4	=	4
lcd_D5	=	5
lcd_D6	=	6
lcd_D7	=	7

def mcp23016_pinReadLevel(id, gp, pin):
	value=mcp230xx_regLeggi(id,gp)
	value=value & (1 << pin )
	if (value==(1 << pin )):
		return 1
	else:
		 return 0

def mcp23016_pinWriteLevel(id, gp,pin,level):
	value=mcp23016_regLeggi(id, gp)
	print "value_write_level %s\n" %value
	if (level==1):
		 value=value | (1 << pin )
	else:
		value=value & ( 0xff -(1 << pin ))
		mcp23016_regScrivi(id, gp,value)

def mcp23016_regLeggi(id , reg):
	print "id %s\n" %id
	print "reg %s\n" %reg
	i2c_start()
	i2c_outbyte(id)
	i2c_outbyte(reg)
	i2c_start()
	i2c_outbyte(id+1)
	data=i2c_inbyte(0)
	i2c_stop()
	print "data_reg_Leggi %s\n" %data
	return data

def mcp23016_regScrivi(id, registro, value):
	i2c_start()
	i2c_outbyte(id)
	i2c_outbyte(registro)
	i2c_outbyte(value)
	i2c_stop()
