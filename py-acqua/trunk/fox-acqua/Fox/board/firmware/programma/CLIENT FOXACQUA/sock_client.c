/* sock_client.c 

#
# Copyright (C) 2003 Marco Pagnanini
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
#

*/

// header file per i socket
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <netinet/in.h>

// altri header
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
   int sd;                      	        // descrittore di socket
   int bufsize = 1024; 			            // dimensione buffer stdin
   char *buffer = (char*) malloc(bufsize);	// buffer per stdin
   struct sockaddr_in address;		        // indirizzo e porta del server


   if (argc < 2) {
     printf("Uso del Client : Client indirizzo_IP (del server da contattare)\n");
     exit(0);
   }
   

   if ((sd = socket(AF_INET, SOCK_STREAM, 0)) > 0)
     printf("Socket creato !\n"); // socket creato senza errori

   // protocollo ARPA di Internet
   address.sin_family = AF_INET;
   // numero porta del server (man htons) inserita in address
   address.sin_port = htons(15000);
   // IP server inserito in address

   inet_pton(AF_INET, argv[1], &address.sin_addr);

   /*
    * con la connect il client si collega al server, la comunicazione
    * viene effettivamente stabilita.
    * arg1: descrittore di socket locale
    * arg2: indirizzo del server a cui connettersi
    * arg3: dimensione struttura indirizzo server
    *
    */

   if (connect(sd, (struct sockaddr *)&address, sizeof(address)) == 0)
     {
     printf("Connessione accettata con il Server: %s ...\n",inet_ntoa(address.sin_addr));
     printf("(quit per uscire)\n");


   /*
    * ricezione e invio messaggi per mezzo del socket
    * arg1: descrittore di socket
    * arg2: buffer dove porre o da cui prelevare il messaggio
    * arg3: dimensione buffer
    * arg4: (flag)
    *
    */

      while(1)
      {
      //  recv(sd, buffer, bufsize, 0);

      //  printf("Messaggio ricevuto: %s\n", buffer);
        printf("Messaggio da inviare: ");

        fgets(buffer, bufsize, stdin);
	if( ! strcmp(buffer, "quit\n") )
        {
	    printf("\n\nUscita\n\n\a");
	    return 0;
	}

    /*
     *	trasmette il messaggio scrivendo sullo stesso socket,
     *	stessi argomenti di recv
     *
     */
     
        send(sd, buffer, bufsize, 0);
      } //while
   } //if
   close(sd);	  	// viene chiuso il socket

   return 0;
}
