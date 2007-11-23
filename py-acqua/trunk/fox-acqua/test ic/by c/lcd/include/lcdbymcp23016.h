//***************
//LCD PIN
//**************


#include "mcp23016.h"


#define lcdMcp_id	0x40	// 0100 000 0
//			  	    |   |  |_ r/w
//				    |   |____ id impostabile
//				    |________ id fisico


#define P_UP		1
#define P_DOWN		2
#define P_LEFT		3
#define P_RIGHT		4
#define P_OK		5



#define  lcd_port	0X00 //GP0
#define  lcd_E		3
#define  lcd_RS		2
#define  lcd_D4		4
#define  lcd_D5		5
#define  lcd_D6		6
#define  lcd_D7		7
