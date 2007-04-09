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
Collegamenti elettrici:
IOG25 J7.13 as SCL
IOG24 J7.21 as SDA. 

PIN DELLA EEPROM: DA 1 A 3 A MASSA


#define I2C_DATA_LINE        1<<24
#define I2C_CLOCK_LINE        1<<25



i2c_fd = open("/dev/gpiog", O_RDWR);
instead of /dev/gpiob
****************************************************/

#include "stdio.h"
#include "stdlib.h"

#include "unistd.h" 
#include "time.h"
#include "sys/ioctl.h"
#include "fcntl.h"     
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


#define I2C_DATA_LINE       1<<24
#define I2C_CLOCK_LINE      1<<25

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

int ext_eeprom_ready(int id){
	int ack;
	i2c_start();
	ack=i2c_outbyte(id);
	i2c_stop();
	return ack;

}



void write_ext_eeprom(int id,long int address, int data){

while(!ext_eeprom_ready(id));
	i2c_start();
	i2c_outbyte((id|(int)(address>>7))&0xfe);
	i2c_outbyte(address);
	i2c_outbyte(data);
	i2c_stop();



}

int read_ext_eeprom(int id, long int address){
int data;
while(!ext_eeprom_ready(id));
	i2c_start();
	i2c_outbyte((id|(int)(address>>7))&0xfe);
	i2c_outbyte(address);
	i2c_start();
	i2c_outbyte((id|(int)(address>>7))|1);
	data=i2c_inbyte(0);
	i2c_stop();
	return data;//tra parentesi data (data)
}


int  main (void) {
int scelta;
int cella,dato,dato_chek;

    if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }


    for(;;){

	printf("GESTIONE EEPROM 24xx\n");
	printf("Operazioni possibili:\n");
	printf("1:Lettura\n");
	printf("2:Scrittura\n");
	printf("3:Esci\n");
	
	scanf ("%X",&scelta);
	if (scelta==1){
		printf("Inserisci il numero della cella da leggere ( 0..FF) ");
		scanf ("%X",&cella);
		dato=read_ext_eeprom(0xa0,cella);
		printf("dato= %d\n",dato);
	}
	else if (scelta==2){
		printf("Inserisci il numero della cella (0..FF) da scrivere ");
		scanf ("%X",&cella);
		printf("Inserisci il numero del dato (0..FF) da memorizare ");
		scanf ("%X",&dato);
		write_ext_eeprom(0xa0,cella,dato); // A0= ID EEPROM OPZIONI: A0,A2,A4,A6,A8,AA,AC,AE
		//verifica il dato	
		dato_chek=read_ext_eeprom(0xa0,cella); // A0= ID EEPRM
		if (dato==dato_chek) printf("dato scritto correttamente");
		else printf("errore, dato scritto= %d",dato_chek);
	}
	else if (scelta==3) return 1;
    
}
}
