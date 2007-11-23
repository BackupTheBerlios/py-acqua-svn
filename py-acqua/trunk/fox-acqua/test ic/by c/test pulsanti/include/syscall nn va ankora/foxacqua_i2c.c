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

#ifndef FOXACQUA_I2C_SYSCALL_H
#define FOXACQUA_I2C_SYSCALL_H


#include "foxacqua_i2c.h"



// Get the SDA line state
inline unsigned char i2c_getbit(void) {
	return gpiogetbits(PORTG,SDA);  
}
// Set the SDA line state
inline void i2c_data(unsigned char state) {
  if (state==1) 
   	gpiosetbits(PORTG, SDA);
  else 
	gpioclearbits(PORTG, SDA);
}
// Set the SCL line state
inline void i2c_clk(unsigned char state) {
  if (state==1) 
    	gpiosetbits(PORTG,SCL);
  else 
	gpioclearbits(PORTG, SCL);
}
inline void i2c_dir_out(void) {gpiosetdir(PORTG, DIROUT, SDA);}// Set the SDA line as output
inline void i2c_dir_in(void) {gpiosetdir(PORTG, DIRIN, SDA);}// Set the SDA line as input
inline void i2c_init(void) {
	gpiosetdir(PORTG, DIROUT, SCL);	//SCL out
	gpiosetdir(PORTG, DIROUT, SDA);	//SDA out
	i2c_clk(I2C_CLOCK_HIGH);	//SCL high
	i2c_data(I2C_DATA_HIGH);	//SDA high
	msDelay(100);
}
// Read a byte from I2C bus and send the ack sequence
inline unsigned char i2c_inbyte(unsigned char ack) {
  unsigned char value = 0;
  unsigned char bitvalue;
  register unsigned char i;

  // Read data byte
  i2c_dir_in();
  for (i=0;i<8;i++) {
    i2c_clk(1);
    udelay(5);
    bitvalue = i2c_getbit();
    value |= bitvalue;
    if (i<7) value <<= 1;
    i2c_clk(0);
    udelay(50);//5
  }
  // Send Ack
  if(ack){
  i2c_dir_out();
  i2c_data(0);
  i2c_clk(1);
  udelay(50);//5
  i2c_clk(0);
  }
  udelay(2000);//200	
  return value;
}
// Send a start sequence to I2C bus
inline void i2c_start(void){
  i2c_dir_out();
  i2c_clk(1);
  i2c_data(1);
  udelay(50);//5
  i2c_data(0);
}
// Send a stop sequence to I2C bus
inline void i2c_stop(void) {
  i2c_dir_out();
  i2c_clk(1);
  i2c_data(0);
  udelay(50);//5
  i2c_data(1);
}
// Send a byte to the I2C bus and return the ack sequence from slave
inline unsigned char i2c_outbyte(unsigned char x) {
    register unsigned char i;
    unsigned char ack;
    i2c_clk(0);
    for (i=0;i<8;i++) {
        if (x & 0x80) 
        i2c_data(1);
        else
        i2c_data(0);
        i2c_clk(1);
        udelay(50);//5
        i2c_clk(0);
        udelay(50);//5
        x <<= 1;
    }
    i2c_data(0);
    i2c_dir_in();
    i2c_clk(1);
    ack=i2c_getbit();
    i2c_clk(0);
    i2c_dir_out();
    if (ack==0)
        return 1;
    else 
        return 0;
}
#endif
