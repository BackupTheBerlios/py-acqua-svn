// 02/09/07 - manzoni: ho modificato le routine eliminando i ritardi molto + veloxce !!!!!!
//cambiata l routin itoa, molto + performante ora. prima convertiva solo numeri a 2 cifre e lasciava una variabile globale come variabile in cui andava salvato il risultato !!!

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

char stringa[2];
int i2c_fd;
//-----------------------------
//FUNZIONI
//-----------------------------
/*
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
*/

char* itoa (int n){
  int i=0,j;
  char* s;
  char* u;

  s= (char*) malloc(17);
  u= (char*) malloc(17);
  
  do{
    s[i++]=(char)( n%10+48 );
    n-=n%10;
  }
  while((n/=10)>0);
  for (j=0;j<i;j++)
  u[i-1-j]=s[j];

  u[j]='\0';
  return u;
}



// Software delay in us
inline void udelay(int us) {
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
inline unsigned char i2c_getbit(void) {
  unsigned int value;
  value=ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_READBITS));
  if ((value&(I2C_DATA_LINE))==0) 
    return 0;
  else 
    return 1;
}
// Set the SDA line state
inline void i2c_data(unsigned char state) {
  if (state==1) 
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_DATA_LINE);
  else 
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_DATA_LINE);
}
// Set the SCL line state
inline void i2c_clk(unsigned char state) {
  if (state==1) 
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETBITS), I2C_CLOCK_LINE);
  else 
    ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_CLRBITS), I2C_CLOCK_LINE);
}
// Set the SDA line as output
inline void i2c_dir_out(void) {
  int iomask;
  iomask = I2C_DATA_LINE;
  ioctl(i2c_fd, _IO(ETRAXGPIO_IOCTYPE, IO_SETGET_OUTPUT), &iomask);
}
// Set the SDA line as input
inline void i2c_dir_in(void) {
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
inline unsigned char i2c_inbyte(unsigned char ack) {
  unsigned char value = 0;
  unsigned char bitvalue;
  register unsigned char i;

  // Read data byte
  i2c_dir_in();
  for (i=0;i<8;i++) {
    i2c_clk(1);
 //   udelay(5);
    bitvalue = i2c_getbit();
    value |= bitvalue;
    if (i<7) value <<= 1;
    i2c_clk(0);
 //   udelay(5);
  }
  // Send Ack
  if(ack){
  i2c_dir_out();
  i2c_data(0);
  i2c_clk(1);
 // udelay(5);
  i2c_clk(0);
  }
 // udelay(200);	
  return value;
}
// Send a start sequence to I2C bus
inline void i2c_start(void){
  i2c_dir_out();
  i2c_clk(1);
  i2c_data(1);
//  udelay(5);
  i2c_data(0);
}
// Send a stop sequence to I2C bus
inline void i2c_stop(void) {
  i2c_dir_out();
  i2c_clk(1);
  i2c_data(0);
//  udelay(5);
  i2c_data(1);
}
// Send a byte to the I2C bus and return the ack sequence from slave
inline unsigned char i2c_outbyte(unsigned char x) {
    register unsigned char i;
    unsigned char ack;
    
    i2c_clk(0);
    for (i=0;i<8;i++) {
        if (x & 0x80) 
        i2c_data(1);
        else
        i2c_data(0);
        i2c_clk(1);
//        udelay(5);
        i2c_clk(0);
 //       udelay(5);
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
