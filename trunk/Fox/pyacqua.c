//#Copyright (C) 2005, 2006 Luca Sanna - Italy
//#http://pyacqua.altervista.org
//#email: pyacqua@gmail.com  
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




#include "stdio.h"     
#include "unistd.h"    
#include "sys/ioctl.h"
#include "fcntl.h"     
#include "time.h"     
#include "asm/etraxgpio.h"

#define CLOCK_LOW_TIME            8
#define CLOCK_HIGH_TIME           8
#define START_CONDITION_HOLD_TIME 8
#define STOP_CONDITION_HOLD_TIME  8
#define ENABLE_OUTPUT 0x01
#define ENABLE_INPUT 0x00
#define I2C_CLOCK_HIGH 1
#define I2C_CLOCK_LOW 0
#define I2C_DATA_HIGH 1
#define I2C_DATA_LOW 0

#define I2C_DATA_LINE			1<<24
#define I2C_CLOCK_LINE		1<<25



#ifndef IO_SETGET_INPUT
#define IO_SETGET_INPUT 	0x12
#endif

#ifndef IO_SETGET_OUTPUT
#define IO_SETGET_OUTPUT 	0x13
#endif

#define i2c_delay(usecs) usleep(usecs)

int i2c_fd;


// Software delay... :( cercare di modificare sto coso!!!

/*void i2c_delay(int us) {
  int a;
  int b;
  int delayvar=1111;

  for (b=0;b<33;b++) {
	  for (a=0;a<us;a++) {
	    delayvar*=3;
	    delayvar/=3;
	  }
	} 
}*/

// Get the SDA line state - OK
int i2c_getbit(void) {
	unsigned int value;
	value=ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_READBITS));
	if ((value&(I2C_DATA_LINE))==0) return 0;
	else return 1;
}	


// Set the SDA line state - OK

void i2c_data(int state) {
	if (state==1) ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_DATA_LINE);
	else ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_DATA_LINE);
}


// Set the SCL line state - OK

void i2c_clk(int state) {
	if (state==1) ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_CLOCK_LINE);
	else ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_CLOCK_LINE);
}


// Set the SDA line as output - OK

void i2c_dir_out(void) {
 	int iomask;
	iomask = I2C_DATA_LINE;
 	ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_OUTPUT), &iomask);
}


// Set the SDA line as input - OK

void i2c_dir_in(void) {
 	int iomask;
	iomask = I2C_DATA_LINE;
 	ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_INPUT), &iomask);
}


// Read a byte from I2C bus and send the ack sequence - From kernel and tanzilli code (da rivedere)
unsigned char i2c_inbyte(void) {
	unsigned char value = 0;
	int bitvalue;
	int i;

	// Read data byte

	i2c_dir_in();

	for (i=0;i<8;i++) {
		i2c_clk(I2C_CLOCK_HIGH);

		bitvalue = i2c_getbit();
		value |= bitvalue;
		if (i<7) value <<= 1;
		
		i2c_clk(I2C_CLOCK_LOW);
	}
	
	// Send Ack
	
	i2c_data(I2C_DATA_LOW);
	i2c_dir_out();
	i2c_data(I2C_DATA_LOW);

	i2c_clk(I2C_CLOCK_HIGH);
	i2c_clk(I2C_CLOCK_LOW);

	i2c_delay(100);	
	return value;
}


// Open the GPIOG dev - From tanzilli code - OK

int i2c_open(void) {
  i2c_fd = open("/dev/gpiog", O_RDWR);
	i2c_data(I2C_DATA_HIGH);
 	i2c_dir_out();
	i2c_clk(I2C_CLOCK_HIGH);
	i2c_data(I2C_DATA_HIGH);
	i2c_delay(100);
  return i2c_fd;
}


// Close the GPIOB dev - From tanzilli code - OK 

void i2c_close(void) {
  close(i2c_fd);
}


// Send a start sequence to I2C bus - From kernel - OK
void i2c_start(void) {
    /*
     * SCL=1 SDA=1
     */
    i2c_dir_out();
    i2c_delay(CLOCK_HIGH_TIME/6);
    i2c_data(I2C_DATA_HIGH);
    i2c_clk(I2C_CLOCK_HIGH);
    i2c_delay(CLOCK_HIGH_TIME);
    /*
     * SCL=1 SDA=0
     */
    i2c_data(I2C_DATA_LOW);
    i2c_delay(START_CONDITION_HOLD_TIME);
    /*
     * SCL=0 SDA=0
     */
    i2c_clk(I2C_CLOCK_LOW);
    i2c_delay(CLOCK_LOW_TIME);
}


