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

//*********************************************************************
// 
//   viene letta la data e l'ora dal ds1307 
//   e visualizzata sul display lcd
//
//*********************************************************************

#include "stdio.h"     
#include "stdlib.h"     
#include "unistd.h"    
#include "sys/ioctl.h"
#include "fcntl.h"     
#include "asm/etraxgpio.h"
#include "stdarg.h"
#include "string.h"

//i2c  

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
//i2c
int i2c_fd;
char orario[9];
char data_attuale[9];
char stringa[2];
int giorno_in,mese_in,anno_in,ora_in,minuto_in;



//*********************************************************************
//  funzioni di supporto
//*********************************************************************


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

// Software delay in us

void usDelay(int us) {
  int i,a;
  int delayvar=10;
  
  for (a=0;a<us;a++) {
    for (i=0;i<33;i++) {
      delayvar*=2;        
      delayvar/=2;
    } 
  }
}   

void itoa(int valore, int base)
{
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


//*********************************************************************
// LCD functions
//*********************************************************************

// Set RS line
void lcd_rs_hi(int fd) {
  ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), 1 << 12);
}

// Reset RS line
void lcd_rs_lo(int fd) {
  ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), 1 << 12);
}

// Set E line
void lcd_e_hi(int fd) {
  ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), 1 << 13);
}

// Reset E line
void lcd_e_lo(int fd) {
  ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), 1 << 13);
}

// Send an hi pulse to E line
void lcd_e_strobe(int fd) {
	lcd_e_hi(fd);
	lcd_e_lo(fd);
}

// Send a nibble (4 bit) to LCD
void lcd_put_nibble(int fd, int value) {
	if (value&0x01) ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), 1 << 8);
	else ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), 1 << 8);
	if (value&0x02) ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), 1 << 9);
	else ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), 1 << 9);
	if (value&0x04) ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), 1 << 10);
	else ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), 1 << 10);
	if (value&0x08) ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), 1 << 11);
	else ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), 1 << 11);
}

// Send a char to LCD
// data: Ascii char or instruction to send
// mode: 0 = Instruction, 1 = Data
void lcd_putc(int fd,unsigned char data, int mode) {
	int a;
	
	if (mode==0) lcd_rs_lo(fd);
	else lcd_rs_hi(fd);
	
	a=(data>>4)&0x000F;
	lcd_put_nibble(fd,a);
	lcd_e_strobe(fd);
	a=data&0x000F;
	lcd_put_nibble(fd,a);
	lcd_e_strobe(fd);
} 

// Lcd initialization
void lcd_init(int fd) {
 	unsigned long data, mask;

  data = mask = 0xFF << 8;
  ioctl(fd, _IO(ETRAXGPIO_IOCTYPE, 0x13), &mask);
  if ((mask & data) != data)  printf("Check your kernel config\n");

	lcd_rs_lo(fd);
	lcd_e_lo(fd);
	msDelay(15);
	
	lcd_put_nibble(fd,0x03);
	lcd_e_strobe(fd);
	msDelay(4);
	lcd_e_strobe(fd);
	msDelay(2);
	lcd_e_strobe(fd);
	msDelay(2);
	lcd_put_nibble(fd,0x02);
	lcd_e_strobe(fd);
	msDelay(1);

  lcd_putc(fd,0x28,0);
	msDelay(1);
  lcd_putc(fd,0x06,0);
	msDelay(1);
  lcd_putc(fd,0x0C,0);
	msDelay(1);
  lcd_putc(fd,0x01,0);
	msDelay(2);
} 

// Locate cursor on LCD
// row (0-2)
// col (1-39)
void lcd_locate(int fd, int row, int col) {
  lcd_putc(fd,0x80+row*0x40+col,0);
  usDelay(35);
} 

// Clear LCD
void lcd_clear(int fd) {
  lcd_putc(fd,0x01,0);
  msDelay(2);
} 

// Lcd version of printf
void lcd_printf(int fd,char *format, ...) {
  int i;
  
  va_list argptr;
  char buffer[1024];
  
  va_start(argptr,format);
  vsprintf(buffer,format,argptr);
  va_end(argptr);
  
  for (i=0;i<strlen(buffer);i++) {
    lcd_putc(fd,buffer[i],1);
  }
}


//*********************************************************************
// i2c functions
//*********************************************************************

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

// Open the GPIOB dev 
//int i2c_open(void) {
//  i2c_fd = open("/dev/gpiog", O_RDWR);
//  i2c_data(1);
//  i2c_dir_out();
//  i2c_clk(1);
//  i2c_data(1);
//  udelay(100);
//  return i2c_fd;
//}

