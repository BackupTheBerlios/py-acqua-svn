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
/*************************************************


//*********************************************************************
// 
//   TEST DELL'INTEGRATO MCP23008 
//
//*********************************************************************




Collegamenti elettrici:
IOG25 J7.13 as SCL
IOG24 J7.21 as SDA. 

RESISTENZE DI PULLUP SU I2C DI 1K !

di fabbrica tt i pin sono configurati in ingresso

PIN A0,A1,A2 A MASSA
RESET A VCC

****************************************************/

#include "stdio.h"
#include "stdlib.h"

#include "unistd.h" 
#include "time.h"
#include "sys/ioctl.h"
#include "fcntl.h"     
#include "asm/etraxgpio.h"


#define myMcp23008_id	0x27


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


#define I2C_DATA_LINE       1<<24
#define I2C_CLOCK_LINE      1<<17

#ifndef IO_SETGET_INPUT
#define IO_SETGET_INPUT   0x12
#endif
#ifndef IO_SETGET_OUTPUT
#define IO_SETGET_OUTPUT  0x13
#endif

#define i2c_delay(usecs) usleep(usecs)

int i2c_fd;
char stringa[2];
//-----------------------------
//FUNZIONI
//-----------------------------


void itoa(int valore, int base){
  int i, tmp;
 
  for (i=2-1; i>=0; i--)
    {
     tmp=(valore%base);
     if (tmp>9) stringa[i]=(tmp-10)+'a';
     else stringa[i]=tmp+'0';
     valore=valore/base;
    }
}

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

// Software delay in ms
void msDelay(int ms) {
  int i,a;
  int delayvar=10;
  
  for (a=0;a<ms;a++) {
    for (i=0;i<33084;i++) {
      delayvar*=2;        
      delayvar/=2;
    } 
  }
}

// Get the SDA line state
int i2c_getbit(void) {
  unsigned int value;
  value=ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_READBITS));
  if ((value&(I2C_DATA_LINE))==0) 
    return 0;
  else 
    return 1;
}

// Set the SDA line state
void i2c_data(int state) {
  if (state==1) 
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_DATA_LINE);
  else 
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_DATA_LINE);
}

// Set the SCL line state
void i2c_clk(int state) {
  if (state==1) 
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_CLOCK_LINE);
  else 
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_CLOCK_LINE);
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

// Open the GPIOG dev 
int i2c_open(void) {
  i2c_fd = open("/dev/gpiog", O_RDWR);
	i2c_data(I2C_DATA_HIGH);
 	i2c_dir_out();
	i2c_clk(I2C_CLOCK_HIGH);
	i2c_data(I2C_DATA_HIGH);
	i2c_delay(100);
  return i2c_fd;
}

// Close the GPIOG dev 
void i2c_close(void) {
  close(i2c_fd);
}

// Read a byte from I2C bus and send the ack sequence
unsigned char i2c_inbyte(int ack) {
  unsigned char value = 0;
  int bitvalue;
  int i;

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
void i2c_start(void){
  i2c_dir_out();
  i2c_clk(1);
  i2c_data(1);
  udelay(5);
  i2c_data(0);
}

// Send a stop sequence to I2C bus
void i2c_stop(void) {
  i2c_dir_out();
  i2c_clk(1);
  i2c_data(0);
  udelay(5);
  i2c_data(1);
}

// Send a byte to the I2C bus and return the ack sequence from slave
int i2c_outbyte(unsigned char x) {
    int i;
    int ack;
    
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

//*********************
//  MCP23008 ROUTINES
//*********************
int mcp23008_leggi(int reg){
	int data;
	i2c_start();
	i2c_outbyte(myMcp23008_id<<1); // accoda uno zero x dire scrivi
	i2c_outbyte(reg);
	i2c_start();
	i2c_outbyte((myMcp23008_id<<1)+1); // accoda un uno  x dire leggi 
	data=i2c_inbyte(0);
	i2c_stop();
	return data;
}

void mcp23008_scrivi(int registro,int value){

	i2c_start();
	i2c_outbyte(myMcp23008_id<<1);
	i2c_outbyte(registro);
	i2c_outbyte(value);
	i2c_stop();

}
void mcp23008_ttOut(){
	mcp23008_scrivi(IODIR,0);
}
void mcp23008_ttIn(){
	mcp23008_scrivi(IODIR,0XFF);
	mcp23008_scrivi(GPPU,0xFF);//pull-up su tutti
	
}

void mcp23008_scriviGpio(int value){	
	mcp23008_scrivi(IODIR,value);
}

int mcp23008_leggiGpio(){
	int gpio_level;
	gpio_level=mcp23008_leggi(GPIO);
	return gpio_level;
}




int  main (void) {
int scelta,pin,value,level;

    if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }
    for(;;){

	printf("GESTIONE MCP23008\n");
	printf("Operazioni possibili:\n");
	printf("1:Imposta tutti i pin in ingresso con pull-up interno\n");
	printf("2:Imposta tutti i pin in uscita senza interrupt\n");
	printf("3:Lettura dello stato dei pin\n");
	printf("4:Scrittura del valore logico dei pin\n");
	printf("5:Esci\n\n");
	printf("Scelta = ");
	scanf ("%X",&scelta);
	if (scelta==1){
			mcp23008_ttIn();
		printf("Comando eseguito");	
	}
	else if (scelta==2){
		mcp23008_ttOut();
		printf("Comando eseguito");
	}
	else if (scelta==3){//lettura
		printf("1:Leggi tutti lo stato di tutti pin\n");
		printf("2:Leggi lo stato di un singolo pin\n");
		printf("Scelta = ");
		scanf ("%d",&scelta);
	
		if (scelta==1)	printf("\n\n GPIO = %d",mcp23008_leggiGpio());
		else if(scelta==2){
			printf("2:Inserisci il numero del pin(0..7)\n");
			printf("Pin = ");
			scanf ("%d",&pin);
			value=mcp23008_leggiGpio();
			value=value & (2^pin ); // maschra
			printf("Livello logico del pin= ");
			if (value==(2^pin ))printf("1\n");
			else printf("0\n");
		}
	}
	else if (scelta==4){//scrittura
		printf("1:Modifica tutta la porta GPIO\n");
		printf("2:Un singolo pin x volta\n");
		printf("Scelta = ");
		scanf ("%d",&scelta);
	
		if (scelta==1){
			printf("Inserisci il valore(0..FF) a cui si dovranno portare tutti i pin\n");
			printf("Valore = ");
			scanf ("%X",&value);
			// controllare che sia impostato tt in uscita.
			mcp23008_scrivi(GPIO,value);
		}
		else if(scelta==2){
			printf("Inserisci il numero del pin (0..7) e il valore (0..FF) a cui si dovrà portare\n");
			printf("Pin = ");
			scanf ("%d",&pin);
			printf("Valore = ");
			scanf ("%d",&level);
	
			// controllare che il pin sia impostato in uscita.
			value=mcp23008_leggiGpio();
			value = level<<pin;
			mcp23008_scrivi(GPIO,value);
		}
	}
	else if (scelta==5) return 1;
	printf("\n\n");
    }

}








