//#Copyright (C) 2005, 2007 Py-acqua
//#http://www.pyacqua.net
//#
//#email: info@pyacqua.net
//#
//#
//#Py-Acqua is free software; you can redistribute it and/or modify
//#    it under the terms of the GNU General Public License as published by
//#    the Free Software Foundation; either version 2 of the License, or
//#    (at your option) any later version.
//#
//#Py-Acqua is distributed in the hope that it will be useful,
//#    but WITHOUT ANY WARRANTY; without even the implied warranty of
//#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//#    GNU General Public License for more details.
//#
//#    You should have received a copy of the GNU General Public License
//#    along with Py-Acqua; if not, write to the Free Software
//#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
//#
//#    Gestione del database

#include "sqlite.h"

#define SQLITE_OK           0   /* Successful result */
#define SQLITE_ERROR        1   /* SQL error or missing database */

void DATABASE_Control()//funzione che si occupa della connessione con il database  ed eseguire query
{


	FILE *outfile=NULL;
	const int QUERY_SIZE=300;
	char query[QUERY_SIZE];
	sqlite *db=NULL;
	char **errmsg=NULL;
	int resultquery;
	int nvarco;
	char a1;
	char b1;
	char ora[5];  //conterrà l'orario
	char day[9]; //conterrà il giorno


  //controllo data ------------------------------------------------------------------------------
	printf(" -- Avvio controllo numero nel database in corso... \n");

	
	struct tm *tp; 
	time_t curtime;

 	time(&curtime); 
	tp = localtime(&curtime); 
 
	strftime(ora, sizeof(ora), "%H%M",tp);
   	strftime(day, sizeof(day), "%Y%m%d",tp);

	printf(" -- Orario e data in tempo reale = %s %s\n",ora,day);
	
  //fine controllo ------------------------------------------------------------------------------
	
	char *filename = "/usr/local/foxacqua/database.sqlite";  //è il argv[1]
	printf(" -- Creo il Database se non esiste -- ");
	strcpy(a1,"\0");
	//char a[]="CREATE TABLE timer(id integer, ora TEXT, day DATE)";
	char *a = strdup("CREATE TABLE timer(id integer, ora TEXT, day DATE)");
	strcat (a1,a);
	
	printf(" -- invio query %s\n",a1);
	

/*	const char *fileout = "tmp.txt";  				    //è il argv[3]

	//open database
	db=sqlite_open(filename,0,errmsg);
	if (!db){
		fprintf(stderr, " -- Failed to open database %s. Error\n", filename);
		free(errmsg);
		//return -2;
	}

	//open file
	outfile=fopen(fileout, "w");
	if (!outfile){
		fprintf(stderr, " -- Failed to open input file %s\n",fileout);
		sqlite_close(db);
		//return -3;
	}

	//execute query
	
	snprintf(query, QUERY_SIZE, "%s", a1);
	resultquery=sqlite_exec(db, query, &write_result, (void *) &args,errmsg);
	if(resultquery){
		printf("fai qualcosa");
		
	}
	else
		printf(" XX ERROR : Query non eseguita\n");
	
	//controllo con gli altri cancelli--------------------------------

		snprintf(query, QUERY_SIZE, "%s", a1);
		resultquery=sqlite_exec(db, query, &write_result, (void *) &args,errmsg);
		if(!resultquery)
		{
			printf("fai altro");
		
		}
		else
			printf(" XX ERROR : Query non eseguita\n");	
	
*/			
	if (errmsg) 
	{
		printf(" -- Error\n");
		free (errmsg);
	}

	//close everything
	sqlite_close(db);
	fclose(outfile);
	printf(" -- Done\n");
	free(a1);
	free(b1);
}
