// 02/09/07 - manzoni: ho modificato le routine eliminando i ritardi molto + veloce !!!!!!
//cambiata la routin itoa, molto + performante ora. prima convertiva solo numeri a 2 cifre e 
//lasciava una variabile globale come variabile in cui andava salvato il risultato !!!


#ifndef FOXACQUA_I2C_IOCTL_H
#define FOXACQUA_I2C_IOCTL_H

#include "foxacqua_i2c.h"


int i2c_fd;
inline void i2c_init(){
	if (i2c_open()<0) { 	printf("Apertura del bus I2C fallita\n"); return 1; }
} 

// Open the GPIOG dev 
inline int i2c_open(void) {
  i2c_fd = open("/dev/gpiog", O_RDWR);
	i2c_data(I2C_DATA_HIGH);
 	i2c_dir_out();
	i2c_clk(I2C_CLOCK_HIGH);
	i2c_data(I2C_DATA_HIGH);
	i2c_delay(100);
  return i2c_fd;
}
// Close the GPIOG dev 
inline void i2c_close(void) {
  close(i2c_fd);
}

// Get the SDA line state
inline unsigned char i2c_getbit(void) {
  unsigned int value;
  value=ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_READBITS));
  if ((value&(I2C_DATA_LINE))==0) 
    return 0;
  else 
    return 1;
}
// Set the SDA line state
inline void i2c_data(unsigned char state) {
  if (state==1) 
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_DATA_LINE);
  else 
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_DATA_LINE);
}
// Set the SCL line state
inline void i2c_clk(unsigned char state) {
  if (state==1) 
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_CLOCK_LINE);
  else 
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_CLOCK_LINE);
}
// Set the SDA line as output
inline void i2c_dir_out(void) {
  int iomask;
  iomask = I2C_DATA_LINE;
  ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_OUTPUT), &iomask);
}
// Set the SDA line as input
inline void i2c_dir_in(void) {
  int iomask;
  iomask = I2C_DATA_LINE;
  ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_INPUT), &iomask);
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
    udelay(5);
  }
  // Send Ack
  if(ack){
  i2c_dir_out();
  i2c_data(0);
  i2c_clk(1);
  udelay(5);
  i2c_clk(0);
  }
  udelay(200);	
  return value;
}
// Send a start sequence to I2C bus
inline void i2c_start(void){
  i2c_dir_out();
  i2c_clk(1);
  i2c_data(1);
  udelay(5);
  i2c_data(0);
}
// Send a stop sequence to I2C bus
inline void i2c_stop(void) {
  i2c_dir_out();
  i2c_clk(1);
  i2c_data(0);
  udelay(5);
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
        udelay(5);
        i2c_clk(0);
        udelay(5);
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