int i2c_open(void) {
  i2c_fd = open("/dev/gpiog", O_RDWR);
	i2c_data(I2C_DATA_HIGH);
 	i2c_dir_out();
	i2c_clk(I2C_CLOCK_HIGH);
	i2c_data(I2C_DATA_HIGH);
	i2c_delay(100);
  return i2c_fd;
}


// Close the GPIOB dev 
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
//*********************************************************************
// dispositivi I2C functions
//*********************************************************************


//LETTURA PRESSIONE
float PressureRead (void){
  unsigned char buf[2];
  int i;
  float pressure;
  
  i2c_stop();
  i2c_start();
  if (i2c_outbyte(0xF1)==0) {
    i2c_stop();
    printf("Ricevuto NACK 1\n");
    return -1;
  }
  buf[0]=i2c_inbyte(1); 
  buf[1]=i2c_inbyte(0); 
  i2c_stop();

  //printf ("Byte 1: [%03d] Byte 2 [%03d]\n",buf[0],buf[1]);
  
  // Converto in float
  i=buf[0];
  i<<=8;
  i+=buf[1];
  pressure=0.09375*i+762.5;
  
  return pressure;
}


short int read_sec (void)
{
 short int secs;
 i2c_stop();
 i2c_start();
 if (i2c_outbyte(0xd0)==0) {i2c_stop();}
 i2c_outbyte(0);
 i2c_start();
 if (i2c_outbyte(0xd1)==0) {i2c_stop();}
 secs=i2c_inbyte(0);
 i2c_stop();
 return secs;
}

short int read_min (void)
{
 short int mins;
 i2c_stop();
 i2c_start();
 if (i2c_outbyte(0xd0)==0) {i2c_stop();}
 i2c_outbyte(1);
 i2c_start();
 if (i2c_outbyte(0xd1)==0) {i2c_stop();}
 mins=i2c_inbyte(1);
 i2c_stop();
 return mins;
}

short int read_hour (void)
{
 short int hours;
 i2c_stop();
 i2c_start();
 if (i2c_outbyte(0xd0)==0) {i2c_stop();}
 i2c_outbyte(2);
 i2c_start();
 if (i2c_outbyte(0xd1)==0) {i2c_stop();}
 hours=i2c_inbyte(2);
 i2c_stop();
 return hours;
}

short int read_daysett (void)
{
 short int daysett;
 i2c_stop();
 i2c_start();
 if (i2c_outbyte(0xd0)==0) {i2c_stop();}
 i2c_outbyte(3);
 i2c_start();
 if (i2c_outbyte(0xd1)==0) {i2c_stop();}
 daysett=i2c_inbyte(3);
 i2c_stop();
 return daysett;
}

short int read_day (void)
{
 short int days;
 i2c_stop();
 i2c_start();
 if (i2c_outbyte(0xd0)==0) {i2c_stop();}
 i2c_outbyte(4);
 i2c_start();
 if (i2c_outbyte(0xd1)==0) {i2c_stop();}
 days=i2c_inbyte(4);
 i2c_stop();
 return days;
}

short int read_month (void)
{
 short int months;
 i2c_stop();
 i2c_start();
 if (i2c_outbyte(0xd0)==0) {i2c_stop();}
 i2c_outbyte(5);
 i2c_start();
 if (i2c_outbyte(0xd1)==0) {i2c_stop();}
 months=i2c_inbyte(5);
 i2c_stop();
 return months;
}

short int read_year (void)
{
 short int years;
 i2c_stop();
 i2c_start();
 if (i2c_outbyte(0xd0)==0) {i2c_stop();}
 i2c_outbyte(6);
 i2c_start();
 if (i2c_outbyte(0xd1)==0) {i2c_stop();}
 years=i2c_inbyte(6);
 i2c_stop();
 return years;
}

//INIZIALIZZAZIONE RTC_DS1307
void ds1307_init (void)
{
short int secondi;
secondi=read_sec();
i2c_stop();
i2c_start();
if (i2c_outbyte(0xd0)==0) {i2c_stop();}
i2c_outbyte(0);
i2c_outbyte(secondi & 0x7F);
i2c_stop();
i2c_start();
}

void timenow (int modo)
{
 int sec,min,hour;
 
 sec=read_sec();
 min=read_min();
 hour=read_hour();
 
 if (modo==0)
 {
 itoa(hour,16);
 orario[0]=stringa[0];
 orario[1]=stringa[1];
 orario[2]=':';
 itoa(min,16);
 orario[3]=stringa[0];
 orario[4]=stringa[1];
 orario[5]=':';
 itoa(sec,16);
 orario[6]=stringa[0];
 orario[7]=stringa[1];
 orario[8]='\0';
 }

 if (modo==1)
 {
 itoa(hour,16);
 orario[0]=stringa[0];
 orario[1]=stringa[1];
 orario[2]='.';
 itoa(min,16);
 orario[3]=stringa[0];
 orario[4]=stringa[1];
 orario[5]='\0';
 }
}


