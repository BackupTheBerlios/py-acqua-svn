 
//i2c
char orario[9];
char data_attuale[9];
int giorno_in,mese_in,anno_in,ora_in,minuto_in;

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
