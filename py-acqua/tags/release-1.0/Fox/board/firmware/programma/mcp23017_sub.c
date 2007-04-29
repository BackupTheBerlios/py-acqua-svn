#include "mcp23017_reg.h"
#include "pulsantiera_by_mcp23017.h"
#define lcdMcp23017_id	0x27
//*********************
//  MCP23017 ROUTINES
//*********************
int mcp23017_regLeggi(int reg){

	int data;
	i2c_start();
	i2c_outbyte(lcdMcp23017_id<<1); // accoda uno zero x dire scrivi
	i2c_outbyte(reg);
	i2c_start();
	i2c_outbyte((lcdMcp23017_id<<1)+1); // accoda un uno  x dire leggi 
	data=i2c_inbyte(0);
	i2c_stop();
	return data;
}
void mcp23017_regScrivi(int registro,int value){
	i2c_start();
	i2c_outbyte(lcdMcp23017_id<<1);
	i2c_outbyte(registro);
	i2c_outbyte(value);
	i2c_stop();
}
void mcp23017_pinWriteLevel(int gp,int pin,int level){
	int value;
	
///	printf("porta= %d\n",GPIOA);	
//	printf("pin= %d livello= %d\n",pin,level);
		
		
	value=mcp23017_regLeggi(GPIOA);
//	printf("letto= %d\n",value);
	
	if (level==1) value=value | (1 << pin ); // = 2^pin
	else if (level==0) value=value & ( 0xff -(1 << pin ));
	else printf("ERRORE LIVELLO ERATO: %d", level);
	

//	printf("scritto= %d\n",value);
	mcp23017_regScrivi(GPIOA,value);
	
///	value=mcp23017_regLeggi(GPIOA);
	//printf("verifica= %d\n",value);
}

void lcdMcpInit(){
//init input x 5 pulsanti
//init output x fili al display

	
	//imposta mcp
	mcp23017_regScrivi(IODIRA,0);//DISPLAY, TT OUT
	mcp23017_regScrivi(IODIRB,0xff);//pulsanti, tt in
	mcp23017_regScrivi(GPIOA,0);//uscite sul display a zero
	mcp23017_regScrivi(GPPUB,0);// pullup DISATTIVATI sui pulsanti
}

int p_status(){
	int value;
	value=mcp23017_regLeggi(GPIOB);
	if (value==8) return (P_OK);
	else if (value==1)return (P_UP);
	else if (value==16)return (P_DOWN);
	else if (value==2)return (P_RIGHT);
	else if (value==4)return (P_LEFT);
}
