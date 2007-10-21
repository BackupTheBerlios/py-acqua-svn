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
//#    Gestione timer tramite file
#ifndef FOXACQUA_TIME_H
#define FOXACQUA_TIME_H

#include <sys/types.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <stdio.h> 
#include <errno.h> 

#define TIMER_FILE "/usr/local/var/fox-acqua/fox_timer.lst"

#define N_SONDE 7
#define N_TIMER 10

#define RECORD (sizeof(char)+sizeof(char)+sizeof(int)+sizeof(char))


typedef struct {
	char num;		//numero del timer, un numero tra 0 e N_SONDE * N_TIMER
	char pin;
	int ora;
	char stato;
} s_timer ;

//extern int timer_fd;

//Legge l'n-essimo time e salva i valori nella struttura passata per puntatore
int read_timer(s_timer *, int );
//Legge tutti i time e salva i valori nell'array di trutture passati per puntatore
int read_timers(s_timer **);
//Salva l'n-essimo time su file
int set_timer(s_timer *);
//Salva tutti i time su file
int set_timers(s_timer **);
//Resetta il timer n-essimo
int del_timer(int);
int timer_file(int );

#endif
