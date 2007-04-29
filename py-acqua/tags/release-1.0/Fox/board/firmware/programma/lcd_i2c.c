#include "lcdbymcp23017.h"
//*********************************************************************
// LCD functions
//*********************************************************************

// RS line
void lcd_rs(int level) { mcp23017_pinWriteLevel(lcd_port,lcd_RS,level); }
//  E line
void lcd_e(int level) { mcp23017_pinWriteLevel(lcd_port,lcd_E,level);}
// D4..7
void lcdD4(int level) { mcp23017_pinWriteLevel(lcd_port,lcd_D4,level);}
void lcdD5(int level) { mcp23017_pinWriteLevel(lcd_port,lcd_D5,level);}
void lcdD6(int level) { mcp23017_pinWriteLevel(lcd_port,lcd_D6,level);}
void lcdD7(int level) { mcp23017_pinWriteLevel(lcd_port,lcd_D7,level);}
void lcd_e_strobe() {
	lcd_e(1);
	lcd_e(0);
}
// Send a nibble (4 bit) to LCD
void lcd_put_nibble( int value) {
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
void lcd_putc(unsigned char data, int mode) {
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
  int i;
  
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
void lcd_locate(int row, int col) {


 // row (0-2)
// col (1-39)
  lcd_putc(0x80+row*0x40+col,0);
  udelay(35);
} 

void cursore_sceqgli_opz(int pos){
//1..4
	lcd_locate(0,0);
	lcd_printf(" ");			
	lcd_locate(0,20);
	lcd_printf(" ");			
	lcd_locate(1,0);
	lcd_printf(" ");			
	lcd_locate(1,20);
	lcd_printf(" ");
	if (pos==1)		lcd_locate(0,0);
	else if (pos==2)	lcd_locate(1,0);
	else if (pos==3)	lcd_locate(0,20);
	else if (pos==4)	lcd_locate(1,20);
	lcd_printf(">");
}
// Clear LCD
void lcd_clear() {
  lcd_putc(0x01,0);
  msDelay(2);
} 
void clean_row(int row){
//1..4
	if (row==1)		lcd_locate(0,0);
	else if (row==2)	lcd_locate(1,0);
	else if (row==3)	lcd_locate(0,20);
	else if (row==4)	lcd_locate(1,20);
	lcd_printf("                    ");
}


int aggiorna_cursore_opz(int min,int max){
	int scelta,press;
	scelta=min+1; // 1 è il titolo del menu
	cursore_sceqgli_opz(scelta);
	while(p_status() != P_OK){
		press=p_status();
		if (press==P_DOWN)	{if (scelta<max){cursore_sceqgli_opz(++scelta);
						while (p_status()==P_DOWN) msDelay(10);}}
		else if (press==P_UP)  	{if (scelta>min){cursore_sceqgli_opz(--scelta);
						while (p_status()==P_UP)   msDelay(10);}}
		msDelay(50);
	}
	return scelta;
}
void y_pos(int x, int y){
	if (y==1)		lcd_locate(0,x);
	else if (y==2)	lcd_locate(1,x);
	else if (y==3)	lcd_locate(0,20+x);
	else if (y==4)	lcd_locate(1,20+x);
}

void sposta_2cursori_x(int x, int y){
	//clean_row(y-1);	
	//clean_row(y+1);
	y_pos(x,y-1);	
	lcd_printf(" v "); // gli spazi gli permettono di pulire il carattere precedente
	y_pos(x,y+1);
	lcd_printf(" ^ ");

}




void select_cifra(int y, int sx, int dx){
	int press,scelta;
	scelta=sx;
	sposta_2cursori_x(scelta,y);
	while(p_status() != P_OK){
		press=p_status();
		if (press==P_RIGHT)	{if (scelta<dx){scelta++;sposta_2cursori_x(scelta,y);while (p_status()==P_RIGHT) msDelay(10);}}
		if (press==P_LEFT) {if (scelta>sx){scelta--;sposta_2cursori_x(scelta,y);while (p_status()==P_LEFT)   msDelay(10);}}
		msDelay(50);
	}
}