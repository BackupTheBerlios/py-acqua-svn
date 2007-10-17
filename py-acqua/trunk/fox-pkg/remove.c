/*  
    remove.c

    Package Management for FoxBoard 
    and FOXVHDL Board 
  
    This file is part of fpkg.

    Fpkg is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    Fpkg is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

*/

#include "fpkg.h"


//
//	il file di log presenta in prima riga la directory di installazione e nelle
//	righe successive il log di tar -v 
//	Per rimuovere completamente tutti i file installati si dovrà quindi per prima cosa
//	recuperare la directory di installazione e poi a partire dalla fine del file risalire 
//	fino alla prima riga. Questo permette di eliminare anche le directory che vengono a svuotarsi
//	create in fase di installazione!!!	
void remove_programm(char *name){
	char log_name[255],
	file_n[1024], *buffer, *target_path= NULL ;
	
	int len=0, f_len, act,str_len;
	
	memset (log_name,0,255);


	//log
	strcpy(log_name, "/usr/local/var/fpkg/");
	strcat(log_name, name);
#if DEBUG
	printf("log_name: %s\n",log_name);
#endif

	FILE *fp=fopen(log_name, "r");

	if (fp == NULL) {
		printf("Error: application not installed!\n");
		return;
	}

	int fd = fileno(fp);

	
	//directory di installazione
	getline (&target_path, &len , fp);
	target_path[len-1]='\0';

#if DEBUG
	printf("target_path: %s\n",target_path);
#endif

	struct stat tmp;
	fstat(fd, &tmp);

	//FIXME 
	return;
	do {
		if(fgets(buffer, 1024, fp)){
			//replace \n or eof
			if(buffer[strlen(buffer)-1] == '\n'){
				buffer[strlen(buffer)-1] = '\0';
			} else {
				buffer[strlen(buffer)] = '\0';		
			}

			sprintf(file_n ,"%s%s", target_path, buffer);
			if (verbose) printf ("Removing %s...\n", file_n);
			if ( unlink (file_n) == -1 && errno == EISDIR)		//è una directory
				if( rmdir(file_n) == -1 && errno == ENOTEMPTY )
					printf ("%s is not empty dir. Skip!\n", file_n);
		}
	} while(!feof(fp));

	unlink(log_name);
	fclose (fp); 		//close & delete log file

}
