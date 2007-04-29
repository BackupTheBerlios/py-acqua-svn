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



***********************************************************************************
// 
//   TEST DEL LCD PILOTATO IN I2C DAL CHIP MCP230016. si mcp230016 con 16 i/o
//
***********************************************************************************




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
***************
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
	y_pos(1,3);
	lcd_printf("Menu");			
	cursore_sceqgli_opz(3);
}





//*********************************
//***********************************
//******************** 
void barra_menu_vert(unsigned char type){
	if (type==0){
		y_pos(20,0);
		lcd_printf("|");
		y_pos(20,1);
		lcd_printf("|");
		y_pos(20,2);
		lcd_printf("|");
		y_pos(20,3);
		lcd_printf("V");
	}
	else if (type==1){
		y_pos(20,0);
		lcd_printf("^");
		y_pos(20,1);
		lcd_printf("|");
		y_pos(20,2);
		lcd_printf("|");
		y_pos(20,3);
		lcd_printf("V");
	}
	else if (type==2){
		y_pos(20,0);
		lcd_printf("^");
		y_pos(20,1);
		lcd_printf("|");
		y_pos(20,2);
		lcd_printf("|");
		y_pos(20,3);
		lcd_printf("|");
	}
	else if (type==3){
		y_pos(20,0);
		lcd_printf("|");
		y_pos(20,1);
		lcd_printf("|");
		y_pos(20,2);
		lcd_printf("|");
		y_pos(20,3);
		lcd_printf("|");
	}
}



void sk_menu_1_2_1(){
unsigned char scelta;
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
unsigned char scelta;
	y_pos(1,0);
	lcd_printf("<<  PH");	
	y_pos(1,2);
	lcd_printf("Ph = 6");
	scelta=aggiorna_cursore_opz(0,0);
	
}
void sk_menu_1_2_3(){
unsigned char scelta;
	y_pos(1,0);
	lcd_printf("<< CO2");	
	y_pos(3,2);
	lcd_printf("CO2 = 1 mg/m^3");
	scelta=aggiorna_cursore_opz(0,0);
}
void sk_menu_1_2(){
unsigned char scelta;
	y_pos(1,0);
	lcd_printf("<< VALORI SONDE");	
	y_pos(1,1);
	lcd_printf("Temperatura");	
	y_pos(1,2);
	lcd_printf("PH");
	y_pos(1,3);
	lcd_printf("CO2");
	barra_menu_vert(0);
	scelta=aggiorna_cursore_opz(0,3);//12=menu = 1_2
	sk_clear();
	if (scelta==0) udelay(1);//ritorna
	else if (scelta==1) sk_menu_1_2_1(); 
	else if (scelta==2) sk_menu_1_2_2();
	else if (scelta==3) sk_menu_1_2_3();
	
}

void sk_menu_1_1(){
	
	char valore[5];
//	int intervalli[6];
	// leggi rtc
	y_pos(0,0);
	lcd_printf("<<     DATA");			
	y_pos(2,2);
	//lcd_printf("15:00   25/04/07");
//ora 
  valore[0]=read_hour();
  lcd_printf("%02d:",valore[0]);
  valore[1]=read_min();
  lcd_printf("%02d  ",valore[1]);

//data 
  valore[2]=read_day();
  lcd_printf("%02d",valore[2]);
  valore[3]=read_month();
  lcd_printf("/%02d",valore[3]);
  valore[4]=read_year();
  lcd_printf("/%02d",valore[4]);

	// x,y,partenza,min,max
	valore[0]=inc_cifra(2,2,valore[0],0,24);// hh 
	valore[1]=inc_cifra(5,2,valore[1],0,59);// mm
	set_ora(valore[0],valore[1]);
	
	valore[2]=inc_cifra(9,2,valore[2],0,31);// gg
	valore[3]=inc_cifra(12,2,valore[3],0,12);// m
	valore[4]=inc_cifra(15,2,valore[4],7,20);// aa
	// verifica data x gg bisestili e gg de mesi
	set_data(valore[2],valore[3],valore[4]);
	
	//se ok salva il valore
	y_pos(4,3);
		
	if (true) lcd_printf("DATA SALVATA");
	else lcd_printf("DATA ERRATA");
	msDelay(2000);		

}
void sk_menu_1_3(){
unsigned char scelta;
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
	unsigned char scelta;
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
unsigned char valore[2],i;
	system ("clear");
    if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }    
    lcd_init();
    ds1307_init();
//skermate
	sk_init();
	for(;;){
		sk_main();
		
		while(p_status()!= P_OK){
			msDelay(1000); 
			if (p_status()==P_DOWN) return 1; // x debug

			y_pos(13,2);
	 		valore[0]=read_hour();
  			lcd_printf("%02X:",valore[0]);
  			valore[1]=read_min();
  			lcd_printf("%02X",valore[1]);

		} //aspetta finkè premuto   
		sk_clear();
		sk_menu_1(); 
		sk_clear();
	}
	printf("Programma terminato");
}








