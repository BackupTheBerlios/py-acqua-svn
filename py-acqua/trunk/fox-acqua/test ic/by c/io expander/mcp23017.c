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
//   TEST DELL'INTEGRATO MCP23017 
//
//*********************************************************************




Collegamenti elettrici:
IOG25 J7.13 as SCL
IOG24 J7.21 as SDA. 

RESISTENZE DI PULLUP SU I2C DI 1K !

di fabbrica tt i pin sono configurati in ingresso

PIN A0,A1,A2 A vcc
RESET A VCC

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
#define i2c_delay(usecs) usleep(usecs)

int i2c_fd;




#define myMcp23017_id	0x27

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


#ifndef IO_SETGET_INPUT
#define IO_SETGET_INPUT   0x12
#endif
#ifndef IO_SETGET_OUTPUT
#define IO_SETGET_OUTPUT  0x13
#endif


char stringa[2];

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


//*********************
//  MCP23017 ROUTINES
//*********************
int mcp23017_leggi(int reg){
	int data;
	i2c_start();
	i2c_outbyte(myMcp23017_id<<1); // accoda uno zero x dire scrivi
	i2c_outbyte(reg);
	i2c_start();
	i2c_outbyte((myMcp23017_id<<1)+1); // accoda un uno  x dire leggi 
	data=i2c_inbyte(0);
	i2c_stop();
	return data;
}

void mcp23017_scrivi(int registro,int value){

	i2c_start();
	i2c_outbyte(myMcp23017_id<<1);
	i2c_outbyte(registro);
	i2c_outbyte(value);
	i2c_stop();

}
void mcp23017_ttOut(){
	mcp23017_scrivi(IODIRA,0);
	mcp23017_scrivi(IODIRB,0);
	mcp23017_scrivi(GPIOA,0);
	mcp23017_scrivi(GPIOB,0);
	
	
}
void mcp23017_ttIn(){
	mcp23017_scrivi(IODIRA,0xff);
	mcp23017_scrivi(GPPUA,0xff);//pull-up su tutti
	mcp23017_scrivi(IODIRB,0xff);
	mcp23017_scrivi(GPPUB,0xff);//pull-up su tutti
	
}

void mcp23017_scriviGpio(int porta,int value ){	
	mcp23017_scrivi(porta,value);
}

int mcp23017_leggiGpio(int porta){
	int gpio_level;
	gpio_level=mcp23017_leggi(porta);
	return gpio_level;
}




int  main (void) {
int scelta,pin,value,level,porta,i;

    if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }
	system ("clear");
    
    for(;;){

	printf("GESTIONE MCP23017\n");
	printf("Operazioni possibili:\n");
	printf("1:Imposta tutti i pin in ingresso con pull-up interno\n");
	printf("2:Imposta tutti i pin in uscita senza interrupt\n");
	printf("3:Lettura dello stato dei pin\n");
	printf("4:Scrittura del valore logico dei pin\n");
	printf("5:Esci\n\n");
	printf("Scelta = ");
	scanf ("%X",&scelta);
		system ("clear");
	if (scelta==1){
			mcp23017_ttIn();
		printf("Comando eseguito");	
	}
	else if (scelta==2){
		mcp23017_ttOut();
		printf("Comando eseguito");
	}
	else if (scelta==3){//lettura
		printf("1:Leggi lo stato di tutti pin\n");
		printf("2:Leggi lo stato di un singolo pin\n");
		printf("Scelta = ");
		scanf ("%d",&scelta);
	
		if (scelta==1)	printf("\n\n GPIOA = %d - GPIOB = %d",mcp23017_leggiGpio(GPIOA),mcp23017_leggiGpio(GPIOB));
		else if(scelta==2){
			printf("2:Inserisci il numero della porta(0=A, 1=B)\n");
			printf("PORTA = ");
			scanf ("%d",&porta);
			
			printf("2:Inserisci il numero del pin(0..7)\n");
			printf("Pin = ");
			scanf ("%d",&pin);
			value=mcp23017_leggiGpio(GPIOA+porta);
			printf("Livello logico del pin= ");

			value=value & (1 << pin );
			if (value==(1 << pin )) printf("1\n");
			else printf("0\n");
		}
	}
	else if (scelta==4){//scrittura
		printf("1:Modifica tutte e due le porte GPIO\n");
		printf("2:Un singolo pin x volta\n");
		printf("Scelta = ");
		scanf ("%d",&scelta);
	
		if (scelta==1){
			printf("Inserisci il valore(0..FF) a cui si dovranno portare tutti i pin di PORTA\n");
			printf("Valore = ");
			scanf ("%X",&value);
			// controllare che sia impostato tt in uscita.
			mcp23017_scrivi(GPIOA,value);
			printf("Inserisci il valore(0..FF) a cui si dovranno portare tutti i pin di PORTB\n");
			printf("Valore = ");
			scanf ("%X",&value);
			// controllare che sia impostato tt in uscita.
			mcp23017_scrivi(GPIOB,value);
			
		}
		else if(scelta==2){
			printf("Inserisci la porta (0=A, 1=B) da modificare\n");
			printf("Porta = ");
			scanf ("%d",&porta);
	
			printf("Inserisci il numero del pin (0..7) e il valore (0..1) a cui si dovrà portare\n");
			printf("Pin = ");
			scanf ("%d",&pin);
			printf("Valore = ");
			scanf ("%d",&level);
	
			// controllare che il pin sia impostato in uscita.
			value=mcp23017_leggiGpio(GPIOA+porta);
			printf("letto= %d",value);
    		
			if (level==1) value=value | (1 << pin ); // = 2^pin
			else value=value & ( 0xff -(1 << pin ));		
			
			if (porta==0) mcp23017_scrivi(GPIOA,value);
			else if (porta==1) mcp23017_scrivi(GPIOB,value);
			else printf("ERRORE");
			
		}
	}
	else if (scelta==5) return 1;
	printf("\n\n");
    }

}








