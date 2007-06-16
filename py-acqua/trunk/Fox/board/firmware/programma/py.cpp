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
/*************************************************/

#include <stdio.h>     
#include <string.h>    
#include <unistd.h>    
#include <fcntl.h>     
#include <errno.h>     
#include <termios.h>   
#include <sys/types.h>
#include <sys/stat.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <netdb.h>
#include <signal.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <time.h>
#include <sys/ioctl.h>
#include <asm/etraxgpio.h>
#include <syslog.h> 
#include <stdarg.h>
#include <net/if.h>



// connessioni
#include "include/foxacqua_i2c.h"	//routine i2c
//#include "include/socket.c" 		// soket






#include "include/mcp230xx_sub.c"	// routine comuni a questi mcp
#include "include/foxacqua_lcd.c"	//routine x comunicazione e controllo del lcd 
#include "include/foxacqua_rtc.c"	//routine x comunicare con l'rtc
#include "include/foxacqua_ciabatta.c"	//routine x gestire la ciabatta
#include "include/eeprom_24xx.c"	// x sonde
#include "include/mcp3421.c" 		// a/d converter @ i2c
#include "include/board.c" 		// board

// menu
#include "include/foxacqua_menu.c"	//schermate dei menu





//*****************
//	MAIN
//*****************
int  main (int argc, char *argv[]) {
//int port=3023;
unsigned char valore[2];


	system ("clear");

    	if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }
	board_init();
	lcd_init();
	ciabatta_init();
	ds1307_init();
	ad_init(0x68);

	printf("\nfox-acqua in esecuzione.\n"); 

//skermate
	sk_init();
	for(;;){
		y_pos(15,0);
		valore[0]=read_hour();
  		lcd_printf("%02d:",valore[0]);
  		valore[1]=read_min();
  		lcd_printf("%02d",valore[1]);
			
		sk_main();
	




		while(p_status()!= P_OK){
 //ad_regLeggi(mcp_ad1);
	//printf("valor %d\n",valo[0]); 

	//printf("valor %d\n",valo[1]);


			//xml_monitor(port);
   			//i2c_close();

			msDelay(200); 

			if (p_status()==P_DOWN) return 1; // x debug, alla sua pressione il prog termina.
			// scrive ora
			//y_pos(15,0);
	 		//valore[0]=read_hour();
  			//lcd_printf("%02d:",valore[0]);
  			//valore[1]=read_min();
  			//lcd_printf("%02d",valore[1]);
			







		} //luppa finkè non premuto   

	msDelay(200); 
buzzer_set_level(0);
	msDelay(200); 
peristaltica_set_level(0);
	msDelay(200); 


		sk_clear();
		sk_menu_1(); 
		sk_clear();
	}
	msDelay(200); 
buzzer_set_level(0);
	msDelay(200); 
peristaltica_set_level(0);
	msDelay(200); 
}








