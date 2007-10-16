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

FILE *timer_fd=NULL;

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
		return -1;
	}

	fseek (timer_fd, num * RECORD, SEEK_SET);

	char buffer[RECORD];

	fread (buffer, RECORD, 1, timer_fd);

	memcpy (&(ret->num), &buffer[0], sizeof (char));
	memcpy (&(ret->pin), &buffer[sizeof (char)], sizeof (char));
	memcpy (&(ret->ora), &buffer[2 * sizeof (char)], sizeof (int));
	memcpy (&(ret->stato), &buffer[2 * sizeof (char) + sizeof (int)],
		sizeof (char));

	return 0;
}

int
read_timers (s_timer ** ret)
{
	//Legge il timers N_SONDE*N_TIMER  *ret[N_SONDE*N_TIMER]


	perror ("non implementata");


	return 1;

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
		return -1;
	}

	fseek (timer_fd, ret->num * RECORD, SEEK_SET);

	char buffer[RECORD];


	memcpy (&buffer[0], &(ret->num), sizeof (char));
	memcpy (&buffer[sizeof (char)], &(ret->pin), sizeof (char));
	memcpy (&buffer[2 * sizeof (char)], &(ret->ora), sizeof (int));
	memcpy (&buffer[2 * sizeof (char) + sizeof (int)], &(ret->stato),
		sizeof (char));

	fwrite (buffer, RECORD, 1, timer_fd);

	return 0;
}


int
set_timers (s_timer ** ret)
{
	//salva i timer 

	perror ("non implementata");

	return 1;
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
		return -1;
	}
	fseek (timer_fd, num * RECORD, SEEK_SET);
	fwrite (NULL, RECORD, 1, timer_fd);

	return 1;

}

static int
timer_file (int status)
{
	//apre (status =1); chiude (status =0) il file dei timer

	switch (status)
	{
	case 1:
		timer_fd = fopen (TIMER_FILE, "rw+");
		if (timer_fd == NULL)
		{
			perror ("Impossibile aprire file timer ");
			return -1;
		}

		//portati all'ultimo byte
		if (!fseek
		    (timer_fd, N_TIMER * N_SONDE * RECORD - 1, SEEK_SET))
		{
			//il file nn esisteva o è stato dannegiato
			if (!fwrite(NULL, N_TIMER * N_SONDE, RECORD, timer_fd))
			{
				perror ("Impossibile ripristinare file timer ");
				return -1;
			}
		}
		break;
	case 2:
		fclose (timer_fd);
		break;

	}
	
	return 0;
}
