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
#include "linux/gpio_syscalls.h"
#include <netdb.h>



/*

prima di eseguire il prog

[root@axis /root]714# free
              total         used         free       shared      buffers
  Mem:        13968         9640         4328            0         1704
 Swap:            0            0            0
Total:        13968         9640         4328



a runtime
[root@axis /root]714# free
              total         used         free       shared      buffers
  Mem:        13968         9720         4248            0         1704
 Swap:            0            0            0
Total:        13968         9720         4248

-----------------


80 k


*/



const char alfabeto[37][2]={" ","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"};
#define delay_ms(ms) msDelay(ms)
#define delay_us(ms) udelay(ms)

// connessioni
#include "include/foxacqua_i2c.h"	//routine i2c


//include
#include "include/mcp230xx_sub.c"	// routine comuni a questi mcp
#include "include/foxacqua_lcd.c"	//routine x comunicazione e controllo del lcd 

#include "include/foxacqua_ciabatta.c"	//routine x gestire la ciabatta
#include "include/eeprom_24xx.c"	// x sonde
#include "include/board.c" 		// board
// menu
#include "include/foxacqua_menu.c"	//schermate dei menu

#include "include/socket.c" 		// socket


//*****************
//	MAIN
//*****************
int  main (int argc, char *argv[]) {

//orologio
	time_t now;
	struct tm *tm_now;
	char conv[3];
	char buff[20];

//match 
	unsigned char hr;
	unsigned char min;
	
	int presa,timer;//x cicli for
	//aspetta alim stabile
		
	
	delay_ms(50);
	sk_clear();
	delay_ms(50);

	system ("clear");

    	if (i2c_open()<0) { 	printf("Apertura del bus I2C fallita\n"); return 1; }
	board_init();		printf("--Init board					[PASS]\n"); 
	lcd_init();		printf("--Init lcd					[PASS]\n"); 
	ciabatta_init();	printf("--Init ciabatta					[PASS]\n"); 
	socket_init();		printf("--Init socket on 15000				[PASS]\n"); 
	board_init();
	ciabatta_init();
	sk_init();
	printf("\nfox-acqua in esecuzione.\n"); 



	if(fork() != 0){ //eseguito dal processo padre
		for(;;){
			y_pos(1,3);
			lcd_printf("MENU");
			cursore_scegli_opz(3);
		
			while(p_status()!= P_OK){
				//disegna lo stato delle prese
				y_pos(1,0);
				lcd_printf(" P:");
				for(presa=1;presa<8;presa++) lcd_printf("%d",presa_read_level(presa));
			
		
				//mostra ora e data
  			

				y_pos(12,1);
				now = time ( NULL );
  				tm_now = localtime ( &now );
//%a  /* Abbreviated weekday */
//%A  /* Full weekday */
//%b  /* Abbreviated month */
//%b  /* Full month */
//%c  /* Full date and time */
//%d  /* Day of the month (1-31) */
//%H  /* Hour (24 hour clock) */
//%I  /* Hour (12 hour clock) */
//%j  /* Day of the year (1-366)*/
//%m  /* Month (1-12) */
//%M  /* Minute (0-59) */
//%p  /* AM/PM for 12 hour clock */
//%S  /* Second (0-60) */
//%U  /* Week number from Sunday */
//%w  /* Weekday (0-6) from Sunday */
//%W  /* Week number from Monday */
//%x  /* Full date */
//%X  /* Full time of day */
//%y  /* Year without century */
//%Y  /* Year with century */
//%Z  /* Time zone */
//%%  /* Print a % character */
  				strftime ( buff, sizeof buff, "%H:%M:%S", tm_now );
  				strftime ( conv, sizeof conv, "%H", tm_now );	hr=atoi(conv);
  				strftime ( conv, sizeof conv, "%M", tm_now );	min=atoi(conv);

  				lcd_printf( "%s", buff );
				y_pos(12,2);
				strftime ( buff, sizeof buff, "%d/%m/%y", tm_now );
  				lcd_printf( "%s", buff );




				//----match tra rtc e timer vari----
		
				//controlla se un delle 10 prese ha un timer attivo
				for (presa=1;presa<8;presa++){            //sfoglia le prese
					for(timer=0;timer<10;timer++){         //sfoglia i 10 timer di questa presa
						if (presa_timer_stato[presa][timer]<99){
						//allora c'� un timer impostato x questa presa
						//controlla se deve scattare in questo momento
						// !!!!!!!!!!!!!!
						// risolvere il problema nel caso in cui: l'utente sia nel menu,
						// e quando si ritorna qui l'orologio � andato
						// dopo l'evento di un timer.
							if (presa_timer[presa][timer][0]==hr){
								if (presa_timer[presa][timer][1]==min){//ok, allora imposta la presa.
									presa_set_level(presa,presa_timer_stato[presa][timer]);
								}
							}
						}
					}
				}
			} //luppa fink� non � premuto
			sk_clear();
			//socket_printf(cs,"Menu_1_0");
			//write(cs,zero,1); //fa scrivee effettivamente la frase sopra svuotando il buffer ke ha interno(penso).
		
			sk_menu_1();
			sk_clear();
		}//for
	}//fork

	else  sok();   //eseguito dal figlio

}
