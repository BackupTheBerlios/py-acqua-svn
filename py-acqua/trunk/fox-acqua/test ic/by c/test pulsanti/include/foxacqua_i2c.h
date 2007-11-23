//#Copyright (C) 2005, 2007 Py-acqua
//#http://www.pyacqua.net
//#
//#email: info@pyacqua.net
//#
//#
//#Py-Acqua is free software; you can redistribute it and/or modify
//#    it under the terms of the GNU General Public License as published by
//#    the Free Software Foundation; either version 2 of the License, or
//#    (at your option) any later version.
//#
//#Py-Acqua is distributed in the hope that it will be useful,
//#    but WITHOUT ANY WARRANTY; without even the implied warranty of
//#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//#    GNU General Public License for more details.
//#
//#    You should have received a copy of the GNU General Public License
//#    along with Py-Acqua; if not, write to the Free Software
//#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
//#
//#    Gestione i2c tramite syscall in userspace


//sda PA1 //SDA XKÈ C'È GIA LA RESISTENZA DI SW1 A VCC
//scl PA0



#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"




#define SDA PG17 
#define SCL PG24 

#define I2C_CLOCK_HIGH 1
#define I2C_CLOCK_LOW 0
#define I2C_DATA_HIGH 1
#define I2C_DATA_LOW 0


	#include "sys/ioctl.h"
	#include "fcntl.h"


#ifdef FOXACQUA_I2C_SYSCALL_H
	#include "linux/gpio_syscalls.h"
#endif

#ifdef FOXACQUA_I2C_IOCTL_H
	#include "asm/etraxgpio.h"

	#define CLOCK_LOW_TIME            8
	#define CLOCK_HIGH_TIME           8
	#define START_CONDITION_HOLD_TIME 8
	#define STOP_CONDITION_HOLD_TIME  8
	#define ENABLE_OUTPUT 0x01
	#define ENABLE_INPUT 0x00

	#define I2C_DATA_LINE       1<<24
	#define I2C_CLOCK_LINE      1<<17

	#ifndef IO_SETGET_INPUT
	#define IO_SETGET_INPUT   0x12
	#endif
	#ifndef IO_SETGET_OUTPUT
	#define IO_SETGET_OUTPUT  0x13
	#endif
#endif

#define i2c_delay(usecs) usleep(usecs)




inline unsigned char 	i2c_getbit(void);		// Get the SDA line state
inline void 		i2c_data(unsigned char state); 	// Set the SDA line state
inline void 		i2c_clk(unsigned char state); 	// Set the SCL line state
inline void 		i2c_dir_out(void); 		// Set the SDA line as output
inline void 		i2c_dir_in(void); 		// Set the SDA line as input

inline void 		i2c_start(void);		// Send a start sequence to I2C bus
inline void 		i2c_stop(void); 		// Send a stop sequence to I2C bus

inline unsigned char 	i2c_inbyte(unsigned char ack); 	// Read a byte from I2C bus and send the ack sequence
inline unsigned char 	i2c_outbyte(unsigned char x);	// Send a byte to the I2C bus and return the ack sequence from slave

