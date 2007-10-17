/*  
      install.c

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

void install_programm(char *hiveurl, char *target, int i){
	struct stat sbuf;
	char app_url[1024];
	char target_path[1024];
	char tmp_file_name[1024];
	char cmd_buffer[1024];
	char pipe_tee[255], option[255];

	memset (option,0,255);
	memset (pipe_tee,0,255);

	//eventuali subcartelle sono presenti nel file fpk
	if(target){
		strcpy(target_path, target);
	} else {
		strcpy(target_path, apps[i].target);
	}
	
	switch (apps[i].filetype) {
		case 1: 	//programma dipendente da libreria
			sprintf(app_url, "%s%s/%s.fpk", hiveurl, lib_path, apps[i].name); 
			break;
		case 2: 	//file generico
			sprintf(app_url, "%smisc/%s.fpk", hiveurl, apps[i].name); 
			break;
		default: 	//fimage o fpga code
			sprintf(app_url, "%smisc/%s", hiveurl, apps[i].name); 
	}
	
	sprintf(tmp_file_name, "/var/tmp/%s.fpk", apps[i].name);

	if(apps[i].filetype != 4) {
		//scarica files se nn è un fimage
		get_file(app_url, tmp_file_name);	
	}
	
	//se non è fpga code o fimage
	if(apps[i].filetype < 3 ) {
		// check if the file has the correct size
		if (stat(tmp_file_name, &sbuf) == 0 ){
		        if(apps[i].size != sbuf.st_size){
				printf("The file has the wrong size !!!!\n");
				unlink(tmp_file_name);
				exit(-1);
			} else {
				if (verbose) 
					printf("The file you just downloaded has the correct size\n");
			}
		} else {
			printf("Cannot get size of file that was downloaded\n");
			exit(-2);
		}	

		//rimuovi script di post-installazione se esiste
		int post_run=0;
		int fd=open("/var/tmp/post.sh",O_EXCL|O_CREAT);
		if (fd == -1) {
			unlink ("/var/tmp/post.sh");	
			post_run=1;
		}
		close (fd);
		
		//log
		int log_inst = system("mkdir -p /usr/local/var/fpkg/");		//crea directory se nn esiste...
		if (log_inst == -1 ) { 
			printf("Cannot create installation log.\n");
		} else {
			strcpy(pipe_tee, "/usr/local/var/fpkg/");		
			strcat(pipe_tee, apps[i].name);
		
		
			//salva la directory di installazione nel log
#if DEBUG 
			printf("pipe_tee: %s\n", pipe_tee);
#endif 

			fd=open(pipe_tee, O_WRONLY|O_CREAT|O_TRUNC);
			if (fd) {
				write (fd, target_path, strlen(target_path));
				sprintf(option,"\n");
				write (fd, option, 1);
			}
			close (fd);
		
		}

		//Estrai file in  target_path
		if(verbose) 
			strcpy(option, "| tee -a");
		else 
			strcpy(option, ">>");
		
		if (log_inst == -1)
			sprintf(cmd_buffer, "tar -C %s -vxzf %s %s %s", target_path, tmp_file_name, option, pipe_tee);
		else
			sprintf(cmd_buffer, "tar -C %s -vxzf %s", target_path, tmp_file_name);
			
#if DEBUG
		printf("cmd_buffer: %s\n",cmd_buffer);
#endif
		system(cmd_buffer);		
		
		unlink(tmp_file_name);

		// se post-installazione 
		if(post_run){
			fd=open("/var/tmp/post.sh",O_EXCL|O_CREAT);
		
			if (fd == -1) {
				//il file esiste (ora) ed era nel pacchetto
				printf("Now running post installation script...\n");
				system("/var/tmp/post.sh");
			}
			//rimuovi file di post configurazione
			unlink ("/var/tmp/post.sh");
		}
	}
	
	if(apps[i].filetype == 3){
		fpga_code = i;
	}
	
	if(apps[i].filetype == 4){
		fimage_file = i;
	}
}

int download_dep(char *hiveurl, char *dep_list, char *target){
	//scarica e install dipendenze, le dipendenze sono separate da ";" 
	//restituisce il numero di dipendenze  scaricate

	static char *tok,a;
	for(tok = strtok(dep_list, ";"), a=0; tok != NULL;  tok = strtok(NULL, ";"), a++) {
		//printf ("%s\n",tok);
		get_file_from_hive(hiveurl, tok, target);		
	}
	return a;
}	




