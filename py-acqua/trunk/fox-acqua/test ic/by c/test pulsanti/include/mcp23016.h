


//default:
//mcp23016GPIO0		0x00
//mcp23016GPIO1		0x00
//mcp23016OLAT0		0x00
//mcp23016OLAT1		0x00
//mcp23016IPOL0		0x00
//mcp23016IPOL1		0x00
//mcp23016IODIR0	0xff
//mcp23016IODIR1	0xff
//mcp23016INTCAP0 	casuale
//mcp23016INTCAP1	casuale
//mcp23016IOCON0	0
//mcp23016IOCON1	0

// RIFLETTE IL LIVELLO LOGICO DEL PIN
// 1 = livello logico alto
// 0 = livelLo logico basso
#define	mcp23016GPIO0	0X00
#define	mcp23016GPIO1	0X01
	#define mcp23016GP7	7
	#define mcp23016GP6	6
	#define mcp23016GP5	5
	#define mcp23016GP4	4
	#define mcp23016GP3	3
	#define mcp23016GP2	2
	#define mcp23016GP1	1
	#define mcp23016GP0	0



// ACCEDE AL VALORE DEI LATCH DI USCITA
// 1 = livello logico alto
// 0 = livelLo logico basso
#define	mcp23016OLAT0	0X02  //LATCH
#define	mcp23016OLAT1	0X03  //LATCH
	#define mcp23016OL7	7
	#define mcp23016OL6	6
	#define mcp23016OL5	5
	#define mcp23016OL4	4
	#define mcp23016OL3	3
	#define mcp23016OL2	2
	#define mcp23016OL1	1
	#define mcp23016OL0	0

// INVERTE LETTURA
// 1 = riflette il livello logico opposto a quello presente sul pin quando si legge GPIO
// 0 = lettura = stato del pin
#define	mcp23016IPOL0	0X04 	
#define	mcp23016IPOL1	0X05 	
	#define mcp23016IP7	7
	#define mcp23016IP6	6
	#define mcp23016IP5	5
	#define mcp23016IP4	4
	#define mcp23016IP3	3
	#define mcp23016IP2	2
	#define mcp23016IP1	1
	#define mcp23016IP0	0


//x impostare direzione
// 1 = input
// 0 = output
#define	mcp23016IODIR0	0X06
#define	mcp23016IODIR1	0X07
	#define mcp23016IODIRIO7	7
	#define mcp23016IODIRIO6	6
	#define mcp23016IODIRIO5	5
	#define mcp23016IODIRIO4	4
	#define mcp23016IODIRIO3	3
	#define mcp23016IODIRIO2	2
	#define mcp23016IODIRIO1	1
	#define mcp23016IODIRIO0	0



// RIFLETTE I LIVELLI LOGICI DEI PIN IMPOSTATI COME INTERRUPT AL MOMENTO DEL CAMBIAMENTO DI STATO
// 1 = attivo alto
// 0 = attivo basso
#define	mcp23016INTCAP0 0X08
#define	mcp23016INTCAP1	0X09
	#define mcp23016ICP7	7
	#define mcp23016ICP6	6
	#define mcp23016ICP5	5
	#define mcp23016ICP4	4
	#define mcp23016ICP3	3
	#define mcp23016ICP2	2
	#define mcp23016ICP1	1
	#define mcp23016ICP0	0


//CONFIGURAZIONE DEI REGISTRI DELL' I/O EXPANDER
#define	mcp23016IOCON0	0X0A
#define	mcp23016IOCON1	0X0B

	

	#define mcp23016INTPOL	1	// INTERRUPT ACTIITY RESOLUTION
						// 1 = 
						// 0 =
