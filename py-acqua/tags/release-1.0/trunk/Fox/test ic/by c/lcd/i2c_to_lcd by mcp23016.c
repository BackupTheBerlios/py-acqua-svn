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



//***********************************************************************************
// 
//   TEST DEL LCD PILOTATO IN I2C DAL CHIP MCP230016. si mcp230016 con 16 i/o
//
//***********************************************************************************




Collegamenti elettrici:
IOG25 J7.13 as SCL
IOG24 J7.21 as SDA. 

RESISTENZE DI PULLUP SU I2C DI 1K !

di fabbrica tt i pin sono configurati in ingresso

PIN A0,A1,A2 A VCC
RESET A VCC

****************************************************/

#include "stdio.h"
#include "stdlib.h"
#include "unistd.h" 
#include "time.h"
#include "sys/ioctl.h"
#include "fcntl.h"     
#include "asm/etraxgpio.h"
#include "stdarg.h"
#include "string.h"




#define lcdMcp23016_id	0x27



// RIFLETTE IL LIVELLO LOGICO DEL PIN
// 1 = livello logico alto
// 0 = livelLo logico basso
#define	GPIO0	0X00
	#define GP07	7
	#define GP06	6
	#define GP05	5
	#define GP04	4
	#define GP03	3
	#define GP02	2
	#define GP01	1
	#define GP00	0
#define	GPI01	0X01
	#define GP17	7
	#define GP16	6
	#define GP15	5
	#define GP14	4
	#define GP13	3
	#define GP12	2
	#define GP11	1
	#define GP10	0
// ACCEDE AL VALORE DEI LATCH DI USCITA
// 1 = livello logico alto
// 0 = livelLo logico basso
#define	OLAT0	0X02  //LATCH
	#define OL07	7
	#define OL06	6
	#define OL05	5
	#define OL04	4
	#define OL03	3
	#define OL02	2
	#define OL01	1
	#define OL00	0
#define	OLAT1	0X03  //LATCH
	#define OL17	7
	#define OL16	6
	#define OL15	5
	#define OL14	4
	#define OL13	3
	#define OL12	2
	#define OL11	1
	#define OL10	0
// INVERTE LETTURA
// 1 = riflette il livello logico opposto a quello presente sul pin quando si legge GPIO
// 0 = lettura = stato del pin
#define	IPOL0	0X04	
	#define IP07	7
	#define IP06	6
	#define IP05	5
	#define IP04	4
	#define IP03	3
	#define IP02	2
	#define IP01	1
	#define IP00	0
#define	IPOL1	0X05
	#define IP17	7
	#define IP16	6
	#define IP15	5
	#define IP14	4
	#define IP13	3
	#define IP12	2
	#define IP11	1
	#define IP10	0
//REGISTRI
//x impostare direzione
// 1 = input
// 0 = output
#define	IODIR0	0X06	
	#define IO07	7
	#define IO06	6
	#define IO05	5
	#define IO04	4
	#define IO03	3
	#define IO02	2
	#define IO01	1
	#define IO00	0
#define	IODIR1	0X07	
	#define IO17	7
	#define IO16	6
	#define IO15	5
	#define IO14	4
	#define IO13	3
	#define IO12	2
	#define IO11	1
	#define IO10	0
// RIFLETTE I LIVELLI LOGICI DEI PIN IMPOSTATI COME INTERRUPT AL MOMENTO DEL CAMBIAMENTO DI STATO
// 1 = attivo alto
// 0 = attivo basso
#define	INTCAP0	0X08	//SOLA LETTURA
	#define ICP07	7
	#define ICP06	6
	#define ICP05	5
	#define ICP04	4
	#define ICP03	3
	#define ICP02	2
	#define ICP01	1
	#define ICP00	0
#define	INTCAP1	0X09	//SOLA LETTURA
	#define ICP17	7
	#define ICP16	6
	#define ICP15	5
	#define ICP14	4
	#define ICP13	3
	#define ICP12	2
	#define ICP11	1
	#define ICP10	0
// SETTA LA VELOCITÀ CON CUI CAMPIONA GLI INGRESSI IMPOSTATI COME INTERRUPT X GENERARE L'INTERRUPT
// 1 = lento (32ms)
// 0 = veloce (200us)
#define	IOCON0	0X0A
	#define IARES0	0
#define	IOCON1	0X0B
	#define IARES1	0

//***************
//LCD PIN
//**************

#define  lcd_E		GP00
#define  lcd_RS		GP01
#define  lcd_D4		GP02
#define  lcd_D5		GP03
#define  lcd_D6		GP04
#define  lcd_D7		GP05
  


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

//*********************
//  MCP23008 ROUTINES
//*********************
int mcp23016_regLeggi(int reg){
	int data;
	i2c_start();
	i2c_outbyte(lcdMcp23016_id<<1); // accoda uno zero x dire scrivi
	i2c_outbyte(reg);
	i2c_start();
	i2c_outbyte((lcdMcp23016_id<<1)+1); // accoda un uno  x dire leggi 
	data=i2c_inbyte(0);
	i2c_stop();
	return data;
}

