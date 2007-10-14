//*****************
//	MAIN
//*****************


#define boardMcp23016_id	0x21
#define io_buzzer		0 	// out
#define io_peristaltica		1	// out

#define io_nc1			0	// in
#define io_nc2			1	// in
#define io_galleg1		2	// in
#define io_galleg2		3	// in
#define io_nc3			4	// in

inline void board_init(){
	//mcp230xx_regScrivi(boardMcp23016_id,mcp23016IPOL,0x00);		//lettura non complementata
	//mcp230xx_regScrivi(boardMcp23016_id,mcp23016GPINTEN,0x00);	//nessun interrupt
	mcp230xx_regScrivi(boardMcp23016_id,mcp23016IODIR0,0x00);	//I/O
	mcp230xx_regScrivi(boardMcp23016_id,mcp23016IODIR1,0xf);	//I/O
	mcp230xx_regScrivi(boardMcp23016_id,mcp23016GPIO0,0x00);
}
//peristaltica
inline void peristaltica_set_level(unsigned char level){
// level 0..1
	mcp230xx_pinWriteLevel(boardMcp23016_id,mcp23016IODIR0,io_peristaltica,level);
}

inline unsigned char peristaltica_read_level(){
unsigned char value;
	value=mcp230xx_pinReadLevel(boardMcp23016_id, mcp23016IODIR0,io_peristaltica);
if (value==1)
	return 1;
else 
	return 0;

}



//buzzer
inline void buzzer_set_level(unsigned char level){
// level 0..1
	mcp230xx_pinWriteLevel(boardMcp23016_id,mcp23016IODIR0,io_buzzer,level);
}
inline unsigned char galleggiante_read_level(unsigned char galleggiante){
// galleggiante 1..2
	if (galleggiante==1) return mcp230xx_pinReadLevel(boardMcp23016_id, mcp23016IODIR1,io_galleg1);
	else if (galleggiante==2) return mcp230xx_pinReadLevel(boardMcp23016_id, mcp23016IODIR1,io_galleg2);
}
