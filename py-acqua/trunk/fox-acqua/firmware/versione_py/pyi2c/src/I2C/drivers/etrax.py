#! /usr/bin/env python
#
# python I2C FoxBoard SDA/SCL mapping
#


import sys
import time
import struct
import fcntl
import os

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


I2C_DATA_LINE =     1<<24
I2C_CLOCK_LINE =   1<<17

InterfaceName='FOX'


#---------------------------------------------------------------------------------
class Driver:

    def __init__(self, name):
        self.setSpeed(1200)   # speed depends on hardware
        self.port = serial.Serial(int(name[len(InterfaceName):])-1)
# iniziamo con l i2c di fox

##Get the SDA line state
	def i2c_getbit():
		value=ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_READBITS));
		if ((value&(I2C_DATA_LINE))==0) 
			return 0;
		else 
			return 1;

##Set the SDA line state
	def i2c_data():
		if (state==1)
			ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_DATA_LINE);
		else
			ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_DATA_LINE);

##Set the SCL line state
	def i2c_clk():
		if (state==1)
			ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_CLOCK_LINE);
		else 
			ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_CLOCK_LINE);

##Set the SDA line as output
	def i2c_dir_out():
		iomask = I2C_DATA_LINE;
		ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_OUTPUT), &iomask);

##Set the SDA line as input
	def i2c_dir_in():
		iomask = I2C_DATA_LINE
		ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_INPUT), &iomask);

##Open the GPIOG dev 
	def i2c_open():
		i2c_fd = open("/dev/gpiog", O_RDWR);
		i2c_data(I2C_DATA_HIGH);
		i2c_dir_out();
		i2c_clk(I2C_CLOCK_HIGH);
		i2c_data(I2C_DATA_HIGH);
		i2c_delay(100);
		return i2c_fd;

##Read a byte from I2C bus and send the ack sequence
	def i2c_inbyte():
		value = 0;
##Read data byte
			i2c_dir_in();
			for (i=0;i<8;i++)
			i2c_clk(1)
			bitvalue = i2c_getbit()
			value |= bitvalue
			if (i<7) value <<= 1
				i2c_clk(0)
##Send Ack
		if(ack):
			i2c_dir_out()
			i2c_data(0)
			i2c_clk(1)
			i2c_clk(0)
		return value;

##Send a start sequence to I2C bus
	def i2c_start():
		i2c_dir_out()
		i2c_clk(1)
		i2c_data(1)
		i2c_data(0)
##Send a stop sequence to I2C bus
	def i2c_stop():
		i2c_dir_out()
		i2c_clk(1)
		i2c_data(0)
		i2c_data(1)

##Send a byte to the I2C bus and return the ack sequence from slave
	def i2c_outbyte():
		i2c_clk(0)
		for (i=0;i<8;i++):
			if (x & 0x80):
				i2c_data(1)
			else:
				i2c_data(0)
				i2c_clk(1)
				i2c_clk(0)
				x <<= 1
		i2c_data(0)
		i2c_dir_in()
		i2c_clk(1)
		ack=i2c_getbit()
		i2c_clk(0)
		i2c_dir_out()
		if (ack==0):
			return 1
		else:
			return 0





    def close(self):
        self.os.close(p)

    def setSpeed(self, freq):
        self.delay = 1/(0.0000001+freq)


    def write(self, sda, scl):
        self.port.setRTS(sda)
        self.port.setDTR(scl)
        time.sleep(self.delay)

    def read(self):
        return not self.port.getCTS()


def getDevices():
# Gives back availables interfaces names
	available = []
	device = "/dev/gpiog"
	p = os.open(device, os.O_RDWR)
	return available

