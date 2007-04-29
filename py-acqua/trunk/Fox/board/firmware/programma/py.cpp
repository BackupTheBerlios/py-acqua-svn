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
#include "include/foxacqua_i2c.h"
#include "include/mcp23017_sub.c"
#include "include/foxacqua_lcd.c"
#include "include/foxacqua_rtc.c"
#include "include/foxacqua_ciabatta.c"





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
 	y_pos(7,0);
	lcd_printf("VISITA");	
		
 	y_pos(2,1);
	lcd_printf("www.pyacqua.net"); 
	y_pos(0,3);
	lcd_printf("--------------------");	
	msDelay(3000);
	sk_clear();
	
}

void sk_main(){
	y_pos(1,0);
	lcd_printf("GESTIONE  ACQUARIO");			
	y_pos(5,2);
	lcd_printf("16:21");			
	y_pos(1,3);
	lcd_printf("Menu");			
	cursore_sceqgli_opz(3);
}





//*********************************
//***********************************
//******************** 





void sk_menu_1_2_1(){
int scelta;
	y_pos(1,0);
	lcd_printf("<<  TEMPERATURA");		
	y_pos(1,2);
	//controllo se sonda presente
		//se si leggila temperatura
		//altrimenti mex di errore
	lcd_printf("Temp=10");
//scrivi temp
	lcd_printf("C");
	scelta=aggiorna_cursore_opz(0,0);
}
void sk_menu_1_2_2(){
int scelta;
	y_pos(1,0);
	lcd_printf("<<  PH");	
	y_pos(1,2);
	lcd_printf("Ph = 6");
	scelta=aggiorna_cursore_opz(0,0);
	
}
void sk_menu_1_2_3(){
int scelta;
	y_pos(1,0);
	lcd_printf("<< CO2");	
	y_pos(3,2);
	lcd_printf("CO2 = 1 mg/m^3");
	scelta=aggiorna_cursore_opz(0,0);
}
void sk_menu_1_2(){
int scelta;
	y_pos(1,0);
	lcd_printf("<< VALORI SONDE");	
	y_pos(1,1);
	lcd_printf("Temperatura");	
	y_pos(1,2);
	lcd_printf("PH");
	y_pos(1,3);
	lcd_printf("CO2");
	scelta=aggiorna_cursore_opz(0,3);
	sk_clear();
	if (scelta==0) udelay(1);//ritorna
	else if (scelta==1) sk_menu_1_2_1(); 
	else if (scelta==2) sk_menu_1_2_2();
	else if (scelta==3) sk_menu_1_2_3();
	
}

void sk_menu_1_1(){
	int cifra;
	int valore;
//	int intervalli[6];
	// leggi rtc
	y_pos(0,0);
	lcd_printf("<<     DATA");			
	y_pos(2,2);
	//lcd_printf("15:00   25/04/07");
//ora 
  ora_in=read_hour();
  lcd_printf("%02d:",ora_in);
  minuto_in=read_min();
  lcd_printf("%02d  ",minuto_in);
//data 
  giorno_in=read_day();
  lcd_printf("%02d",giorno_in);
  mese_in=read_month();
  lcd_printf("/%02d",mese_in);
  anno_in=read_year();
  lcd_printf("/%02d",anno_in);

	// x,y,partenza,min,max
	valore=inc_cifra(2,2,0,0,24);// hh 
	valore=inc_cifra(5,2,0,0,59);// mm
	valore=inc_cifra(9,2,0,0,31);// gg
	valore=inc_cifra(12,2,0,0,12);// m
	valore=inc_cifra(15,2,0,7,20);// aa
	clean_row(1);	
	clean_row(3);
// verifica data

	//se ok salva il valore
	y_pos(4,3);
		
	if (true) lcd_printf("DATA SALVATA");
	else lcd_printf("DATA ERRATA");
	msDelay(2000);		

}
void sk_menu_1_3(){
int scelta;
	y_pos(1,0);
	lcd_printf("<<     INFO");			
	y_pos(1,1);
	lcd_printf("Progetto opensource");			
	y_pos(1,2);
	lcd_printf("  per la gestione   ");			
	y_pos(1,3);
	lcd_printf("     di acquari     ");		
	scelta=aggiorna_cursore_opz(0,0);//min,max quindi solo ritornare indietro
	
}




void sk_menu_1(){

	// problema... cm fare x scorrere le voci in verticale????
	int scelta;
	y_pos(1,0);
	lcd_printf("<<     Menu 1");			
	y_pos(1,1);
	lcd_printf("DATA");			
	y_pos(1,2);
	lcd_printf("VALORI SONDE");			
	y_pos(1,3);
	lcd_printf("INFO");
	scelta=aggiorna_cursore_opz(0,3);
	sk_clear();
	if (scelta==0) udelay(1);//ritorna
	else if (scelta==1) sk_menu_1_1(); 
	else if (scelta==2) sk_menu_1_2();
	else if (scelta==3) sk_menu_1_3();
}

//*****************
//		MAIN
//*****************
int  main (void) {
int valore;
	system ("clear");
    if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }    
    lcd_init();
    ds1307_init();
//skermate
	sk_init();
	printf("ok, programma partito. premi pulsante giu x uscire");
	for(;;){
		sk_main();
		
		while(p_status()!= P_OK){
			msDelay(50); 
			if (p_status()==P_DOWN) return 1; // x debug
		} //aspetta finkè premuto   
		sk_clear();
		sk_menu_1(); 
		sk_clear();
	}
	printf("Programma terminato");
}








