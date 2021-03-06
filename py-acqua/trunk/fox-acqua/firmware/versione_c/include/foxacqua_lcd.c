//#Copyright (C) 2005, 2007 Py-acqua
//#http://www.pyacqua.net
//#
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
//#
//#    Gestione del database
#include "lcdbymcp23016.h"

#define P_UP		1
#define P_DOWN		2
#define P_LEFT		3
#define P_RIGHT		4
#define P_OK		5

#define lcdMcp_id	0x20

void aspetta(){
  while(27==mcp230xx_regLeggi(lcdMcp_id,mcp23016GP1));//aspetta il pulsante ok rilasciato
}


int p_status(){
	unsigned char valore;
   

   valore=mcp230xx_regLeggi(lcdMcp_id,mcp23016GP1);
	if (valore==31) return 0;
	else if (valore==30) return (P_DOWN);
	else if (valore==29) return (P_RIGHT);
	else if (valore==27) return (P_OK);
	else if (valore==23) return (P_UP);
	else if (valore==15) return (P_LEFT);
   msDelay(2);
   
   
}
	

//*********************************************************************
// LCD functions
//*********************************************************************

// RS line
void lcd_rs(unsigned char level) { mcp230xx_pinWriteLevel(lcdMcp_id,lcd_port,lcd_RS,level); }
//  E line
void lcd_e(unsigned char level) { mcp230xx_pinWriteLevel(lcdMcp_id,lcd_port,lcd_E,level);}
// D4..7
void lcdD4(unsigned char level) { mcp230xx_pinWriteLevel(lcdMcp_id,lcd_port,lcd_D4,level);}
void lcdD5(unsigned char level) { mcp230xx_pinWriteLevel(lcdMcp_id,lcd_port,lcd_D5,level);}
void lcdD6(unsigned char level) { mcp230xx_pinWriteLevel(lcdMcp_id,lcd_port,lcd_D6,level);}
void lcdD7(unsigned char level) { mcp230xx_pinWriteLevel(lcdMcp_id,lcd_port,lcd_D7,level);}
void lcd_e_strobe() {
	lcd_e(1);
	lcd_e(0);
}
// Send a nibble (4 bit) to LCD
void lcd_put_nibble( unsigned char value) {
	if (value&0x01) lcdD4(1);
	else 			lcdD4(0);
	if (value&0x02) lcdD5(1);
	else 			lcdD5(0);
	if (value&0x04) lcdD6(1);
	else 			lcdD6(0);
	if (value&0x08) lcdD7(1);
	else 			lcdD7(0);
}
// Send a char to LCD
void lcd_putc(unsigned char data, unsigned char mode) {
// data: Ascii char or instruction to send
// mode: 0 = Instruction, 1 = Data
	int a;
	
	if (!mode) lcd_rs(0);
	else lcd_rs(1);
	
	a=(data>>4)&0x000F;
	lcd_put_nibble(a);
	lcd_e_strobe();
	a=data&0x000F;
	lcd_put_nibble(a);
	lcd_e_strobe();
} 
// Lcd initialization
void lcdMcpInit(){
//init input x 5 pulsanti
//init output x fili al display

	//imposta mcp
	mcp230xx_regScrivi(lcdMcp_id,mcp23016IODIR0,0);//DISPLAY, TT OUT
	mcp230xx_regScrivi(lcdMcp_id,mcp23016IODIR1,0xff);//pulsanti, tt in
	mcp230xx_regScrivi(lcdMcp_id,mcp23016GP0,0);//uscite sul display a zero
	//mcp230xx_regScrivi(lcdMcp_id,mcp23017GPIOB,0);// pullup DISATTIVATI sui pulsanti
}
void lcd_init() {
	lcdMcpInit();

	lcd_rs(0);
	lcd_e(0);
	msDelay(15);
	
	lcd_put_nibble(0x03);
	lcd_e_strobe();
	msDelay(4);
	lcd_e_strobe();
	msDelay(2);
	lcd_e_strobe();
	msDelay(2);
	lcd_put_nibble(0x02);
	lcd_e_strobe();
	msDelay(1);

  	lcd_putc(0x28,0);
	msDelay(1);
  	lcd_putc(0x06,0);
	msDelay(1);
  	lcd_putc(0x0C,0);
	msDelay(1);
 	lcd_putc(0x01,0);
	msDelay(2);
} 

// Lcd version of printf
void lcd_printf(char *format, ...) {
  unsigned char i;
  
  va_list argptr;
  char buffer[1024];
  
  va_start(argptr,format);
  vsprintf(buffer,format,argptr);
  va_end(argptr);
  
  for (i=0;i<strlen(buffer);i++) {
    lcd_putc(buffer[i],1);
  }
}
// Locate cursor on LCD
void lcd_locate(unsigned char row, unsigned char col) {


 // row (0-2)
// col (1-39)
  lcd_putc(0x80+row*0x40+col,0);
  udelay(35);
} 

