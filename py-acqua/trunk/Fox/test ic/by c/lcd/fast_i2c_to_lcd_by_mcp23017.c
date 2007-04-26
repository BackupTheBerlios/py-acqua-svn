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

#include "stdarg.h"
#include "string.h"






#define lcdMcp23017_id	0x27


//REGISTRI  X BANCO ZERO !
//x impostare direzione
// 1 = input
// 0 = output
#define	IODIRA	0X00
#define	IODIRB	0X01
	#define IO7	7
	#define IO6	6
	#define IO5	5
	#define IO4	4
	#define IO3	3
	#define IO2	2
	#define IO1	1
	#define IO0	0
// INVERTE LETTURA
// 1 = riflette il livello logico opposto a quello presente sul pin quando si legge GPIO
// 0 = lettura = stato del pin
#define	IPOLA	0X02 	
#define	IPOLB	0X03 	
	#define IP7	7
	#define IP6	6
	#define IP5	5
	#define IP4	4
	#define IP3	3
	#define IP2	2
	#define IP1	1
	#define IP0	0
// INTERRUPT AD OGNI CAMBIAMENTO
// 1 = abilitato
//	N.B.: bisogna configurare anche DEFVAL ed INTCON
// 0 = disabilitato
#define	GPINTENA	0X04
#define	GPINTENB	0X05
	#define GPINT7	7
	#define GPINT6	6
	#define GPINT5	5
	#define GPINT4	4
	#define GPINT3	3
	#define GPINT2	2
	#define GPINT1	1
	#define GPINT0	0
// LIVELLO LOGICO A CUI SI GENERE L'INTERRUPT
//   l'interrupt si genera quando sul pin c'è un livello 
//  opposto a quello impostato nel bit associato di questo registro.
#define	DEFVALA	0X06
#define	DEFVALB 0X07
	#define DEF7	7
	#define DEF6	6
	#define DEF5	5
	#define DEF4	4
	#define DEF3	3
	#define DEF2	2
	#define DEF1	1
	#define DEF0	0
//REGISTRO DI CONTROLLO DELL'INTERRUPT
// 1 = IL PIN È COMPARATO CON IL CORRISPONDENTE BIT IN DEFVAL
// 0 = IL PIN È COMPARATO CON LO STATO PRECEDENTE DELLO STESSO. (DEFVAL VIENE IGNORATO) 
#define	INTCONA	0X08
#define	INTCONB 0X09
	#define IOC7	7
	#define IOC6	6
	#define IOC5	5
	#define IOC4	4
	#define IOC3	3
	#define IOC2	2
	#define IOC1	1
	#define IOC0	0
//CONFIGURAZIONE DEI REGISTRI DELL' I/O EXPANDER
#define	IOCONA	0X0A
#define	IOCONB	0X0B
	#define BANK	7 	//SCELTA DEL BANCO DEI REGISTRI
						// 1 i regiastri assocciati ad ogni porta sono separati uin 2 banchi separati
						// 0 registri nello stesso banco (default)
						
	#define MIRROR	6	//SETTING DEI PIEDINI DI INTERRUPT
						// 1 INTA E INTB internamente connessi
						// 0 INTA è associato a porta e INTB a portb
		

	#define SREAD	5 	// LETTURA SEQUENZIALE
						// 1 = lettura sequenziale disabilitata, puntatore indirizzi non incrementato
						// 0 = lettura sequenziale abilitata, puntatore indirizzi incrementato

	#define DISSLW	4	//GESTISCE SLEW RATE DI SDA
						// 1 = disabilitato
						// 0 = abilitato
						
//	#define HAEN	3	//non presente in questo chip

	#define ODR		2	//CONFIGURA IL TIPO DI OUTPUT DEGLI 'INT' PIN
						// 1 = open drain
						// 0 = uscita del driver attiva

	#define INTPOL	1	// SETTA LA POLARITÀ DELL'OUTPUT PIN 'INT'
						// 1 = attivo a livello alto
						// 0 = attivo a livello basso
						
