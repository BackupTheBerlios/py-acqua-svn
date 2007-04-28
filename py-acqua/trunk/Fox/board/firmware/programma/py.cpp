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
/*************************************************
si ok
metti il link x ora



//***********************************************************************************
// 
//   TEST DEL LCD PILOTATO IN I2C DAL CHIP MCP230016. si mcp230016 con 16 i/o
//
//***********************************************************************************




Collegamenti elettrici:
IOG25 J7.13 as SCL
IOG24 J7.21 as SDA. 

RESISTENZE DI PULLUP SU I2C DI 1K !

di fabbrica tt i pin sono configurati in ingresso

PIN A0,A1,A2 A VCC
RESET A VCC

****************************************************/

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
#include "foxacqua_i2c.h"
#include "mcp23017_reg.h"
#include "mcp23017_sub.c"

#include "lcd_i2c.c"




/***************
//	SCHERMATE
//
//	MENU
//
//***************
//0,0	riga1 
//0,20  riga2
//1,0   riga3
//1,20  riga4*/


void sk_clear(){
	lcd_clear(); 
}



void sk_init(){

int i;
 	lcd_locate(0,7);
	lcd_printf("VISITA");	
		
 	lcd_locate(1,2);
	lcd_printf("www.pyacqua.net"); 
	lcd_locate(1,20);
	lcd_printf("-------------------");	
	for(i=8;i>0;i--) msDelay(250);
	sk_clear();
	
}

void sk_main(){
	lcd_locate(0,1);
	lcd_printf("GESTIONE  ACQUARIO");			
	lcd_locate(0,35);
	lcd_printf("16:21");			
 		
	lcd_locate(1,21);
	lcd_printf("Menu");			
	cursore_sceqgli_opz(4);
}





//*********************************
//***********************************
//******************** 



void sk_menu_1_1(){
//	int scelta;
//	int intervalli[6];
	lcd_locate(0,0);
	lcd_printf("<<     DATA");			
	lcd_locate(0,22);
	lcd_printf("15:00   25/04/07");			
	select_cifra(3,2,16);
}


void sk_menu_1_2(){
int scelta;
	lcd_locate(0,1);
	lcd_printf("<<  VALORI SONDE");	

	scelta=aggiorna_cursore_opz(1,4);
	
}


void sk_menu_1_3(){
int scelta;
	lcd_locate(0,0);
	lcd_printf("<<     INFO");			

	scelta=aggiorna_cursore_opz(1,2);
	
}




void sk_menu_1(){
	int scelta;
	lcd_locate(0,1);
	lcd_printf("<<     Menu 1");			
	lcd_locate(1,1);
	lcd_printf("DATA");			
	lcd_locate(0,21);
	lcd_printf("VALORI SONDE");			
	lcd_locate(1,21);
	lcd_printf("INFO");
	scelta=aggiorna_cursore_opz(1,4);
	sk_clear();
	if (scelta==1) udelay(1);//ritorna
	else if (scelta==2) sk_menu_1_1(); 
	else if (scelta==3) sk_menu_1_2();
	else if (scelta==4) sk_menu_1_2();
}

//*****************
//		MAIN
//*****************
int  main (void) {
	system ("clear");
    if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }    
    lcd_init();		
//skermate
	sk_init();
	
	
		sk_main();
	
		while(p_status()!= P_OK) msDelay(50); //aspetta finkè premuto   
		sk_clear();
		sk_menu_1(); 
		sk_clear();
    
	        
return 1;
}








