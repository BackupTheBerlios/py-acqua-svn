#include "mcp23017_reg.h"
#include "foxacqua_pulsantiera_by_mcp23017.h"

//*********************
//  MCP23017 ROUTINES
//*********************
unsigned char mcp23017_regLeggi(unsigned char id, int reg){

	unsigned char data;
	i2c_start();
	i2c_outbyte(id<<1); // accoda uno zero x dire scrivi
	i2c_outbyte(reg);
	i2c_start();
	i2c_outbyte((id<<1)+1); // accoda un uno  x dire leggi 
	data=i2c_inbyte(0);
	i2c_stop();
	return data;
}
void mcp23017_regScrivi(unsigned char id, unsigned char registro,unsigned char value){
	i2c_start();
	i2c_outbyte(id<<1);
	i2c_outbyte(registro);
	i2c_outbyte(value);
	i2c_stop();
}
void mcp23017_pinWriteLevel(unsigned char id, unsigned char gp,unsigned char pin,unsigned char level){
	unsigned char value;
	
		
	value=mcp23017_regLeggi(id,GPIOA);

	if (level==1) value=value | (1 << pin ); // = 2^pin
	else if (level==0) value=value & ( 0xff -(1 << pin ));
	else printf("ERRORE LIVELLO ERATO: %d", level);
	
	mcp23017_regScrivi(id,GPIOA,value);
	
}


