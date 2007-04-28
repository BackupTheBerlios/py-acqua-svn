//REGISTRI  X BANCO ZERO !
//x impostare direzione
// 1 = input
// 0 = output
#define	IODIRA	0X00
#define	IODIRB	0X01
	#define IO7	7
	#define IO6	6
	#define IO5	5
	#define IO4	4
	#define IO3	3
	#define IO2	2
	#define IO1	1
	#define IO0	0
// INVERTE LETTURA
// 1 = riflette il livello logico opposto a quello presente sul pin quando si legge GPIO
// 0 = lettura = stato del pin
#define	IPOLA	0X02 	
#define	IPOLB	0X03 	
	#define IP7	7
	#define IP6	6
	#define IP5	5
	#define IP4	4
	#define IP3	3
	#define IP2	2
	#define IP1	1
	#define IP0	0
// INTERRUPT AD OGNI CAMBIAMENTO
// 1 = abilitato
//	N.B.: bisogna configurare anche DEFVAL ed INTCON
// 0 = disabilitato
#define	GPINTENA	0X04
#define	GPINTENB	0X05
	#define GPINT7	7
	#define GPINT6	6
	#define GPINT5	5
	#define GPINT4	4
	#define GPINT3	3
	#define GPINT2	2
	#define GPINT1	1
	#define GPINT0	0
// LIVELLO LOGICO A CUI SI GENERE L'INTERRUPT
//   l'interrupt si genera quando sul pin c'è un livello 
//  opposto a quello impostato nel bit associato di questo registro.
#define	DEFVALA	0X06
#define	DEFVALB 0X07
	#define DEF7	7
	#define DEF6	6
	#define DEF5	5
	#define DEF4	4
	#define DEF3	3
	#define DEF2	2
	#define DEF1	1
	#define DEF0	0
//REGISTRO DI CONTROLLO DELL'INTERRUPT
// 1 = IL PIN È COMPARATO CON IL CORRISPONDENTE BIT IN DEFVAL
// 0 = IL PIN È COMPARATO CON LO STATO PRECEDENTE DELLO STESSO. (DEFVAL VIENE IGNORATO) 
#define	INTCONA	0X08
#define	INTCONB 0X09
	#define IOC7	7
	#define IOC6	6
	#define IOC5	5
	#define IOC4	4
	#define IOC3	3
	#define IOC2	2
	#define IOC1	1
	#define IOC0	0
//CONFIGURAZIONE DEI REGISTRI DELL' I/O EXPANDER
#define	IOCONA	0X0A
#define	IOCONB	0X0B

	#define BANK	7 	//SCELTA DEL BANCO DEI REGISTRI
						// 1 i regiastri assocciati ad ogni porta sono separati uin 2 banchi separati
						// 0 registri nello stesso banco (default)
						
	#define MIRROR	6	//SETTING DEI PIEDINI DI INTERRUPT
						// 1 INTA E INTB internamente connessi
						// 0 INTA è associato a porta e INTB a portb
		

	#define SREAD	5 	// LETTURA SEQUENZIALE
						// 1 = lettura sequenziale disabilitata, puntatore indirizzi non incrementato
						// 0 = lettura sequenziale abilitata, puntatore indirizzi incrementato

	#define DISSLW	4	//GESTISCE SLEW RATE DI SDA
						// 1 = disabilitato
						// 0 = abilitato
						
//	#define HAEN	3	//non presente in questo chip

	#define ODR		2	//CONFIGURA IL TIPO DI OUTPUT DEGLI 'INT' PIN
						// 1 = open drain
						// 0 = uscita del driver attiva

	#define INTPOL	1	// SETTA LA POLARITÀ DELL'OUTPUT PIN 'INT'
						// 1 = attivo a livello alto
						// 0 = attivo a livello basso
						
// Imposta le resistenze di pull-up sugli ingressi
// 1 = se il pin è configurato come input, viene applicata la resistenza di pullup
// 0 = nessun pullup
#define	GPPUA	0X0C
#define	GPPUB	0X0D
	#define PU7	7
	#define PU6	6
	#define PU5	5
	#define PU4	4
	#define PU3	3
	#define PU2	2
	#define PU1	1
	#define PU0	0
// Registro x abilitare gli interrupt
// 1 = interrupot abilitato
// 0 = interrupt disabilitato
#define	INTFA	0X0E
#define	INTFB	0X0F
	#define INT7	7
	#define INT6	6
	#define INT5	5
	#define INT4	4
	#define INT3	3
	#define INT2	2
	#define INT1	1
	#define INT0	0
// RIFLETTE I LIVELLI LOGICI DEI PIN IMPOSTATI COME INTERRUPT AL MOMENTO DEL CAMBIAMENTO DI STATO
// 1 = attivo alto
// 0 = attivo basso
#define	INTCAPA	0X10
#define	INTCAPB	0X11
	#define ICP7	7
	#define ICP6	6
	#define ICP5	5
	#define ICP4	4
	#define ICP3	3
	#define ICP2	2
	#define ICP1	1
	#define ICP0	0
// RIFLETTE IL LIVELLO LOGICO DEL PIN
// 1 = livello logico alto
// 0 = livelLo logico basso
#define	GPIOA	0X12
#define	GPIOB	0X13
	#define GP7	7
	#define GP6	6
	#define GP5	5
	#define GP4	4
	#define GP3	3
	#define GP2	2
	#define GP1	1
	#define GP0	0
// ACCEDE AL VALORE DEI LATCH DI USCITA
// 1 = livello logico alto
// 0 = livelLo logico basso
#define	OLATA	0X14  //LATCH
#define	OLATB	0X15  //LATCH
	#define OL7	7
	#define OL6	6
	#define OL5	5
	#define OL4	4
	#define OL3	3
	#define OL2	2
	#define OL1	1
	#define OL0	0
