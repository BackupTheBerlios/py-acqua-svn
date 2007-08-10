
#define RX_BUFFER_LEN 1024
#define TX_BUFFER_LEN 1024




//****************************************************
// Socket functions
//****************************************************



 int sd, new_sd;
   socklen_t addrlen;
   int bufsize = 1024;


   /*
    * struttura che contiene l'indirizzo ip del
    * server e la porta a cui il server si mette in ascolto
    * oltre che la famiglia di indirizzi usati
    *
    */

    struct sockaddr_in address;


   /*
    * struttura che conterra' l'indirizzo ip
    * e la porta del client (dopo la chiamata accept,
    * netstat -at dara' l'indirizzo del client e la porta
    * che risultera' essere 32775 o 32777 .....)
    * oltre che la famiglia di indirizzi usati
    *
    */

    struct sockaddr_in client_address;



int socket_init(){

   /*
    * creiamo il socket come in sock_client.c
    * arg1: AF_INET rappresenta il protocollo ARPA di internet
    *       (AF_INET = IPv4 internet protocol, IP e porta)
    * arg2: sock_stream fornisce una connessione affidabile, sequenziata,
    *       full duplex, dunque una connessione tcp
    * arg3: rappresenta il protocollo, il valore zero permette al sistema di
    *       scegliere quello piu' adatto
    *
    */


   if ((sd = socket(AF_INET,SOCK_STREAM,0)) > 0) printf("--Socket creato					[PASS]\n"); 


   /*
    * come per client ( vedere ip(7) )
    *
    */

   address.sin_family = AF_INET; // famiglia indirizzi ARPA di internet
   address.sin_addr.s_addr = INADDR_ANY; // qualsiasi indirizzo per il binding
   address.sin_port = htons(15000); // numero di porta ascolto server


   /*
    * Associamo un processo al socket locale che rimarra' in attesa
    * delle connessioni da parte di ogni client sulla porta 15000
    * arg1: il desrittore di socket sd creato in precedenza
    * arg2: la struttura address che contiene porta del server e indirizzo ip
    *       del server
    * arg3: dimensione della struttura address
    *
    */

   if ( bind(sd, (struct sockaddr *)&address, sizeof(address)) == 0 ) printf("--Processo per il socket creato			[PASS]\n"); 

presa_set_level(3,1);
msDelay(2000);
presa_set_level(3,0);
}






