char prese_nomi[8][15]; // 8 nomi da 15 caratterri 
#define preseMcp23008_id	0x20
#define presa1			0
#define presa2			1
#define presa3			2
#define presa4			3
#define presa5			4
#define presa6			5
#define presa7			6
#define	reg_prese		0X09 // = GPIO

void ciabatta_init(){
	mcp230xx_regScrivi(preseMcp23008_id,mcp23008IODIR,0);
}
void presa_set_level(int presa,int level){
	mcp230xx_pinWriteLevel(preseMcp23008_id,reg_prese,--presa,level);
}

