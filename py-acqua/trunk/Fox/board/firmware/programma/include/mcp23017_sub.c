#include "mcp23017_reg.h"
#include "foxacqua_pulsantiera_by_mcp23017.h"

//*********************
//  MCP23017 ROUTINES
//*********************
int mcp23017_regLeggi(int id, int reg){

	int data;
	i2c_start();
	i2c_outbyte(id<<1); // accoda uno zero x dire scrivi
	i2c_outbyte(reg);
	i2c_start();
	i2c_outbyte((id<<1)+1); // accoda un uno  x dire leggi 
	data=i2c_inbyte(0);
	i2c_stop();
	return data;
}
void mcp23017_regScrivi(int id, int registro,int value){
	i2c_start();
	i2c_outbyte(id<<1);
	i2c_outbyte(registro);
	i2c_outbyte(value);
	i2c_stop();
}
void mcp23017_pinWriteLevel(int id, int gp,int pin,int level){
	int value;
	
		
	value=mcp23017_regLeggi(id,GPIOA);

	if (level==1) value=value | (1 << pin ); // = 2^pin
	else if (level==0) value=value & ( 0xff -(1 << pin ));
	else printf("ERRORE LIVELLO ERATO: %d", level);
	
	mcp23017_regScrivi(id,GPIOA,value);
	
}


