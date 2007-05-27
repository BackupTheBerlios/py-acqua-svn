// I2C user space bit banging example
// See: http://www.acmesystems.it/?id=10

#include "stdio.h"     
#include "unistd.h"    
#include "sys/ioctl.h"
#include "fcntl.h"     
#include "time.h"     
#include "asm/etraxgpio.h"

#define I2C_DATA_LINE   1<<24
#define I2C_CLOCK_LINE  1<<25

int i2c_fd;

// Get the SDA line state

int i2c_getbit(void) {
  unsigned int value;
  value=ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_READBITS));
  if ((value&(I2C_DATA_LINE))==0) return 0;
  else return 1;
} 

// Set the SDA line as output

void i2c_dir_out(void) {
  int iomask;
  iomask = I2C_DATA_LINE;
  ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_OUTPUT), &iomask);
}

// Set the SDA line as input

void i2c_dir_in(void) {
  int iomask;
  iomask = I2C_DATA_LINE;
  ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_INPUT), &iomask);
}

// Set the SDA line state

void i2c_data(int state) {
  if (state==1) {
    i2c_dir_in(); 
  } else {  
    i2c_dir_out();  
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_DATA_LINE);
  } 
}

// Set the SCL line state

void i2c_clk(int state) {
  if (state==1) ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_CLOCK_LINE);
  else ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_CLOCK_LINE);
}

// Read a byte from I2C bus and send the ack sequence
// Put islast = 1 is this is the last byte to receive from the slave

unsigned char i2c_inbyte(int islast) {
  unsigned char value = 0;
  int bitvalue;
  int i;

  // Read data byte

  i2c_clk(0);
  i2c_dir_in();

  for (i=0;i<8;i++) {
    i2c_clk(1);

    bitvalue = i2c_getbit();
    value |= bitvalue;
    if (i<7) value <<= 1;
    
    i2c_clk(0);
  }
  
  if (islast==0) {
    // Send Ack if is not the last byte to read
  
    i2c_dir_out();
    i2c_data(0);
    i2c_clk(1);
    i2c_clk(0);
    i2c_dir_in();
  } else {
    // Doesn't send Ack if is the last byte to read
    i2c_dir_in();
    i2c_clk(1);
    i2c_clk(0);
  }
  return value;
}


// Open the GPIOB dev 

int i2c_open(void) {
  int iomask;

  i2c_fd = open("/dev/gpiog", O_RDWR);
  iomask = I2C_CLOCK_LINE;
  ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_OUTPUT), &iomask);
  iomask = I2C_DATA_LINE;
  ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_INPUT), &iomask);
  ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_DATA_LINE);
  i2c_dir_in();
  i2c_clk(1);
  return i2c_fd;
}

// Close the GPIOB dev 

void i2c_close(void) {
  i2c_dir_in();
  close(i2c_fd);
}

// Send a start sequence to I2C bus

void i2c_start(void){
  i2c_clk(0);
  i2c_data(1);
  i2c_clk(1);
  i2c_data(0);
}

// Send a stop sequence to I2C bus

void i2c_stop(void) {
  i2c_clk(0);
  i2c_data(0);
  i2c_clk(1);
  i2c_data(1);
}

// Send a byte to the I2C bus and return the ack sequence from slave
// rtc
//  0 = Nack, 1=Ack

int i2c_outbyte(unsigned char x) {
  int i;
  int ack;

  i2c_clk(0);

  for (i=0;i<8;i++) {
    if (x & 0x80) i2c_data(1);
    else  i2c_data(0);
    i2c_clk(1);
    i2c_clk(0);
    x <<= 1;
  }

  i2c_dir_in();
  i2c_clk(1);
  ack=i2c_getbit();
  i2c_clk(0);
  
  if (ack==0) return 1;
  else return 0;
}

int main(void) {
  int value;
  int ch;

  // PCF8591 address scheme
  // |  1 |  0 |  0 |  1 | A2 | A1 | A0 | R/W |
  // | i2c_fixed         | i2c_addr     | 1/0 |

  int i2c_fixed=0x09;
  int i2c_addr=0x01;

  printf("Reading from 4 ch 8 bit A/D converter PCF8591\n");

  if (i2c_open()<0) {
    printf("i2c open error\n");
    return 1;
  }

  ch=0;
  while (1) {

    // Select the channel number  
    i2c_start();
    if (i2c_outbyte((i2c_fixed<<4)|(i2c_addr<<1)|0)==0) {
      printf("NACK received %d\n",__LINE__);
      i2c_stop();
      continue;
    }
      
    if (i2c_outbyte(ch)==0) {
      printf("NACK received %d\n",__LINE__);
      i2c_stop();
      continue;
    }
    i2c_stop();

    // Read the A/D value

    i2c_start();
    if (i2c_outbyte((i2c_fixed<<4)|(i2c_addr<<1)|1)==0) {
      printf("NACK received %d\n",__LINE__);
      i2c_stop();
      continue;
    }
  
    i2c_inbyte(0);        // Last conversion result
    value=i2c_inbyte(1);  // Current conversion result
    i2c_stop();
    
    // Show the voltage level
    printf("CH%d = %.2fv (%02X hex)\n",ch,value*0.012941,value);
    ch++;
    if (ch==4) break;
  } 
  
  i2c_close();
  return 0;
} 
