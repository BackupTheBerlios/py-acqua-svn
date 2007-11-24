####routine lcd
####
from  mcp23016 import *


def lcdMcpInit():
	mcp23016_regScrivi(id, mcp23016IODIR0,0)#DISPLAY, TT OUT
	mcp23016_regScrivi(id, mcp23016IODIR1,0xff)#pulsanti, tt in
	mcp23016_regScrivi(id, mcp23016GP0,0)#us

#RS line
def lcd_rs(level) :
	mcp23016_pinWriteLevel(id, lcd_port,lcd_RS,level)
#E line
def lcd_e(level):
	mcp23016_pinWriteLevel(id, lcd_port,lcd_E,level)
#D4..7
def lcdD4(level):
	mcp23016_pinWriteLevel(id, lcd_port,lcd_D4,level)
def lcdD5(level):
	mcp23016_pinWriteLevel(id, lcd_port,lcd_D5,level)
def lcdD6(level):
	mcp23016_pinWriteLevel(id, lcd_port,lcd_D6,level)
def lcdD7(level):
	mcp23016_pinWriteLevel(id, lcd_port,lcd_D7,level)

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
	if not mode:
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
	lcdMcpInit()
	lcd_rs(0)
	lcd_e(0)
	time.sleep(0.015)
	lcd_put_nibble(0x03)
	lcd_e_strobe()
	time.sleep(0.004)
	lcd_e_strobe()
	time.sleep(0.002)
	lcd_e_strobe()
	time.sleep(0.002)
	lcd_put_nibble(0x02)
	lcd_e_strobe()
	time.sleep(0.001)
	lcd_putc(0x28,0)
	time.sleep(0.001)
	lcd_putc(0x06,0)
	time.sleep(0.001)
	lcd_putc(0x0C,0)
	time.sleep(0.001)
	lcd_putc(0x01,0)
	time.sleep(0.002)


# Locate cursor on LCD
# row (0-2)
# col (1-39)
def  lcd_locate(row, col):
	lcd_putc(0x80+row*0x40+col,0)
	#lcd_putc((0x80+row*0x40+col),0)
	time.sleep(0.00035)

# Clear LCD
def  lcd_clear():
  lcd_putc(0x01,0)
  time.sleep(0.002)

# Lcd version of printf
def lcd_printf(stringa): 
	for i in stringa: 
		lcd_putc(ord(i), 1)
		print i
