/*  
  fpkg
    Package Management for FoxBoard 
    and FOXVHDL Board 
  
    Ver 1.0 originaly writed by:
    Author: John Crispin
    Copyright (C) 2006 Phrozen (http://www.phrozen.biz)

    Maintainer: Claudio Mignanti <claudyus@users.sourceforge.net>
    Copyright (C) 2007  (http://claudyus.altervista.org http://www.pyacqua.net)
  

  This is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.
    
  This programm is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
    
  To have a copy of the GNU General Public License write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

#include "fpkg.h"



char app_count = 0;
APP apps[MAX_APP];
char hive_url[MAX_HIVE][256];
char hive_count = 0;
char lib_path[32];
char lib_type;
int fpga_code = 0;
int fimage_file = 0;
int verbose = 0;
int remove_app = 0;

int main(int argc, char **argv) {
	int flag = 0;
	char desc_app[128];
	char get_app[128];
	char target_path[128];
	int i,c;
	char buffer[1024];

	if (argc== 0) {
		print_usage();
		exit(-1);
	}
	
	load_config(0);
	
	while ((c = getopt(argc, argv, ":hufvc:t:")) != -1) {
        switch(c) {
	        case 'v':
				flag |= FLG_VRB; break;
			case 'f':
				flag |= FLG_FLH; break;
			case 'c':
				printf("Using configfile : %s\n", optarg);
				load_config(optarg);
				break;
			case 't':
				flag |= FLG_TRG;
				strcpy(target_path, optarg);
				printf("Using target : %s\n", optarg);
				break;
			case 'u':
				flag |= FLG_UPG; break;
			case 'h':
				print_usage();
				exit(2);
		}
	}
	
	for(i = 1; i < argc; i++){

		if (!strcmp(argv[i], "update")) {
			update();
			
		}
		if (!strcmp(argv[i], "remove")) {
			flag |= FLG_RMV;
			i++;
			strcpy(get_app, argv[i]);
			continue;
		}
		if (!strcmp(argv[i], "install")) {
			flag |= FLG_GET;
			i++;
			strcpy(get_app, argv[i]);
			continue;
			
		}		
		if (!strcmp(argv[i], "list")) {
			// read in the hive info
			load_hive();
			list_hive_files();
		}
		if (!strcmp(argv[i], "show")) {
			system("ls -1 /usr/local/var/fpkg/");
			continue;		
		}
		if (!strcmp(argv[i], "info")) {
			flag |= FLG_DSC;
			i++;
			strcpy(desc_app, argv[i]);
			continue;
		}
		if (!strcmp(argv[i], "--help") || !strcmp(argv[i], "help")) {
			print_usage();
			exit(2);
			
		}
		

	}



	//visualizza la descrizione completa per l'applicazione
	if (CHK_FLG(flag,FLG_DSC)) {
		sprintf(buffer, "%s%s.dsc", hive_url[0], desc_app);
		int ret = get_file(buffer, "/var/tmp/desc");
		if (ret == 256) 
			printf("Cannot find description file for this application.");
		else
			//if (system("less /var/tmp/desc") == -1)
				system("cat /var/tmp/desc");
	}
	
	// are we supposed to get a file ?
	if(CHK_FLG(flag,FLG_GET)){
		load_hive();
		
		if(CHK_FLG(flag,FLG_FLH) && (fpga_code >= 0)){
			system("/usr/bin/fbctl -d");
			flash_fpga();
			system("/usr/bin/foxbone r 1");
			system("/usr/bin/fbctl -e");
		}
		if(CHK_FLG(flag,FLG_UPG) && (fimage_file >= 0)){
			flash_fimage();
			printf("System going down\n");
			system("/sbin/reboot");
			
		}
		//esegui parsing della lista e passa a get file 
		char *ptr=NULL, *app_name;
		for (app_name = strtok_r(get_app, ",", &ptr); app_name != NULL; app_name = strtok_r(NULL, ",", &ptr)) {
			get_file_from_hive(hive_url[0], app_name, (CHK_FLG(flag,FLG_TRG))?(target_path):(0));
		}
	}
	
	if (CHK_FLG(flag,FLG_RMV)) {
		//esegui parsing della lista e passa a get file 
		char **ptr=NULL, *app_name;
		for (app_name = strtok_r(get_app, ",", ptr); app_name != NULL; app_name = strtok_r(NULL, ",", ptr)) {
			remove_programm(app_name);
		}
	}
	return 0;
} 

int hive_loaded = 0;
// load the info inside Packages
void load_hive(void){
	
	//evita caricamenti multipli di enviroment
	if (hive_loaded) return;
	hive_loaded=1;
	
	// check if at least one hive was found
	if(hive_count == 0){
		printf("No hive was found !\n");
		return;
	}
	
	FILE *fp;
	char *file_list="/var/tmp/Packages";
	
	char buffer[1024];	
	
	// downlod the hive file
	sprintf(buffer, "%s%s", hive_url[0], "Packages");
	get_file(buffer, file_list);
	
	fp = fopen(file_list, "r");
	if(!fp){
		printf("Unable to load Packages\n");
		exit(0);
	}

	do {
		if(fgets(buffer, 1024, fp)){
			if(strlen(buffer) > 5){
				if(*buffer != '#'){
					if(buffer[strlen(buffer)-1] == '\n'){
						buffer[strlen(buffer)-1] = '\0';
					} else 
						buffer[strlen(buffer)] = '\0';
					
					char *tok, *tmp,a;
					for(tok = strtok(buffer, "|"), a=0; tok != NULL;
								tok = strtok(NULL, "|"), a++) {
#if DEBUG
						printf("%s\n", tok);
#endif
						switch (a) {
							case 0: tmp= apps[app_count].name;	
								strcpy(tmp, tok);
								break;
							case 1: apps[app_count].size=atoi(tok);	
								break;
							case 2: tmp= apps[app_count].description; 
								strcpy(tmp, tok);
								break;
							case 3: tmp= apps[app_count].dep;
								strcpy(tmp, tok);
								break;
							case 4: tmp= apps[app_count].target;
								strcpy(tmp, tok);
								break;
							case 5: apps[app_count].type=atoi(tok);
								break;
							case 6: apps[app_count].filetype=atoi(tok);
								break;
							case 7: apps[app_count].lib_avail=atoi(tok);
								break;
						}					
					}
					app_count++;
				}
			}	
		}
	} while(!feof(fp));
	
	fclose(fp);
	unlink(file_list);
}



void print_usage(void){
	printf("Usage : fpkg [options] <command>\n"
	"Version : %s\n"
    " Where options is one of the following:\n"
    "        -c configfile   - /etc/fpkg.conf is default\n"
    "        -v              - Be verbose\n"
    "        -f              - Flash file int fpga\n"
    "        -h              - This help\n"
    "        -t FOLDER       - Download into a non default folder\n"
    "        -u              - Flash FOX with a fimage (DANGEROUS!)\n"
	" Command is a least one of the following:"
	"        install APPLIST      - Get and install APPNAME\n"
	"        remove APPLIST       - Remove APPNAME\n"
	"	     info APPNAME	      - Show full description, code source and mainteiner\n"
	"        update 			  - Update installed packages\n"
	" 		 show 				  - Show installed application\n"
	"        list                 - List avaible apps and short description\n"
	" Where:\n"
	"        APPNAME          - Is a packages name\n"
	"		 APPLIST          - Is a list of APPNAME separated by ','\n", VERSION);
}
