#include "stdio.h"     
#include "unistd.h"    
#include "sys/ioctl.h"
#include "fcntl.h"     
#include "time.h"     
#include "asm/etraxgpio.h"

#define I2C_DATA_LINE		1<<24
#define I2C_CLOCK_LINE		1<<25


#ifndef IO_SETGET_INPUT
#define IO_SETGET_INPUT 	0x12
#endif

#ifndef IO_SETGET_OUTPUT
#define IO_SETGET_OUTPUT 	0x13
#endif


int i2c_fd;

// Software delay in us

void udelay(int us) {
  int a;
  int b;
  int delayvar=1111;

  for (b=0;b<33;b++) {
	  for (a=0;a<us;a++) {
	    delayvar*=3;
	    delayvar/=3;
	  }
	}  
}   

// Get the SDA line state

int i2c_getbit(void) {
	unsigned int value;
	value=ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_READBITS));
	if ((value&(I2C_DATA_LINE))==0) return 0;
	else return 1;
}	

// Set the SDA line state

void i2c_data(int state) {
	if (state==1) ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_DATA_LINE);
	else ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_DATA_LINE);
}

// Set the SCL line state

void i2c_clk(int state) {
	if (state==1) ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_CLOCK_LINE);
	else ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_CLOCK_LINE);
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


// Read a byte from I2C bus and send the ack sequence

unsigned char i2c_inbyte(void) {
	unsigned char value = 0;
	int bitvalue;
	int i;

	// Read data byte

	i2c_dir_in();

	for (i=0;i<8;i++) {
		i2c_clk(1);

		bitvalue = i2c_getbit();
		value |= bitvalue;
		if (i<7) value <<= 1;
		
		i2c_clk(0);
	}
	
	// Send Ack
	
	i2c_data(0);
	i2c_dir_out();
	i2c_data(0);

	i2c_clk(1);
	i2c_clk(0);

	udelay(100);	
	return value;
}


// Open the GPIOB dev 

int i2c_open(void) {
  i2c_fd = open("/dev/gpiog", O_RDWR);
	i2c_data(1);
 	i2c_dir_out();
	i2c_clk(1);
	i2c_data(1);
	udelay(100);
  return i2c_fd;
}

// Close the GPIOB dev 

void i2c_close(void) {
  close(i2c_fd);
}

// Send a start sequence to I2C bus

void i2c_start(void){
	i2c_data(0);
	i2c_clk(0);
}

// Send a stop sequence to I2C bus

void i2c_stop(void) {
	i2c_clk(1);
	i2c_data(1);
}

// Send a byte to the I2C bus and return the ack sequence from slave
// rtc
//	0 = Nack, 1=Ack

int i2c_outbyte(unsigned char x) {
	int i;
	int ack;

	i2c_clk(0);

	for (i=0;i<8;i++) {
		if (x & 0x80) i2c_data(1);
		else	i2c_data(0);
		i2c_clk(1);
		i2c_clk(0);
		x <<= 1;
	}
	
 	i2c_dir_in();
	i2c_clk(1);
	ack=i2c_getbit();
	i2c_clk(0);
	i2c_dir_out();
	
	if (ack==0) return 1;
	else return 0;
}

//==========================
// write data one byte from DS1307
//==========================

void write_ds1307(unsigned char address, unsigned char data)
{
    printf("-------------------------------->\r\n");
    printf("Scrittura sul ds1307\r\n");
    short int status;
    i2c_start();
    i2c_outbyte(210);
    i2c_outbyte(address);
    i2c_outbyte(data);
    i2c_stop();
    /*i2c_start();
    status=i2c_outbyte(208);
    while(status==1)
    {
        i2c_start();
        status=i2c_outbyte(208);
        i2c_stop();
    }*/
    printf("<--------------------------------\r\n");
}

//==========================
// read data one byte from DS1307
//==========================

unsigned char read_ds1307(unsigned char address)
{
    printf("-------------------------------->\r\n");
    printf("Lettura dal ds1307\r\n");
    unsigned char data;
    i2c_start();
    i2c_outbyte(210);
    i2c_outbyte(address);
    i2c_stop();
    i2c_start();
    i2c_outbyte(211);
    data=i2c_inbyte();
    printf("Valore letto: %d\r\n",data);
    i2c_stop();
    printf("<--------------------------------\r\n");
    return(data);
}


int main(void)
{
    int sec,min,hour,day,date,month,year=0;

    if (i2c_open()<0) {
        printf("i2c open error\n");
        return 1;
    }

    usleep(50);
    sec=read_ds1307(0);
    write_ds1307(0,sec & 0x7F);	// enable oscillator(bit 7 =0)
    write_ds1307(1,30);
    write_ds1307(2,5);

    while(1)
    {
        sec=read_ds1307(0);   // read second
        min=read_ds1307(1);   // read minute
        hour=read_ds1307(2);  // read hour
        day=read_ds1307(3);   // read day
        date=read_ds1307(4);  // read date
        month=read_ds1307(5); // read month
        year=read_ds1307(6);  // read year
        printf("\n\rTime : %u:%u:%u\r\n",hour,min,sec);
        printf("Day  : %d\r\n",day);
        printf("Date : %d/%d/20%d\r\n",date,month,year); 
        usleep(500);
    }
}