void cursore_scegli_opz(unsigned char pos){
//0..3
	lcd_locate(0,0);
	lcd_printf(" ");			
	lcd_locate(0,20);
	lcd_printf(" ");			
	lcd_locate(1,0);
	lcd_printf(" ");			
	lcd_locate(1,20);
	lcd_printf(" ");
	if (pos==0)		lcd_locate(0,0);
	else if (pos==1)	lcd_locate(1,0);
	else if (pos==2)	lcd_locate(0,20);
	else if (pos==3)	lcd_locate(1,20);
	lcd_printf(">");
}
// Clear LCD
void lcd_clear() {
  lcd_putc(0x01,0);
  msDelay(2);
} 


void clean_row(unsigned char row){
//0..3
	if (row==0)		lcd_locate(0,0);
	else if (row==1)	lcd_locate(1,0);
	else if (row==2)	lcd_locate(0,20);
	else if (row==3)	lcd_locate(1,20);
	lcd_printf("                    ");
}
void y_pos(unsigned char x, unsigned char y){
// punto (0,0) in alto allo schermo a sx
// punto (-3,-19) in basso a dx

	if (y==0)	lcd_locate(0,x);//y,x
	else if (y==1)	lcd_locate(1,x);
	else if (y==2)	lcd_locate(0,20+x);
	else if (y==3)	lcd_locate(1,20+x);
}

void barra_menu_vert(unsigned char type){
	if (type==0){
		y_pos(19,0);
		lcd_printf("|");
		y_pos(19,1);
		lcd_printf("|");
		y_pos(19,2);
		lcd_printf("|");
		y_pos(19,3);
		lcd_printf("V");
	}
	else if (type==1){
		y_pos(19,0);
		lcd_printf("^");
		y_pos(19,1);
		lcd_printf("|");
		y_pos(19,2);
		lcd_printf("|");
		y_pos(19,3);
		lcd_printf("V");
	}
	else if (type==2){
		y_pos(19,0);
		lcd_printf("^");
		y_pos(19,1);
		lcd_printf("|");
		y_pos(19,2);
		lcd_printf("|");
		y_pos(19,3);
		lcd_printf("|");
	}
	else if (type==3){
		y_pos(19,0);
		lcd_printf("|");
		y_pos(19,1);
		lcd_printf("|");
		y_pos(19,2);
		lcd_printf("|");
		y_pos(19,3);
		lcd_printf("|");
	}
}

unsigned char aggiorna_cursore_opz(unsigned char min,unsigned char max){
// 0..3
// se trova 4 in max sa ke deve ritornare xkè verraà caricata un altra skermata del displayy
	unsigned char scelta,press;
	scelta=min; // 1 è il titolo del menu
	cursore_scegli_opz(scelta);
	while(p_status() != P_OK){
		press=p_status();
		if (press==P_DOWN)	{if (scelta<max){cursore_scegli_opz(++scelta);
						while (p_status()==P_DOWN) msDelay(10);}}
		else if (press==P_UP)  	{if (scelta>min){cursore_scegli_opz(--scelta);
						while (p_status()==P_UP)   msDelay(10);}}
		msDelay(50);



	if (scelta==4) break;

	}
	return scelta;
}

void sposta_2cursori_x(unsigned char x, unsigned char y){
//1..2 0..19
	y_pos(x,y-1);	
	lcd_printf("vv"); // gli spazi gli permettono di pulire il carattere precedente
	y_pos(x,y+1);
	lcd_printf("^^");
}

void pulisci_2cursori_x(unsigned char x, unsigned char y){
//1..2 0..19
	y_pos(x,y-1);	
	lcd_printf("  "); // gli spazi gli permettono di pulire il carattere precedente
	y_pos(x,y+1);
	lcd_printf("  ");
}





int select_cifra(unsigned char y, unsigned char sx, unsigned char dx){
	int press,scelta;
	scelta=sx;
	sposta_2cursori_x(scelta,y);
	while(p_status() != P_OK){
		press=p_status();
		if (press==P_RIGHT)	{if (scelta<dx){scelta++;sposta_2cursori_x(scelta,y);while (p_status()==P_RIGHT) msDelay(10);}}
		//if (press==P_LEFT) {if (scelta>sx){scelta--;sposta_2cursori_x(scelta,y);while (p_status()==P_LEFT)   msDelay(10);}}
		msDelay(50);
	}
	return scelta;
}

int inc_cifra(unsigned char x, unsigned char y, unsigned char attuale, unsigned char min, unsigned char max){
	unsigned char press,scelta;
	scelta=attuale;
	sposta_2cursori_x(x,y);
	while(p_status() != P_OK){
		press=p_status();
		if (press!=0){
			if (press==P_UP) if (scelta<max)  scelta++;
			if (press==P_DOWN) if (scelta>min) scelta--;
			y_pos(x,y);//bisogna sempre riportarlo li se no aggiunge caratteri uno dopo l'altro	
			lcd_printf("%02d",scelta);
			while (p_status()!=0) msDelay(10);		
		}
		msDelay(50);
	}
	y_pos(x,y);
	pulisci_2cursori_x(x,y);
	return scelta;
}



