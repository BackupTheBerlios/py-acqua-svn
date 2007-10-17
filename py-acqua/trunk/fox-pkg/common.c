/*  
    common.c

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

//funzione principale
void get_file_from_hive(char *hiveurl, char *appname, char *target){
	int i;
	for(i = 0; i < app_count; i++){
		if(!strcmp(appname, apps[i].name)){
			//ho trovato il file richiesto
			if(apps[i].type <3 ){
				//scarica dipendenze
				if (strlen(apps[i].dep) != 0 && !remove_app) {
					int dep_n = download_dep(hiveurl,apps[i].dep , target);
					if (verbose) 
						printf("Downloaded %d dependences\n",dep_n);
				}	
			//install
			install_programm(hiveurl, target, i);	
			} 
			return;
		}
	}
	printf("App is not available in the hive!\n");
}

// download a file
long get_file(char *from, char *to){
	char cmd[512];
	printf("Downloading %s...\n", from);
	if(verbose) {
		sprintf(cmd, "wget %s -O %s", from, to);
	} else {
		sprintf(cmd, "wget -q %s -O %s", from, to);
	}
	
	return system(cmd);
}

//Stampa la lista di pacchetti compatibile con il sistema in uso
void list_hive_files(void){
	int i,a,max=0,len;
	//trova max lunghezza nome
	for(i = 0; i < app_count; i++) {
		len =strlen(apps[i].name);
		if (len > max) max = len;		//lunghezza massima nome
	}
	max++;
	
	for(i = 0; i < app_count; i++) {
		if((apps[i].type != 3) && ((apps[i].lib_avail == 0) || (apps[i].lib_avail == lib_type))){
			len = strlen(apps[i].name);
			printf("%s", apps[i].name);
			for (a=0; a< max-len; a++)  printf(" ");	//riempi di spazi
			printf("- %s\n", apps[i].description);	
		}
	}
}

void load_config(char *filename){
	char buffer[256];
	FILE *fp;
	if(filename){
		fp = fopen(filename, "r");
	} else {
		fp = fopen("/usr/local/etc/fpkg.conf", "r");
		if(!fp) {
			fp = fopen("/etc/fpkg.conf", "r");
		}
		if(!fp) {
			fp = fopen("fpkg.conf", "r");
		}
	}
	if(!fp){
		printf("Error opening config file !!\n");
		exit(0);
	}
	
	do{
		if(fgets(buffer, 256, fp)){
			if(strlen(buffer) > 5){
				if(hive_count < MAX_HIVE){
					if(buffer[strlen(buffer)-1] == '\n'){
						buffer[strlen(buffer)-1] = '\0';
					}
					// what type of entry is this ?
					char *sep = strstr(buffer, ":");
					if(sep){
						*sep = '\0';
						sep++;
						if(strcmp(buffer, "hive")==0){
							if (verbose) 
								printf("Found hive : %s in config file\n", sep);
							strcpy(hive_url[hive_count], sep);
							hive_count++;
							
						
						} else if(strcmp(buffer, "lib")==0){
							printf("Using lib : %s \n", sep);
							strcpy(lib_path, sep);
							if(strcmp(lib_path, "glibc") == 0){
								lib_type = GLIBC;
							} else 	if(strcmp(lib_path, "uclibc") == 0){
								lib_type = UCLIBC;
							} else {
								printf("Unknown lib type !!\n");
								exit(-3);
							}								
						}						
					}
				}
			}
		}	
	} while(!feof(fp));	
	
	fclose(fp);

}

void flash_fpga(void){
	char fpga_buffer[1024];
	sprintf(fpga_buffer, "fpga_flash -aprogram -f%s%s", apps[fpga_code].target, apps[fpga_code].name);
	system(fpga_buffer);

}

void flash_fimage(void){
	 char buffer[1024];
         sprintf(buffer, "/usr/bin/wget %smisc/%s -q -O - | /bin/flash -t flash_all -m FTP", hive_url[0], apps[fimage_file].name);
         printf("Doing a fimage upgrade : %s \n", buffer);
	 system(buffer);
}
