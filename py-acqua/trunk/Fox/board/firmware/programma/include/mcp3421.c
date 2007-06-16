// a/d converter su i2c 
#define mcp_ad1 0x68


int valo[3];
//*********************
//  MCP23017 ROUTINES
//*********************
void ad_regLeggi(int id){

 i2c_stop();
	i2c_start();
	i2c_outbyte(id<<1+1); 


	valo[0]=i2c_inbyte(1);//manda anke l'ack se si mette l' tra parentesi
	valo[1]=i2c_inbyte(1);
valo[2]=0x32;
	i2c_stop();
}
void ad_init(int id){
 i2c_stop();
	i2c_start();
	i2c_outbyte(id<<1); 
	i2c_outbyte(0x00); 
	i2c_outbyte(0x10); 
	i2c_stop();
}
