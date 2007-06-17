//#Copyright (C) 2005, 2007 Py-Acqua
//#http://www.pyacqua.net
//#email: info@pyacqua.net
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
/*************************************************/


#include "stdio.h"
#include "stdlib.h"
#include "unistd.h" 
#include "time.h"
#include "sys/ioctl.h"
#include "fcntl.h"     
#include "asm/etraxgpio.h"
#include "stdarg.h"
#include "string.h"
#include "errno.h"
#include "termios.h"
#include "sys/types.h"
#include "sys/stat.h"
#include "netinet/in.h"
#include "sys/socket.h"
#include "netdb.h"
#include "signal.h"
#include "arpa/inet.h"
#include "stdlib.h"
#include "syslog.h"
#include "stdarg.h"
#include "net/if.h"
//lib
#include "include/foxacqua_i2c.h"	//routine i2c
#include "include/mcp230xx_sub.c"	// routine comuni a questi mcp
#include "include/foxacqua_lcd.c"	//routine x comunicazione e controllo del lcd 
#include "include/foxacqua_rtc.c"	//routine x comunicare con l'rtc
#include "include/foxacqua_ciabatta.c"	//routine x gestire la ciabatta
#include "include/eeprom_24xx.c"	// x sonde
#include "include/mcp3421.c" 		// a/d converter @ i2c
//#include "include/board.c" 		// a/d converter @ i2c

// menu
#include "include/foxacqua_menu.c"	//schermate dei menu


#define RX_BUFFER_LEN 1024
#define TX_BUFFER_LEN 1024

#ifndef IO_SETGET_INPUT
#define IO_SETGET_INPUT 	0x12
#endif

#ifndef IO_SETGET_OUTPUT
#define IO_SETGET_OUTPUT 	0x13
#endif

//****************************************************
// Socket functions
//****************************************************

// Send a formatted string to a socket

int socket_printf(int fs, char *format, ...) {
	va_list argptr;
	char msg[TX_BUFFER_LEN];
	
  va_start(argptr,format);
  vsprintf(msg,format,argptr);
  va_end(argptr);
	
  write(fs,msg,strlen(msg));
  return 0;
}	

int ch;
int value;
int cs;


int xml_monitor(int local_port) {
 // int cs;
  int s;
  int sockfl;
  int size_csa;
  struct sockaddr_in csa;
  struct sockaddr_in sa; 
  int rc;
  int yes = 1;
  int rxpointer=0;
	char rxbuffer[RX_BUFFER_LEN];
	//int ch;
	//int value;
	char zero[1];
	
	zero[0]=0;
  rxbuffer[rxpointer]=0;

  memset(&sa, 0, sizeof(sa));

  sa.sin_family = AF_INET;         
  sa.sin_port = htons(local_port); 
  sa.sin_addr.s_addr = INADDR_ANY; 

  // Create a socket
  
  s = socket(AF_INET, SOCK_STREAM, 0);
  if (s < 0) {
    printf("Error opening control socket\n");
    return -1;
  }

  // Socket in non blocking mode
  sockfl = fcntl(s, F_GETFL, 0);
  fcntl(s, F_SETFL, sockfl | O_NONBLOCK);

  setsockopt(s, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int));

  rc = bind(s, (struct sockaddr *)&sa, sizeof(sa));
  if (rc) {
    printf("Error binding control socket\n");
    return -1;
  }

  rc = listen(s, 1);

  if (rc) {
    printf("Error listening control socket\n");
    return -1;
  } 
  
  while(1) {  
    
    size_csa = sizeof(csa);
    //cs = accept(s, (struct sockaddr *)&csa, &size_csa); // Qui non si ferma
    cs = accept(s, (struct sockaddr *)&csa, (socklen_t *)&size_csa);
    if (cs > 0) {
    	
      sockfl = fcntl(cs, F_GETFL, 0);
      fcntl(cs, F_SETFL, sockfl | O_NONBLOCK);
    
      // Read data loop
			value=0;	
      for (;;) {
				sleep(1);

     		socket_printf(cs,"<analog>");
				for (ch=0;ch<4;ch++) {
					i2c_start();
					if (i2c_outbyte(0x92)==0) {
						printf("NACK received\n");
					}
					
					if (i2c_outbyte(ch)==0) {
						printf("NACK received\n");
					}
					i2c_stop();
							
					i2c_start();
					if (i2c_outbyte(0x93)==0) {
						printf("NACK received\n");
					}
			
					i2c_inbyte(1); 					// Last conversion result
					value=i2c_inbyte(1); 		// Current conversion result
					i2c_stop();
				
					printf("%3d ",value);
					socket_printf(cs,"<input line=\"%d\" value=\"%d\"/>",ch,value);
					
				}	
				socket_printf(cs,"</analog>");
				printf("\n");
				
			  write(cs,zero,1); 
      }
      printf("Close\n");
      close(s);
      return -1;
    } 
  }
  printf("Rx socket accept timeout\n");
  sleep(2);
  return -1;
} 

/*int main(int argc, char *argv[]) {
  int port=3023;

	printf("xmlvoltmeter\n");
	  
  while(1) {  
  	
 		if (i2c_open()<0) {
	    printf("i2c open error\n");
	    return 1;
		}
  	
    xml_monitor(port);
    
   	i2c_close();
  } 
  return 0; 
}

*/


//*****************
//	MAIN
//*****************
int  main (int argc, char *argv[]) {
	
	unsigned char valore[2];
	int port=3023;
	printf("xmlvoltmeter\n");
	
	//system ("clear");
	if (i2c_open()<0) { 
		printf("Apertura del bus I2C fallita\n"); 
		return 1; }
	xml_monitor(port);
		
	//board_init();
	lcd_init();
	ciabatta_init();
	ds1307_init();
	ad_init(0x68);

	printf("valor %s\n","ciaooo"); 
ad_regLeggi(mcp_ad1);
	printf("valor %d\n",valo[0]); 

	printf("valor %d\n",valo[1]); 

	



//skermate
	sk_init();
	for(;;){
		sk_main();
		
		while(p_status()!= P_OK){
 ad_regLeggi(mcp_ad1);
	printf("valor %d\n",valo[0]); 

	printf("valor %d\n",valo[1]);


			msDelay(1000); 
			if (p_status()==P_DOWN) return 1; // x debug, alla sua pressione il prog termina.
			// scrive ora
			y_pos(15,0);
	 		valore[0]=read_hour();
  			lcd_printf("%02d:",valore[0]);
  			valore[1]=read_min();
  			lcd_printf("%02d",valore[1]);
			//valore temperatura
			//valore ph
			// valore gh
		} //aspetta finkè premuto   
		sk_clear();
		sk_menu_1(); 
		sk_clear();
	}
	socket_printf(cs,"<prova>");
	socket_printf(cs,"<input line=\"%d\" value=\"%d\"/>",ch,value);
	socket_printf(cs,"</prova>");
}
