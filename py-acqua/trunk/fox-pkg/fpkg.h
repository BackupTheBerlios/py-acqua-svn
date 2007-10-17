#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>


typedef struct _APP {
	char name[128];
	int size;
	char description[1024];
	char dep[1024];
	char target[128];
	char type;
	char filetype;
	char lib_avail;
} APP;

typedef struct s_tab {
		char *name;
		char *ver;
} t_tab;
 

#define VERSION "2.1.2"

#define MAX_APP 128
#define GLIBC 	1
#define UCLIBC 	2
#define MAX_HIVE 16

#define DEBUG 0

#define FLG_NONE 0
#define FLG_LST 1
#define FLG_RMV 2
#define FLG_GET 4
#define FLG_TRG 8
#define FLG_DSC 16
#define FLG_UPG 32
#define FLG_FLH 64
#define FLG_VRB 128


#define CHK_FLG(v, f) ((v & f) == f)

//prototipi
long get_file( char *,  char *);
void load_hive(void);
void list_hive_files(void);
void install_programm(char *,  char *,  int);
void remove_programm(char *);
int download_dep(char *,char *, char *);
void get_file_from_hive(char *, char *, char *);
void load_config(char *);
void flash_fpga(void);
void flash_fimage(void);
void print_usage(void);
int update(void);
int upgrade (t_tab *loc, t_tab *rem);

extern char app_count;
extern APP apps[MAX_APP];
extern char hive_url[MAX_HIVE][256];
extern char hive_count;
extern char lib_path[32];
extern char lib_type;
extern int fpga_code;
extern int fimage_file;
extern int verbose;
extern int remove_app;
