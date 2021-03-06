#! /usr/bin/env python
#
# python I2C FoxBoard SDA/SCL mapping
#


import sys
import time
import struct
import fcntl
import os

InterfaceName='FOX'

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
IO_SETOUTPUT  	=	0xA
IO_SETINPUT   	=	0x9


I2C_DATA_LINE =     1<<24

I2C_CLOCK_LINE =   1<<17


#---------------------------------------------------------------------------------
class Driver:

    def __init__(self, name):
        self.setSpeed(1200)   # speed depends on hardware
        self.port = serial.Serial(int(name[len(InterfaceName):])-1)

    def close(self):
        self.os.close(p)

    def setSpeed(self, freq):
        self.delay = 1/(0.0000001+freq)

	
	def write(self, sda, scl):
		ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_CLOCK_LINE);
		time.sleep(self.delay)
		ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_OUTPUT), I2C_DATA_LINE);
		time.sleep(self.delay)
		ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_DATA_LINE);
		time.sleep(self.delay)
		
		#self.port.setRTS(sda)
		#self.port.setDTR(scl)
		#time.sleep(self.delay)
	def read(self):
		ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETINPUT), I2C_DATA_LINE);
		time.sleep(self.delay)
		ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_READBITS), I2C_DATA_LINE);
		time.sleep(self.delay)
		#return not self.port.getCTS()


def getDevices():
# Gives back availables interfaces names
	available = []
	device = "/dev/gpiog"
	p = os.open(device, os.O_RDWR)
	return available

