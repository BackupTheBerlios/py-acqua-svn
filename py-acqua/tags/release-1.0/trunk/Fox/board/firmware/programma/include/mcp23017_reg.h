//REGISTRI  X BANCO ZERO !
//x impostare direzione
// 1 = input
// 0 = output
#define	mcp23017IODIRA	0X00
#define	mcp23017IODIRB	0X01
	#define mcp23017IODIRAIO7	7
	#define mcp23017IODIRAIO6	6
	#define mcp23017IODIRAIO5	5
	#define mcp23017IODIRAIO4	4
	#define mcp23017IODIRAIO3	3
	#define mcp23017IODIRAIO2	2
	#define mcp23017IODIRAIO1	1
	#define mcp23017IODIRAIO0	0
// INVERTE LETTURA
// 1 = riflette il livello logico opposto a quello presente sul pin quando si legge GPIO
// 0 = lettura = stato del pin
#define	mcp23017IPOLA	0X02 	
#define	mcp23017IPOLB	0X03 	
	#define mcp23017IP7	7
	#define mcp23017IP6	6
	#define mcp23017IP5	5
	#define mcp23017IP4	4
	#define mcp23017IP3	3
	#define mcp23017IP2	2
	#define mcp23017IP1	1
	#define mcp23017IP0	0
// INTERRUPT AD OGNI CAMBIAMENTO
// 1 = abilitato
//	N.B.: bisogna configurare anche DEFVAL ed INTCON
// 0 = disabilitato
#define	mcp23017GPINTENA	0X04
#define	mcp23017GPINTENB	0X05
	#define mcp23017GPINT7	7
	#define mcp23017GPINT6	6
	#define mcp23017GPINT5	5
	#define mcp23017GPINT4	4
	#define mcp23017GPINT3	3
	#define mcp23017GPINT2	2
	#define mcp23017IPINT1	1
	#define mcp23017IPINT0	0
// LIVELLO LOGICO A CUI SI GENERE L'INTERRUPT
//   l'interrupt si genera quando sul pin c'è un livello 
//  opposto a quello impostato nel bit associato di questo registro.
#define	mcp23017DEFVALA	0X06
#define	mcp23017DEFVALB 0X07
	#define mcp23017DEF7	7
	#define mcp23017DEF6	6
	#define mcp23017DEF5	5
	#define mcp23017DEF4	4
	#define mcp23017DEF3	3
	#define mcp23017DEF2	2
	#define mcp23017DEF1	1
	#define mcp23017DEF0	0
//REGISTRO DI CONTROLLO DELL'INTERRUPT
// 1 = IL PIN È COMPARATO CON IL CORRISPONDENTE BIT IN DEFVAL
// 0 = IL PIN È COMPARATO CON LO STATO PRECEDENTE DELLO STESSO. (DEFVAL VIENE IGNORATO) 
#define	mcp23017INTCONA	0X08
#define	mcp23017INTCONB 0X09
	#define mcp23017IOC7	7
	#define mcp23017IOC6	6
	#define mcp23017IOC5	5
	#define mcp23017IOC4	4
	#define mcp23017IOC3	3
	#define mcp23017IOC2	2
	#define mcp23017IOC1	1
	#define mcp23017IOC0	0
//CONFIGURAZIONE DEI REGISTRI DELL' I/O EXPANDER
#define	mcp23017IOCONA	0X0A
#define	mcp23017IOCONB	0X0B

	#define mcp23017BANK	7 	//SCELTA DEL BANCO DEI REGISTRI
						// 1 i regiastri assocciati ad ogni porta sono separati uin 2 banchi separati
						// 0 registri nello stesso banco (default)
						
	#define mcp23017MIRROR	6	//SETTING DEI PIEDINI DI INTERRUPT
						// 1 INTA E INTB internamente connessi
						// 0 INTA è associato a porta e INTB a portb
		

	#define mcp23017SREAD	5 	// LETTURA SEQUENZIALE
						// 1 = lettura sequenziale disabilitata, puntatore indirizzi non incrementato
						// 0 = lettura sequenziale abilitata, puntatore indirizzi incrementato

	#define mcp23017DISSLW	4	//GESTISCE SLEW RATE DI SDA
						// 1 = disabilitato
						// 0 = abilitato
						
//	#define mcp23017HAEN	3	//non presente in questo chip

	#define mcp23017ODR		2	//CONFIGURA IL TIPO DI OUTPUT DEGLI 'INT' PIN
						// 1 = open drain
						// 0 = uscita del driver attiva

	#define mcp23017INTPOL	1	// SETTA LA POLARITÀ DELL'OUTPUT PIN 'INT'
						// 1 = attivo a livello alto
						// 0 = attivo a livello basso
						
// Imposta le resistenze di pull-up sugli ingressi
// 1 = se il pin è configurato come input, viene applicata la resistenza di pullup
// 0 = nessun pullup
#define	mcp23017GPPUA	0X0C
#define	mcp23017GPPUB	0X0D
	#define mcp23017PU7	7
	#define mcp23017PU6	6
	#define mcp23017PU5	5
	#define mcp23017PU4	4
	#define mcp23017PU3	3
	#define mcp23017PU2	2
	#define mcp23017PU1	1
	#define mcp23017PU0	0
// Registro x abilitare gli interrupt
// 1 = interrupot abilitato
// 0 = interrupt disabilitato
#define	mcp23017INTFA	0X0E
#define	mcp23017INTFB	0X0F
	#define mcp23017INT7	7
	#define mcp23017INT6	6
	#define mcp23017INT5	5
	#define mcp23017INT4	4
	#define mcp23017INT3	3
	#define mcp23017INT2	2
	#define mcp23017INT1	1
	#define mcp23017INT0	0
// RIFLETTE I LIVELLI LOGICI DEI PIN IMPOSTATI COME INTERRUPT AL MOMENTO DEL CAMBIAMENTO DI STATO
// 1 = attivo alto
// 0 = attivo basso
#define	mcp23017INTCAPA	0X10
#define	mcp23017INTCAPB	0X11
	#define mcp23017ICP7	7
	#define mcp23017ICP6	6
	#define mcp23017ICP5	5
	#define mcp23017ICP4	4
	#define mcp23017ICP3	3
	#define mcp23017ICP2	2
	#define mcp23017ICP1	1
	#define mcp23017ICP0	0
// RIFLETTE IL LIVELLO LOGICO DEL PIN
// 1 = livello logico alto
// 0 = livelLo logico basso
#define	mcp23017GPIOA	0X12
#define	mcp23017GPIOB	0X13
	#define mcp23017GP7	7
	#define mcp23017GP6	6
	#define mcp23017GP5	5
	#define mcp23017GP4	4
	#define mcp23017GP3	3
	#define mcp23017GP2	2
	#define mcp23017GP1	1
	#define mcp23017GP0	0
// ACCEDE AL VALORE DEI LATCH DI USCITA
// 1 = livello logico alto
// 0 = livelLo logico basso
#define	mcp23017OLATA	0X14  //LATCH
#define	mcp23017OLATB	0X15  //LATCH
	#define mcp23017OL7	7
	#define mcp23017OL6	6
	#define mcp23017OL5	5
	#define mcp23017OL4	4
	#define mcp23017OL3	3
	#define mcp23017OL2	2
	#define mcp23017OL1	1
	#define mcp23017OL0	0