int sok() { 
 
//char *array[50];
 // int loop;
   char *buffertcp = (char*) malloc(bufsize);

int value;





   /*
    * mettiamo il processo server appena creato in attesa di eventuali
    * connessioni sul socket
    * arg1: desrittore di socket
    * arg2: grandezza massima della coda delle connessioni vale a dire
    *       numero max di connessioni che possono essere accodate per
    *       una eventuale accept successiva
    *
    */

   listen(sd, 3);


   /*
    * La accept (utilizzata solo con socket connessi come SOCK_STREAM che
    * abbiamo qui utilizzato), prende la prima connessione accodata, crea un
    * nuovosocket new_sd connesso con le stesse propriet�di sd ma con i
    * dati del client e collega i due socket. new_sd viene ritornato da
    * accept. Il server poi comunica con il client leggendo e scrivendo sul
    * socket new_sd .
    * arg1: sd e' il descrittore di socket generato dalla chiamata socket
    *       all' interno del client
    * arg2: l'indirizzo e' quello del server al quale il client deve
    *       connettersi
    *
    */

   // addrlen mi serve poi nella accept
   addrlen = sizeof(struct sockaddr_in);

   // client_address viene riempita con i dati del client
   new_sd = accept(sd, (struct sockaddr *)&client_address, &addrlen);

   if (new_sd > 0)  // non si sono verificati errori
     {
      printf("%s e' connesso ...\n", inet_ntoa(client_address.sin_addr));
      putchar(7); // bell
      }
   else
      return 1;
   while(1){

 	recv(new_sd, buffertcp, bufsize, 0);
      	printf("Messaggio ricevuto: %s\n", buffertcp);


	 
	     if  ( strstr (buffertcp,"PRESA(1,1)") != NULL )  presa_set_level(1,1);
	else if  ( strstr (buffertcp,"PRESA(1,0)") != NULL )  presa_set_level(1,0);
	else if  ( strstr (buffertcp,"PRESA(2,1)") != NULL )  presa_set_level(2,1);
	else if  ( strstr (buffertcp,"PRESA(2,0)") != NULL )   presa_set_level(2,0);
 	else if  ( strstr (buffertcp,"PRESA(3,1)") != NULL )   presa_set_level(3,1);		
	else if  ( strstr (buffertcp,"PRESA(3,0)") != NULL )   presa_set_level(3,0);	
 	else if  ( strstr (buffertcp,"PRESA(4,1)") != NULL ) presa_set_level(4,1);	
	else if  ( strstr (buffertcp,"PRESA(4,0)") != NULL ) presa_set_level(4,0);
 	else if  ( strstr (buffertcp,"PRESA(5,1)") != NULL ) presa_set_level(5,1);	
	else if  ( strstr (buffertcp,"PRESA(5,0)") != NULL ) presa_set_level(5,0);		
	else if  ( strstr (buffertcp,"PRESA(6,1)") != NULL )  presa_set_level(6,1);	
	else if  ( strstr (buffertcp,"PRESA(6,0)") != NULL ) presa_set_level(6,0);
 	else if  ( strstr (buffertcp,"PRESA(7,1)") != NULL )  presa_set_level(7,1);	
	else if  ( strstr (buffertcp,"PRESA(7,0)") != NULL ) presa_set_level(7,0);	
	else if  ( strstr (buffertcp,"PERISTALTICA(ON)") != NULL ) peristaltica_set_level(1);
	else if  ( strstr (buffertcp,"PERISTALTICA(OFF)") != NULL ) peristaltica_set_level(0);

else if  ( strstr (buffertcp,"PRESAGETLEVEL(1)") != NULL ){
		value=presa_read_level(1);
		if (value==1) 		send(new_sd, "PRESA1=ON", strlen("PRESA1=ON"), 0);
		else if (value==0)	send(new_sd, "PRESA1=OFF", strlen("PRESA1=OFF"), 0);}
	else if  ( strstr (buffertcp,"PRESAGETLEVEL(2)") != NULL ){
		value=presa_read_level(2);
		if (value==1) 		send(new_sd, "PRESA2=ON", strlen("PRESA2=ON"), 0);
		else if (value==0)	send(new_sd, "PRESA2=OFF", strlen("PRESA2=OFF"), 0);}
	else if  ( strstr (buffertcp,"PRESAGETLEVEL(3)") != NULL ){
		value=presa_read_level(3);
		if (value==1) 		send(new_sd, "PRESA3=ON", strlen("PRESA3=ON"), 0);
		else if (value==0)	send(new_sd, "PRESA3=OFF", strlen("PRESA3=OFF"), 0);}
	else if  ( strstr (buffertcp,"PRESAGETLEVEL(4)") != NULL ){
		value=presa_read_level(4);
		if (value==1) 		send(new_sd, "PRESA4=ON", strlen("PRESA4=ON"), 0);
		else if (value==0)	send(new_sd, "PRESA4=OFF", strlen("PRESA4=OFF"), 0);}
	else if  ( strstr (buffertcp,"PRESAGETLEVEL(5)") != NULL ){
		value=presa_read_level(5);
		if (value==1) 		send(new_sd, "PRESA5=ON", strlen("PRESA5=ON"), 0);
		else if (value==0)	send(new_sd, "PRESA5=OFF", strlen("PRESA5=OFF"), 0);}
	else if  ( strstr (buffertcp,"PRESAGETLEVEL(6)") != NULL ){
		value=presa_read_level(6);
		if (value==1) 		send(new_sd, "PRESA6=ON", strlen("PRESA6=ON"), 0);
		else if (value==0)	send(new_sd, "PRESA6=OFF", strlen("PRESA6=OFF"), 0);}
	else if  ( strstr (buffertcp,"PRESAGETLEVEL(7)") != NULL ){
		value=presa_read_level(7);
		if (value==1) 		send(new_sd, "PRESA7=ON", strlen("PRESA7=ON"), 0);
		else if (value==0)	send(new_sd, "PRESA7=OFF", strlen("PRESA7=OFF"), 0);}
	




	else if  ( strstr (buffertcp,"PERISTALTICAGETLEVEL()") != NULL ){
		value=peristaltica_read_level();
		if (value==1) 		send(new_sd, "PERISTALTICA=ON", strlen("PERISTALTICA=ON"), 0);
		else if (value==0)	send(new_sd, "PERISTALTICA=OFF", strlen("PERISTALTICA=OFF"), 0);}
	else if  ( strstr (buffertcp,"PERISTALTICAGETLEVEL()") != NULL ){
		value=peristaltica_read_level();
		if (value==1) 		send(new_sd, "PERISTALTICA=ON", strlen("PERISTALTICA=ON"), 0);
		else if (value==0)	send(new_sd, "PERISTALTICA=OFF", strlen("PERISTALTICA=OFF"), 0);}
	else if  ( strstr (buffertcp,"GALL1GETLEVEL()") != NULL ){
		value=galleggiante_read_level(1);
		if (value==1) 		send(new_sd, "GALL1=OK", strlen("GALL1=OK"), 0);
		else if (value==0)	send(new_sd, "GALL1=BAD", strlen("GALL1=BAD"), 0);}
	else if  ( strstr (buffertcp,"GALL2GETLEVEL()") != NULL ){
		value=galleggiante_read_level(2);
		if (value==1) 		send(new_sd, "GALL2=OK", strlen("GALL2=OK"), 0);
		else if (value==0)	send(new_sd, "GALL2=BAD", strlen("GALL2=BAD"), 0);}

	else if  ( strstr (buffertcp,"REBOOT") != NULL ) 	system ("reboot");
	



}


}




