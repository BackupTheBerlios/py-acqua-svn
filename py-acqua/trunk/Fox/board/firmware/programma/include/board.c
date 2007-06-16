//*****************
//	MAIN
//*****************


#define bordMcp23008_id	0x21

void board_init(){
	mcp230xx_regScrivi(preseMcp23008_id,mcp23008IOCON,0x24); //slew rate su sda, interrupt disablitati, no pull up 
	mcp230xx_regScrivi(preseMcp23008_id,mcp23008IPOL,0x00);//lettura non complementata
	mcp230xx_regScrivi(preseMcp23008_id,mcp23008GPINTEN,0x00);//nessun interrupt
	mcp230xx_regScrivi(preseMcp23008_id,mcp23008IODIR,0x00);//tutti out
	mcp230xx_regScrivi(preseMcp23008_id,reg_prese,0x70);//tutti spenti

}