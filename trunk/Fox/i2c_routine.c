
#include "unistd.h"    
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
char orario[9];
char data_attuale[9];
char stringa[2];
int giorno_in,mese_in,anno_in,ora_in,minuto_in;
//-----------------------------
//FUNZIONI
//-----------------------------


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

printf ("%s \r\n"," ");
printf ("Ora (oo): (%02X)  ",ora_in);scanf ("%X",&ora_in);
printf ("Minuti (mm): (%02X)  ",minuto_in);scanf ("%X",&minuto_in);
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


int  main (void)
{
     if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }

	ds1307_init();

	input_data();
	set_data(giorno_in,mese_in,anno_in);
	input_ora();
	set_ora(ora_in,minuto_in);

        //timenow(0);
        //datanow();

	//printf ("%s \r\n", " ");
	//printf("Data: %s \r\n",data_attuale);
	//printf("Ora: %s \r\n",orario);
	//printf ("%s \r\n", " ");
	
	printf ("%s \r\n", " ");
	setsystemdate();
	printf ("%s \r\n", " ");
}