void mcp23016_regScrivi(int registro,int value){
	i2c_start();
	i2c_outbyte(lcdMcp23016_id<<1);
	i2c_outbyte(registro);
	i2c_outbyte(value);
	i2c_stop();
}
void mcp23016_ttOut(){
	mcp23016_reScrivi(IODIR0,0);
	mcp23016_regcrivi(IODIR1,0);
}
void mcp23016_ttIn(){
	mcp23016_regScrivi(IODIR0,255);
	mcp23016_regScrivi(IODIR1,255);
}

void mcp23016_pinWriteLevel(int GP,pin,level){
	int value;
	
	value=mcp23016_leggiGpio(GP);
	value = level<<pin;
	mcp23008_scrivi(GP,value);
}



void mcp23016_scriviGpio(int GP,int value){	
	mcp23016_scrivi(IODIR0+GP,value);
}

int mcp23016_leggiGpio(int GP){
	int gpio_level;
	gpio_level=mcp23016_leggi(GPIO0+GP);
	return gpio_level;
}

void lcdMcpInit(){
//init input x 5 pulsanti
//init output x fili al display


//*********************************************************************
// LCD functions
//*********************************************************************

// RS line
void lcd_rs(int level) { mcp23016_pinWriteLevel(0,RS,level); }
//  E line
void lcd_e(int level) { mcp23016_pinWriteLevel(0,E,level);}
// D4..7
void lcdD4(int level) { mcp23016_pinWriteLevel(0,lcd_D4,level);}
void lcdD5(int level) { mcp23016_pinWriteLevel(0,lcd_D5,level);}
void lcdD6(int level) { mcp23016_pinWriteLevel(0,lcd_D6,level);}
void lcdD7(int level) { mcp23016_pinWriteLevel(0,lcd_D7,level);}

void lcd_e_strobe() {
	lcd_e(1);
	lcd_e(0);
}

// Send a nibble (4 bit) to LCD
void lcd_put_nibble( int value) {
	if (value&0x01) lcdD4(1);
	else 			lcdD4(0);
	if (value&0x02) lcdD5(1);
	else 			lcdD5(0);
	if (value&0x04) lcdD6(1);
	else 			lcdD6(0);
	if (value&0x08) lcdD7(1);
	else 			lcdD7(0);
}

// Send a char to LCD
// data: Ascii char or instruction to send
// mode: 0 = Instruction, 1 = Data
void lcd_putc(unsigned char data, int mode) {
	int a;
	
	if (!mode) lcd_rs(0);
	else lcd_rs(1);
	
	a=(data>>4)&0x000F;
	lcd_put_nibble(a);
	lcd_e_strobe();
	a=data&0x000F;
	lcd_put_nibble(a);
	lcd_e_strobe();
} 

// Lcd initialization
void lcd_init() {
 	unsigned long data, mask;
				
	//SETTA IO DELL'MCP
 
	lcd_rs(0);
	lcd_e(0);
	msDelay(15);
	
	lcd_put_nibble(0x03);
	lcd_e_strobe();
	msDelay(4);
	lcd_e_strobe();
	msDelay(2);
	lcd_e_strobe();
	msDelay(2);
	lcd_put_nibble(0x02);
	lcd_e_strobe();
	msDelay(1);

  	lcd_putc(0x28,0);
	msDelay(1);
  	lcd_putc(0x06,0);
	msDelay(1);
  	lcd_putc(0x0C,0);
	msDelay(1);
 	lcd_putc(0x01,0);
	msDelay(2);
} 

// Locate cursor on LCD
// row (0-2)
// col (1-39)
void lcd_locate(int row, int col) {
  lcd_putc(0x80+row*0x40+col,0);
  usDelay(35);
} 

// Clear LCD
void lcd_clear(int fd) {
  lcd_putc(0x01,0);
  msDelay(2);
} 

// Lcd version of printf
void lcd_printf(char *format, ...) {
  int i;
  
  va_list argptr;
  char buffer[1024];
  
  va_start(argptr,format);
  vsprintf(buffer,format,argptr);
  va_end(argptr);
  
  for (i=0;i<strlen(buffer);i++) {
    lcd_putc(buffer[i],1);
  }
}


//*****************
//		MAIN
//*****************
}
int  main (void) {
int scelta;

    if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }
    
    for(;;){
	printf("GESTIONE MCP23016\n");
	printf("Operazioni possibili:\n");
	printf("1:TEST\n");
	printf("2:Esci\n\n");
	printf("Scelta = ");
	scanf ("%X",&scelta);
	if (scelta==1){
	 	lcd_locate(0,0);
	    lcd_printf("Ciao");
		printf("Frase  di prova scritta\n");	
	}
	else if (scelta==2) return 1;
    }
}








