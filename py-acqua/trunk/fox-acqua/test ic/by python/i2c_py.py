#I2C user space bit banging example
#See: http://www.acmesystems.it/?id=10
import sys
import struct
import fcntl
import os
import time
import select

#----
# Generated by h2py 0.1.1 from <linux/ppdev.h>,
# then cleaned up a bit by Michael P. Ashton and then a gain by chris ;-)
# Changes for Python2.2 support (c) September 2004 Alex.Perry@qm.com


def sizeof(type): return struct.calcsize(type)
def _IOC(dir, type, nr, size):  return int((dir << _IOC_DIRSHIFT ) | (type << _IOC_TYPESHIFT ) |\
                                       (nr << _IOC_NRSHIFT ) | (size << _IOC_SIZESHIFT))
def _IO(type, nr):      return _IOC(_IOC_NONE,  type, nr, 0)
def _IOR(type,nr,size): return _IOC(_IOC_READ,  type, nr, sizeof(size))
def _IOW(type,nr,size): return _IOC(_IOC_WRITE, type, nr, sizeof(size))

_IOC_SIZEBITS   = 14
_IOC_SIZEMASK   = (1L << _IOC_SIZEBITS ) - 1
_IOC_NRSHIFT    = 0
_IOC_NRBITS     = 8
_IOC_TYPESHIFT  = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_TYPEBITS   = 8
_IOC_SIZESHIFT  = _IOC_TYPESHIFT + _IOC_TYPEBITS
IOCSIZE_MASK    = _IOC_SIZEMASK << _IOC_SIZESHIFT
IOCSIZE_SHIFT   = _IOC_SIZESHIFT

# Python 2.2 uses a signed int for the ioctl() call, so ...
if ( sys.version_info[0] < 3 ) or ( sys.version_info[1] < 3 ):
 _IOC_WRITE      =  1L
 _IOC_READ       = -2L
 _IOC_INOUT      = -1L
else:
 _IOC_WRITE      =  1L
 _IOC_READ       =  2L
 _IOC_INOUT      =  3L

_IOC_DIRSHIFT   = _IOC_SIZESHIFT + _IOC_SIZEBITS
IOC_INOUT       = _IOC_INOUT << _IOC_DIRSHIFT
IOC_IN          = _IOC_WRITE << _IOC_DIRSHIFT
IOC_OUT         = _IOC_READ << _IOC_DIRSHIFT

_IOC_NONE       = 0

_IOC_DIRBITS    = 2
_IOC_DIRMASK    = (1 << _IOC_DIRBITS) - 1
_IOC_NRMASK     = (1 << _IOC_NRBITS) - 1
_IOC_TYPEMASK   = (1 << _IOC_TYPEBITS ) - 1

def _IOC_DIR(nr):       return (nr >> _IOC_DIRSHIFT)  & _IOC_DIRMASK
def _IOC_NR(nr):        return (nr >> _IOC_NRSHIFT)   & _IOC_NRMASK
def _IOC_SIZE(nr):      return (nr >> _IOC_SIZESHIFT) & _IOC_SIZEMASK
def _IOC_TYPE(nr):      return (nr >> _IOC_TYPESHIFT) & _IOC_TYPEMASK
def _IOWR(type, nr, size): return _IOC(_IOC_READ | _IOC_WRITE, type, nr , sizeof(size))


MODEM_POWER_LINE        = 1<<28
ETRAXGPIO_IOCTYPE       = 43
IO_READBITS             = 0x1
IO_SETBITS              = 0x2
IO_CLRBITS              = 0x3

IO_HIGHALARM            = 0x4
IO_LOWALARM             = 0x5
IO_CLRALARM             = 0x6

IO_SETGET_INPUT		= 0x12
IO_SETGET_OUTPUT	= 0x13

leggi = 1<<2
leggi_2 = 1<<4


I2C_DATA_LINE  = 1<<24
I2C_CLOCK_LINE = 1<<17

#Get the SDA line state

def i2c_getbit():
	value=ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_READBITS));
	if ((value&(I2C_DATA_LINE))==0):
		return 0
	else:
		return 1


# Set the SDA line as output

def i2c_dir_out():
	iomask = I2C_DATA_LINE
	fcntl.ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_OUTPUT), iomask);


# Set the SDA line as input

def i2c_dir_in():
	iomask = I2C_DATA_LINE
	fcntl.ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_INPUT), iomask);

# Set the SDA line state

def i2c_data():
	if (state==1):
		i2c_dir_in()
	else:
		i2c_dir_out()
		fcntl.ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_DATA_LINE);



# Set the SCL line state

def i2c_clk():
	if (state==1):
		fcntl.ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_CLOCK_LINE);
	else:
		fcntl.ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_CLOCK_LINE);


#Read a byte from I2C bus and send the ack sequence
#Put islast = 1 is this is the last byte to receive from the slave

def i2c_inbyte():
#Read data byte
	i2c_clk(0)
	i2c_dir_in()
	for i in range (0, 8):
		i2c_clk(1)
		bitvalue = i2c_getbit()
		value |= bitvalue;
		if (i<7):
			value <<= 1
			i2c_clk(0)
	if (islast==0):
#Send Ack if is not the last byte to read
		i2c_dir_out()
		i2c_data(0)
		i2c_clk(1)
		i2c_clk(0)
		i2c_dir_in()
	else:
#Doesn't send Ack if is the last byte to read
		i2c_dir_in()
		i2c_clk(1)
		i2c_clk(0)
	return value;



# Open the GPIOB dev 

def i2c_open():
	device = "/dev/gpiog"
	i2c_fd = os.open(device, os.O_RDWR)
	print i2c_fd
	iomask = I2C_CLOCK_LINE
	print iomask
	fcntl.ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_OUTPUT), iomask)
	iomask = I2C_DATA_LINE
	print iomask
	fcntl.ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_INPUT), iomask)
	fcntl.ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_DATA_LINE)
	i2c_dir_in()
	i2c_clk(1)
	return i2c_fd


# Close the GPIOB dev 

def i2c_close():
	i2c_dir_in()
	os.close(i2c_fd)


# Send a start sequence to I2C bus

def i2c_start():
	i2c_clk(0)
	i2c_data(1)
	i2c_clk(1)
	i2c_data(0)

# Send a stop sequence to I2C bus

def i2c_stop():
	i2c_clk(0)
	i2c_data(0)
	i2c_clk(1)
	i2c_data(1)

# Send a byte to the I2C bus and return the ack sequence from slave
# rtc
#  0 = Nack, 1=Ack

def i2c_outbyte():
	i2c_clk(0)
	for i in range(0, 8):
		if (x & 0x80):
			 i2c_data(1)
		else:
			i2c_data(0)
		i2c_clk(1)
		i2c_clk(0)
		x <<= 1
	i2c_dir_in()
	i2c_clk(1)
	ack=i2c_getbit()
	i2c_clk(0)
	if (ack==0):
		 return 1
	else:
		return 0