// Imposta le resistenze di pull-up sugli ingressi
// 1 = se il pin è configurato come input, viene applicata la resistenza di pullup
// 0 = nessun pullup
#define	GPPUA	0X0C
#define	GPPUB	0X0D
	#define PU7	7
	#define PU6	6
	#define PU5	5
	#define PU4	4
	#define PU3	3
	#define PU2	2
	#define PU1	1
	#define PU0	0
// Registro x abilitare gli interrupt
// 1 = interrupot abilitato
// 0 = interrupt disabilitato
#define	INTFA	0X0E
#define	INTFB	0X0F
	#define INT7	7
	#define INT6	6
	#define INT5	5
	#define INT4	4
	#define INT3	3
	#define INT2	2
	#define INT1	1
	#define INT0	0
// RIFLETTE I LIVELLI LOGICI DEI PIN IMPOSTATI COME INTERRUPT AL MOMENTO DEL CAMBIAMENTO DI STATO
// 1 = attivo alto
// 0 = attivo basso
#define	INTCAPA	0X10
#define	INTCAPB	0X11
	#define ICP7	7
	#define ICP6	6
	#define ICP5	5
	#define ICP4	4
	#define ICP3	3
	#define ICP2	2
	#define ICP1	1
	#define ICP0	0
// RIFLETTE IL LIVELLO LOGICO DEL PIN
// 1 = livello logico alto
// 0 = livelLo logico basso
#define	GPIOA	0X12
#define	GPIOB	0X13
	#define GP7	7
	#define GP6	6
	#define GP5	5
	#define GP4	4
	#define GP3	3
	#define GP2	2
	#define GP1	1
	#define GP0	0
// ACCEDE AL VALORE DEI LATCH DI USCITA
// 1 = livello logico alto
// 0 = livelLo logico basso
#define	OLATA	0X14  //LATCH
#define	OLATB	0X15  //LATCH
	#define OL7	7
	#define OL6	6
	#define OL5	5
	#define OL4	4
	#define OL3	3
	#define OL2	2
	#define OL1	1
	#define OL0	0


//***************
//LCD PIN
//**************

#define  lcd_port	0X12 //GPIOA
#define  lcd_E		3
#define  lcd_RS		2
#define  lcd_D4		4
#define  lcd_D5		5
#define  lcd_D6		6
#define  lcd_D7		7
  


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


#define I2C_DATA_LINE       PORTG
#define I2C_CLOCK_LINE      PORTG
#define I2C_DATA_PIN       24
#define I2C_CLOCK_PIN      25


#ifndef IO_SETGET_INPUT
#define IO_SETGET_INPUT   0x12
#endif
#ifndef IO_SETGET_OUTPUT
#define IO_SETGET_OUTPUT  0x13
#endif

#define i2c_delay(usecs) usleep(usecs)


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
    return (gpiogetbits(I2C_DATA_LINE,I2C_DATA_PIN))?(1):(0);    
}//        (gpiogetbits(PORTG, PG2))?(1):(0))

// Set the SDA line state
void i2c_data(int state) {
  if (state==1) 
    gpiosetbits(I2C_DATA_LINE,I2C_DATA_PIN);
  else 
    gpioclearbits(I2C_DATA_LINE,I2C_DATA_PIN);
}

// Set the SCL line state
void i2c_clk(int state) {
  if (state==1) 
    gpiosetbits(I2C_CLOCK_LINE,I2C_CLOCK_PIN);
  else 
     gpioclearbits(I2C_CLOCK_LINE,I2C_CLOCK_PIN);
}

// Set the SDA line as output
void i2c_dir_out(void) {
 gpiosetdir(PORTG, DIROUT, PG24);
}

