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

#include "foxacqua_time.h"

int timer_fd=0;

int
read_timer (s_timer * ret, int num)
{
	//Legge il timer num e salva dati nella struttura *ret

	if (ret == NULL || num < 0 || num > N_TIMER * N_SONDE)
	{
		//struttura ret nn allocata o num fuori dai limiti
		return -2;
	}

	if (!timer_file (1))
	{
		perror ("Uscita da errore precedente");
		return 0;
	}

	lseek (timer_fd, num * RECORD, SEEK_SET);

	char buffer[RECORD];

	read (timer_fd, buffer, RECORD);

	memcpy (&(ret->num), &buffer[0], sizeof (char));
	memcpy (&(ret->pin), &buffer[sizeof (char)], sizeof (char));
	memcpy (&(ret->ora), &buffer[2 * sizeof (char)], sizeof (int));
	memcpy (&(ret->stato), &buffer[2 * sizeof (char) + sizeof (int)],
		sizeof (char));

	return 1;
}

int
read_timers (s_timer ** ret)
{
	//Legge il timers N_SONDE*N_TIMER  *ret[N_SONDE*N_TIMER]


	perror ("non implementata");


	return 0;

}

int
set_timer (s_timer * ret)
{
	//salva la struttura dati ret su file

	if (ret == NULL)
	{
		//struttura ret nn allocata
		return -2;
	}
	if (!timer_file (1))
	{
		perror ("Uscita da errore precedente");
		return 0;
	}

	lseek (timer_fd, ret->num * RECORD, SEEK_SET);

	char buffer[RECORD];


	memcpy (&buffer[0], &(ret->num), sizeof (char));
	memcpy (&buffer[sizeof (char)], &(ret->pin), sizeof (char));
	memcpy (&buffer[2 * sizeof (char)], &(ret->ora), sizeof (int));
	memcpy (&buffer[2 * sizeof (char) + sizeof (int)], &(ret->stato),
		sizeof (char));

	write (timer_fd, &buffer[0], RECORD);

	return 1;
}


int
set_timers (s_timer ** ret)
{
	//salva i timer 

	perror ("non implementata");

	return 0;
}

int
del_timer (int num)
{
	if (num < 0 || num > N_TIMER * N_SONDE)
	{
		//num fuori dai limiti
		return -2;
	}
	if (!timer_file (1))
	{
		perror ("Uscita da errore precedente ");
		return 0;
	}
	lseek (timer_fd, num * RECORD, SEEK_SET);
	char a[RECORD]={0};
	write (timer_fd, &a, RECORD);

	return 1;

}

int
timer_file (int status)
{
	//apre (status =1); chiude (status =0) il file dei timer

	switch (status)
	{
	case 1:
		if (timer_fd == 0) {
			timer_fd = open (TIMER_FILE, O_CREAT | O_RDWR );
			if (timer_fd == -1)
			{
				perror ("Impossibile aprire file timer ");
				return 0;
			}

			//portati all'ultimo byte
			if (lseek (timer_fd, N_TIMER * N_SONDE * RECORD - 1, SEEK_SET)==-1)
			{
				//il file nn esisteva o è stato dannegiato
				char a[N_TIMER * N_SONDE*RECORD]={0};
				if (write(timer_fd, &a, N_TIMER * N_SONDE*RECORD)==-1)
				{
					perror ("Impossibile ripristinare file timer ");
					return 0;
				}
			}	
		}
		break;
	case 2:
		close (timer_fd);
		break;

	}
	
	return 1;
}