// Send a stop sequence to I2C bus - From kernel - OK
void i2c_stop(void) {
    i2c_dir_out();
    /*
     * SCL=0 SDA=0
     */
    i2c_clk(I2C_CLOCK_LOW);
    i2c_data(I2C_DATA_LOW);
    i2c_delay(CLOCK_LOW_TIME*2);
    /*
     * SCL=1 SDA=0
     */
    i2c_clk(I2C_CLOCK_HIGH);
    i2c_delay(CLOCK_HIGH_TIME*2);
    /*
     * SCL=1 SDA=1
     */
    i2c_data(I2C_DATA_HIGH);
    i2c_delay(STOP_CONDITION_HOLD_TIME);

    i2c_dir_in();
}


// Send a byte to the I2C bus and return the ack sequence from slave - From kernel and tanzilli code (da rivedere)
//	0 = Nack, 1=Ack
int i2c_outbyte(unsigned char x){
    int i,ack;

    i2c_dir_out();

    for (i = 0; i < 8; i++) {
        if (x & 0x80) {
            i2c_data(I2C_DATA_HIGH);
        } else {
            i2c_data(I2C_DATA_LOW);
        }

        i2c_delay(CLOCK_LOW_TIME/2);
        i2c_clk(I2C_CLOCK_HIGH);
        i2c_delay(CLOCK_HIGH_TIME);
        i2c_clk(I2C_CLOCK_LOW);
        i2c_delay(CLOCK_LOW_TIME/2);
        x <<= 1;
    }
    i2c_data(I2C_DATA_LOW);
    i2c_delay(CLOCK_LOW_TIME/2);

    /*
     * enable input
     */
    i2c_dir_in();
    i2c_clk(I2C_CLOCK_HIGH);
    ack=i2c_getbit();
    i2c_clk(I2C_CLOCK_LOW);
    i2c_dir_out();

    if (ack==0) return 1;
    else return 0;

}




// Example program for PCF8574


int scrivi (unsigned char byte) {	
	if (i2c_outbyte(byte)==0) {
		printf("NACK received\n");
	}
	else {
		//printf("Indirizzamento in scrittura accettato\n");
	}
}

int main(void) {
	int value;
	int ch;
	int val;
	
	if (i2c_open()<0) {
		printf("i2c open error\n");
    		return 1;
	}
	i2c_start();
	
	printf("Inserisci il numero\n");
	printf("uscita P0 = 1\n");
	printf("uscita P1 = 2\n");
	printf("uscita P2 = 4\n");
	printf("uscita P3 = 8\n");
	printf("uscita P4 = 16\n");
	printf("uscita P5 = 32\n");
	printf("uscita P6 = 64\n");
	printf("uscita P7 = 128\n");
	printf("uscite tutte a 0 = 0\n");
	printf("uscite tutte a 1 = 255\n");
	
	
	scanf("%d", &val);
	
	scrivi(0x40);
	
	scrivi(0);	
	
	scrivi(val);
		
	
	i2c_stop();
				
	i2c_start();
	scrivi(0x41);

		//i2c_inbyte(); 	    // Last conversion result
	value=i2c_inbyte(); // Current conversion result
	i2c_stop();
	
	printf("Ricevuto: %d\n",value);
	printf("\n");
	//out=out*2;
	sleep(1);
	
	
		//while (1) {
	for (ch=0;ch<4;ch++) {
		i2c_start();
		scrivi(0x92);
			
		if (i2c_outbyte(ch)==0) {
			printf("NACK received\n");
		}
		i2c_stop();
					
		i2c_start();
		scrivi(0x93);
		
	
		i2c_inbyte(); 					// Last conversion result
		value=i2c_inbyte(); // Current conversion result
		i2c_stop();
		
		printf("CH%d = %.2fv\n",ch,value*0.012941);
		//}	
		printf("\n");
		sleep(1);
	
	//ds 1307
	int sec;
	int min;
	i2c_start();
	scrivi(0)
	sec=i2c_inbyte();
	//scrivi(0);
	i2c_outbyte(sec);
	//i2c_outbyte(0x7F);
	
	i2c_stop();
	//int va;
	i2c_start();
	scrivi(0);
	sec=i2c_inbyte();
	//va = i2c_inbyte();
	i2c_stop();
	i2c_start();
	scrivi(1);
	min = i2c_inbyte();
	i2c_stop();
	printf("Time : %02X:%02X\r\n", min, sec);
	
		
		
	}
	
	
	
i2c_close();
return 0;
}
