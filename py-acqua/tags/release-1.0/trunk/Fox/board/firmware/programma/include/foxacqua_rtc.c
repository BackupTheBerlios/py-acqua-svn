 
//i2c
char orario[9];
char data_attuale[9];
unsigned char giorno_in,mese_in,anno_in,ora_in,minuto_in;

unsigned char read_sec (void)
{
unsigned char secs;
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

unsigned char read_min (void)
{
unsigned char mins;
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

unsigned char read_hour (void)
{
unsigned char hours;
 i2c_stop();
 i2c_start();
 if (i2c_outbyte(0xd0)==0) {i2c_stop();}
 i2c_outbyte(2);
 i2c_start();
 if (i2c_outbyte(0xd1)==0) {i2c_stop();}
 hours=i2c_inbyte(2);
 i2c_stop();


//passare da hex a decimale


 return hours;
}

unsigned char read_daysett (void)
{
unsigned char daysett;
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

unsigned char read_day (void)
{
unsigned char days;
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

unsigned char read_month (void)
{
unsigned char months;
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

unsigned char read_year (void)
{
unsigned char years;
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
unsigned char secondi;
secondi=read_sec();
i2c_stop();
i2c_start();
if (i2c_outbyte(0xd0)==0) {i2c_stop();}
i2c_outbyte(0);
i2c_outbyte(secondi & 0x7F);
i2c_stop();
i2c_start();
}

void timenow (unsigned char modo)
{
unsigned char sec,min,hour;
 
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
unsigned char gio,mes,ann;

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



void set_data (unsigned char g_in, unsigned char m_in, unsigned char a_in)
{
unsigned char temp;
itoa(g_in,16);//ritorna valore dentro stringa.. m ke skifo di funzione ki l'ha fatta???????
temp=atoi(stringa);

i2c_stop();
i2c_start();
if (i2c_outbyte(0xd0)==0){i2c_stop();}
i2c_outbyte(4);
i2c_outbyte(temp);
i2c_stop();
i2c_start();

itoa(m_in,16);//ritorna valore dentro stringa.. m ke skifo di funzione ki l'ha fatta???????
temp=atoi(stringa);
i2c_stop();
i2c_start();
if (i2c_outbyte(0xd0)==0){i2c_stop();}
i2c_outbyte(5);
i2c_outbyte(temp);
i2c_stop();
i2c_start();

itoa(g_in,16);//ritorna valore dentro stringa.. m ke skifo di funzione ki l'ha fatta???????
temp=atoi(stringa);
i2c_stop();
i2c_start();
if (i2c_outbyte(0xd0)==0){i2c_stop();}
i2c_outbyte(6);
i2c_outbyte(temp);
i2c_stop();
i2c_start();
}

void set_ora ( unsigned char o_in,unsigned char min_in)
{
unsigned char temp;
//passa da base 10 a 16
//num in char

//itoa(o_in,10);//ritorna valore dentro stringa.. m ke skifo di funzione ki l'ha fatta???????
//temp=atoi(stringa);


i2c_stop();
i2c_start();
if (i2c_outbyte(0xd0)==0){i2c_stop();}
i2c_outbyte(2);
i2c_outbyte(o_in);
i2c_stop();
i2c_start();

//itoa(min_in,10);//ritorna valore dentro stringa.. m ke skifo di funzione ki l'ha fatta???????
//temp=atoi(stringa);

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
unsigned char giorno,mese,anno,ore,minuti;

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
