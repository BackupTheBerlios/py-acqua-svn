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


int min,hr,sec,day,mth,year;// x rtc
int presa,timer;//x cicli for
//aspetta alim stabile
delay_ms(50);
sk_clear();
delay_ms(50);

	system ("clear");

    	if (i2c_open()<0) { 	printf("Apertura del bus I2C fallita\n"); return 1; }
	board_init();		printf("--Init board				[PASS]\n"); 
	lcd_init();		printf("--Init lcd					[PASS]\n"); 
	ciabatta_init();	printf("--Init ciabatta					[PASS]\n"); 
	socket_init();	printf("--Init socket on 15000				[PASS]\n"); 
	printf("\nfox-acqua in esecuzione.\n"); 



REBOOT:
printf("reboot0\n");
	board_init();
	ciabatta_init();

   sk_init();
//   rtc_init();



	if(fork() != 0){ //eseguito dal processo padre

   	y_pos(1,3);
      lcd_printf("MENU");
   	cursore_scegli_opz(3);

		while(p_status()!= P_OK){
//disegna lo stato delle prese
      	y_pos(1,0);
         lcd_printf(" P:");
      	for(presa=1;presa<8;presa++) {//1..7
            lcd_printf("%d",presa_read_level(presa));
         }

//mostra ora e data
      	y_pos(12,1);
//         hr = rm_bcd(read_ds1302(0x85));
 //        min = rm_bcd(read_ds1302(0x83));
   //      sec = rm_bcd(read_ds1302(0x81));
         lcd_printf("%d:%d:%d",hr,min,sec);

         y_pos(12,2);
//         day = rm_bcd ( read_ds1302 ( 0x87 ) );
  //       mth = rm_bcd ( read_ds1302 ( 0x89 ) );
    //     year = rm_bcd ( read_ds1302 ( 0x8d ) );
         lcd_printf("%d/%d/%d",day,mth,year);


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
//controlla se dv riavviarsi
    		if (p_status()==P_DOWN) {
				sk_clear();
   			//	printf("\nFox-acqua spenta.\n");
   			//	return 1; // x debug, alla sua pressione il prog termina.
            goto REBOOT;
         }
		} //luppa fink� non � premuto
		sk_clear();
		//socket_printf(cs,"Menu_1_0");
		//write(cs,zero,1); //fa scrivee effettivamente la frase sopra svuotando il buffer ke ha interno(penso).

		sk_menu_1();
      sk_clear();
	}


	else  sok();   //eseguito dal figlio


}
