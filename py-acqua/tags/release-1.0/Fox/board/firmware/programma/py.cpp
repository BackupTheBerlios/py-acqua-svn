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


#include "stdio.h"
#include "stdlib.h"
#include "unistd.h" 
#include "time.h"
#include "sys/ioctl.h"
#include "fcntl.h"     
#include "asm/etraxgpio.h"
#include "stdarg.h"
#include "string.h"
//lib
#include "include/foxacqua_i2c.h"	//routine i2c
#include "include/mcp230xx_sub.c"	// routine comuni a questi mcp
#include "include/foxacqua_lcd.c"	//routine x comunicazione e controllo del lcd 
#include "include/foxacqua_rtc.c"	//routine x comunicare con l'rtc
#include "include/foxacqua_ciabatta.c"	//routine x gestire la ciabatta
#include "include/eeprom_24xx.c"	// x sonde
#include "include/mcp3421.c" 		// a/d converter @ i2c
// menu
#include "include/foxacqua_menu.c"	//schermate dei menu


//*****************
//		MAIN
//*****************
int  main (void) {
unsigned char valore[2];
	system ("clear");

    	if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }
	
	lcd_init();
	ciabatta_init();
	ds1307_init();

//skermate
	sk_init();
	for(;;){
		sk_main();
		
		while(p_status()!= P_OK){
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
}