// Set the SDA line as input
void i2c_dir_in(void) {
  gpiosetdir(PORTG, DIRIN, PG24);
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
//  MCP23017 ROUTINES
//*********************
int mcp23017_regLeggi(int reg){
	int data;
	i2c_start();
	i2c_outbyte(lcdMcp23017_id<<1); // accoda uno zero x dire scrivi
	i2c_outbyte(reg);
	i2c_start();
	i2c_outbyte((lcdMcp23017_id<<1)+1); // accoda un uno  x dire leggi 
	data=i2c_inbyte(0);
	i2c_stop();
	return data;
}

void mcp23017_regScrivi(int registro,int value){
	i2c_start();
	i2c_outbyte(lcdMcp23017_id<<1);
	i2c_outbyte(registro);
	i2c_outbyte(value);
	i2c_stop();
}


void mcp23017_pinWriteLevel(int gp,int pin,int level){
	int value;
	
///	printf("porta= %d\n",GPIOA);	
//	printf("pin= %d livello= %d\n",pin,level);
		
		
	value=mcp23017_regLeggi(GPIOA);
//	printf("letto= %d\n",value);
	
	if (level==1) value=value | (1 << pin ); // = 2^pin
	else if (level==0) value=value & ( 0xff -(1 << pin ));
	else printf("ERRORE LIVELLO ERATO: %d", level);
	

//	printf("scritto= %d\n",value);
	mcp23017_regScrivi(GPIOA,value);
	
///	value=mcp23017_regLeggi(GPIOA);
	//printf("verifica= %d\n",value);
}



void lcdMcpInit(){
//init input x 5 pulsanti
//init output x fili al display

	//imposta mcp
	
	
	
	mcp23017_regScrivi(IODIRA,0);//DISPLAY, TT OUT
	mcp23017_regScrivi(IODIRB,0);//pulsanti, tt in
	mcp23017_regScrivi(GPIOA,0);//uscite sul display a zero
	mcp23017_regScrivi(GPPUB,0);// pullup sui pulsanti
}


//*********************************************************************
// LCD functions
//*********************************************************************

// RS line
void lcd_rs(int level) { mcp23017_pinWriteLevel(lcd_port,lcd_RS,level); }
//  E line
void lcd_e(int level) { mcp23017_pinWriteLevel(lcd_port,lcd_E,level);}
// D4..7
void lcdD4(int level) { mcp23017_pinWriteLevel(lcd_port,lcd_D4,level);}
void lcdD5(int level) { mcp23017_pinWriteLevel(lcd_port,lcd_D5,level);}
void lcdD6(int level) { mcp23017_pinWriteLevel(lcd_port,lcd_D6,level);}
void lcdD7(int level) { mcp23017_pinWriteLevel(lcd_port,lcd_D7,level);}

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
	gpiosetdir(PORTG, DIROUT, I2C_CLOCK_PIN); //clock

	

	

 
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
  udelay(35);
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

int  main (void) {
int scelta;

	system ("clear");

	if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }
   
    for(;;){
	printf("GESTIONE LCD COMANDATO DA MCP23017\n");
	printf("Operazioni possibili:\n");
	
	printf("0:mcp\n");
	printf("1:lcd\n\n");
	printf("2:TEST\n");
	printf("3:Esci\n\n");
	printf("Scelta = ");
	scanf ("%X",&scelta);
 if (scelta==0)lcdMcpInit();
		
		else if (scelta==1)	lcd_init();
	
	else if (scelta==2){
	    lcd_locate(1,0);
	    lcd_printf("http://www.pyacqua.net");	
	    lcd_locate(1,1);
	    lcd_printf("Visitaci");		
	    lcd_locate(21,0);
	    lcd_printf("Ciao3");	
	    lcd_locate(21,1);
	    lcd_printf("Ciao4");		
	    

		printf("Frasi di prova scritte\n");	
	}
	else if (scelta==3) return 1;
    }
}








