//*****************
//	MAIN
//*****************


#define boardMcp23008_id	0x21
#define io_buzzer		0 	// out
#define io_peristaltica		1	// out
#define io_nc1			2	// in
#define io_nc2			3	// in
#define io_galleg1		4	// in
#define io_galleg2		5	// in
#define io_nc3			6	// in
#define io_ldac			7	// out
#define	reg_io		0X09 // = GPIO

void board_init(){
	mcp230xx_regScrivi(boardMcp23008_id,mcp23008IOCON,0x24); 	//slew rate sda, interrupt disablitati, no pull-up ecc
	mcp230xx_regScrivi(boardMcp23008_id,mcp23008IPOL,0x00);		//lettura non complementata
	mcp230xx_regScrivi(boardMcp23008_id,mcp23008GPINTEN,0x00);	//nessun interrupt
	mcp230xx_regScrivi(boardMcp23008_id,mcp23008IODIR,0x7c);	//I/O
	mcp230xx_regScrivi(boardMcp23008_id,reg_prese,0x00);		//tutti spenti

}
//peristaltica
void peristaltica_set_level(unsigned char level){
// level 0..1
	mcp230xx_pinWriteLevel(boardMcp23008_id,reg_io,io_peristaltica,level);
}
unsigned char peristaltica_read_level(){
	return mcp230xx_pinReadLevel(boardMcp23008_id, reg_io,io_peristaltica);
}



//buzzer
void buzzer_set_level(unsigned char level){
// level 0..1
	mcp230xx_pinWriteLevel(boardMcp23008_id,reg_io,io_buzzer,level);
}
unsigned char galleggiante_read_level(unsigned char galleggiante){
// galleggiante 1..2
	if (galleggiante==1) return mcp230xx_pinReadLevel(boardMcp23008_id, reg_io,io_galleg1);
	else if (galleggiante==2) return mcp230xx_pinReadLevel(boardMcp23008_id, reg_io,io_galleg2);
}