void datanow (void)
{
 int gio,mes,ann;

 gio=read_day();
 mes=read_month();
 ann=read_year();

 itoa(gio,16);
 data_attuale[0]=stringa[0];
 data_attuale[1]=stringa[1];
 data_attuale[2]='/';
 itoa(mes,16);
 data_attuale[3]=stringa[0];
 data_attuale[4]=stringa[1];
 data_attuale[5]='/';
 itoa(ann,16);
 data_attuale[6]=stringa[0];
 data_attuale[7]=stringa[1];
 data_attuale[8]='\0';

}

void input_data (void)
{
system ("clear");

giorno_in=read_day();
mese_in=read_month();
anno_in=read_year();


printf ("Giorno (gg): (%02X)  ",giorno_in);scanf ("%X",&giorno_in);
printf ("Mese (mm): (%02X)  ",mese_in);scanf ("%X",&mese_in);
printf ("Anno (aa): (%02X)  ",anno_in);scanf ("%X",&anno_in);
}

void input_ora (void)
{
ora_in=read_hour();
minuto_in=read_min();
//888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
printf ("%s \r\n"," ");
printf ("Ora (oo): (%02X)  ",ora_in);
scanf ("%X",&ora_in);

printf ("Minuti (mm): (%02X)  ",minuto_in);
scanf ("%X",&minuto_in);
}


void set_data (short int g_in, short int m_in, short int a_in)
{
i2c_stop();
i2c_start();
if (i2c_outbyte(0xd0)==0){i2c_stop();}
i2c_outbyte(4);
i2c_outbyte(g_in);
i2c_stop();
i2c_start();

i2c_stop();
i2c_start();
if (i2c_outbyte(0xd0)==0){i2c_stop();}
i2c_outbyte(5);
i2c_outbyte(m_in);
i2c_stop();
i2c_start();

i2c_stop();
i2c_start();
if (i2c_outbyte(0xd0)==0){i2c_stop();}
i2c_outbyte(6);
i2c_outbyte(a_in);
i2c_stop();
i2c_start();
}

void set_ora (short int o_in, short int min_in)
{
i2c_stop();
i2c_start();
if (i2c_outbyte(0xd0)==0){i2c_stop();}
i2c_outbyte(2);
i2c_outbyte(o_in);
i2c_stop();
i2c_start();

i2c_stop();
i2c_start();
if (i2c_outbyte(0xd0)==0){i2c_stop();}
i2c_outbyte(1);
i2c_outbyte(min_in);
i2c_stop();
i2c_start();

i2c_stop();
i2c_start();
if (i2c_outbyte(0xd0)==0){i2c_stop();}
i2c_outbyte(0);
i2c_outbyte(0x00);
i2c_stop();
i2c_start();
}

void setsystemdate (void)
{
int giorno,mese,anno,ore,minuti;

char comando[20]="date ";

giorno=read_day();
mese=read_month();
anno=read_year();
ore=read_hour();
minuti=read_min();

itoa(mese,16);
comando[5]=stringa[0];
comando[6]=stringa[1];

itoa(giorno,16);
comando[7]=stringa[0];
comando[8]=stringa[1];

itoa(ore,16);
comando[9]=stringa[0];
comando[10]=stringa[1];

itoa(minuti,16);
comando[11]=stringa[0];
comando[12]=stringa[1];

itoa(anno,16);
comando[13]='2';
comando[14]='0';
comando[15]=stringa[0];
comando[16]=stringa[1];

comando[17]='\0';

system(comando);
}


int main(void) {
//variabili
  int fd;
//  char *parola = "02/09/06";
//controllo configurazione pin  
  if ((fd = open("/dev/gpiog", O_RDWR)) < 0) {
    printf("/dev/gpiog error");
    exit(1);
  }
  if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }
// init
  lcd_init(fd);
  ds1307_init();
//corpo
//----------------
  system ("clear");
  printf("Programma data\n\n");
 
//data
  lcd_locate(fd,0,0);
 
  giorno_in=read_day();
  lcd_printf(fd,"%02X",giorno_in);
  printf("O");
  
  mese_in=read_month();
  lcd_printf(fd,"/%02X",mese_in);
  printf("O");
  
  anno_in=read_year();
  lcd_printf(fd,"/%02X",anno_in);
  printf("O");
//ora 
  ora_in=read_hour();
  lcd_printf(fd,"--%02X:",ora_in);
  printf("O");
  
  minuto_in=read_min();
  lcd_printf(fd,"%02X",minuto_in);
  printf("O\n");
  
  
  
//terminale  
  printf("dati trasmessi al display\n");
  
  
  
  close(fd);
  exit(0);


  
  
  
  
  
}
