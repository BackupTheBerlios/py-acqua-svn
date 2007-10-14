 

//REGISTRI
//x impostare direzione
// 1 = input
// 0 = output
#define	mcp23008IODIR	0X00	
	#define mcp23008IO7	7
	#define mcp23008IO6	6
	#define mcp23008IO5	5
	#define mcp23008IO4	4
	#define mcp23008IO3	3
	#define mcp23008IO2	2
	#define mcp23008IO1	1
	#define mcp23008IO0	0
// INVERTE LETTURA
// 1 = riflette il livello logico opposto a quello presente sul pin quando si legge GPIO
// 0 = lettura = stato del pin
#define	mcp23008IPOL	0X01 	
	#define mcp23008IP7	7
	#define mcp23008IP6	6
	#define mcp23008IP5	5
	#define mcp23008IP4	4
	#define mcp23008IP3	3
	#define mcp23008IP2	2
	#define mcp23008IP1	1
	#define mcp23008IP0	0
// INTERRUPT AD OGNI CAMBIAMENTO
// 1 = abilitato
//	N.B.: bisogna configurare anche DEFVAL ed INTCON
// 0 = disabilitato
#define	mcp23008GPINTEN	0X02
	#define mcp23008GPINT7	7
	#define mcp23008GPINT6	6
	#define mcp23008GPINT5	5
	#define mcp23008GPINT4	4
	#define mcp23008GPINT3	3
	#define mcp23008GPINT2	2
	#define mcp23008GPINT1	1
	#define mcp23008GPINT0	0
// LIVELLO LOGICO A CUI SI GENERE L'INTERRUPT
//   l'interrupt si genera quando sul pin c'è un livello 
//  opposto a quello impostato nel bit associato di questo registro.
#define	mcp23008DEFVAL	0X03
	#define mcp23008DEF7	7
	#define mcp23008DEF6	6
	#define mcp23008DEF5	5
	#define mcp23008DEF4	4
	#define mcp23008DEF3	3
	#define mcp23008DEF2	2
	#define mcp23008DEF1	1
	#define mcp23008DEF0	0
//REGISTRO DI CONTROLLO DELL'INTERRUPT
// 1 = IL PIN È COMPARATO CON IL CORRISPONDENTE BIT IN DEFVAL
// 0 = IL PIN È COMPARATO CON LO STATO PRECEDENTE DELLO STESSO. (DEFVAL VIENE IGNORATO) 
#define	mcp23008INTCON	0X04
	#define mcp23008IOC7	7
	#define mcp23008IOC6	6
	#define mcp23008IOC5	5
	#define mcp23008IOC4	4
	#define mcp23008IOC3	3
	#define mcp23008IOC2	2
	#define mcp23008IOC1	1
	#define mcp23008IOC0	0
//CONFIGURAZIONE DEI REGISTRI DELL' I/O EXPANDER
#define	mcp23008IOCON	0X05
	//7,6,3,0 NON PRESENTI
// LETTURA SEQUENZIALE
// 1 = lettura sequenziale disabilitata, puntatore indirizzi non incrementato
// 0 = lettura sequenziale abilitata, puntatore indirizzi incrementato
	#define mcp23008SREAD	5
//GESTISCE SLEW RATE DI SDA
// 1 = disabilitato
// 0 = abilitato
	#define mcp23008DISSLW	4
//CONFIGURA IL TIPO DI OUTPUT DEGLI 'INT' PIN
// 1 = open drain
// 0 = uscita del driver attiva
	#define mcp23008ODR	2
// SETTA LA POLARITÀ DELL'OUTPUT PIN 'INT'
// 1 = attivo a livello alto
// 0 = attivo a livello basso
	#define INTPOL	1
// Imposta le resistenze di pull-up sugli ingressi
// 1 = se il pin è configurato come input, viene applicata la resistenza di pullup
// 0 = nessun pullup
#define	mcp23008GPPU	0X06
	#define mcp23008PU7	7
	#define mcp23008PU6	6
	#define mcp23008PU5	5
	#define mcp23008PU4	4
	#define mcp23008PU3	3
	#define mcp23008PU2	2
	#define mcp23008PU1	1
	#define mcp23008PU0	0
// Registro x abilitare gli interrupt
// 1 = interrupot abilitato
// 0 = interrupt disabilitato
#define	mcp23008INTF	0X07
	#define mcp23008INT7	7
	#define mcp23008INT6	6
	#define mcp23008INT5	5
	#define mcp23008INT4	4
	#define mcp23008INT3	3
	#define mcp23008INT2	2
	#define mcp23008INT1	1
	#define mcp23008INT0	0
// RIFLETTE I LIVELLI LOGICI DEI PIN IMPOSTATI COME INTERRUPT AL MOMENTO DEL CAMBIAMENTO DI STATO
// 1 = attivo alto
// 0 = attivo basso
#define	mcp23008INTCAP	0X08
	#define mcp23008ICP7	7
	#define mcp23008ICP6	6
	#define mcp23008ICP5	5
	#define mcp23008ICP4	4
	#define mcp23008ICP3	3
	#define mcp23008ICP2	2
	#define mcp23008ICP1	1
	#define mcp23008ICP0	0
// RIFLETTE IL LIVELLO LOGICO DEL PIN
// 1 = livello logico alto
// 0 = livelLo logico basso
#define	mcp23008GPIO	0X09
	#define mcp23008GP7	7
	#define mcp23008GP6	6
	#define mcp23008GP5	5
	#define mcp23008GP4	4
	#define mcp23008GP3	3
	#define mcp23008GP2	2
	#define mcp23008GP1	1
	#define mcp23008GP0	0
// ACCEDE AL VALORE DEI LATCH DI USCITA
// 1 = livello logico alto
// 0 = livelLo logico basso
#define	mcp23008OLAT	0X0A  //LATCH
	#define mcp23008OL7	7
	#define mcp23008OL6	6
	#define mcp23008OL5	5
	#define mcp23008OL4	4
	#define mcp23008OL3	3
	#define mcp23008OL2	2
	#define mcp23008OL1	1
	#define mcp23008OL0	0
