/*
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 */

#include "fpkg.h"



int
update (void)
{

	//carica il reposity se necessario
	load_hive ();

	//per ogni applicazione nel reposity riempi struttura
	t_tab *remote_ver = malloc (sizeof (t_tab) * app_count);
	int ret;
	char *name;
	for (ret = 0; ret < app_count; ret++)
	{
		name = apps[ret].name;
		remote_ver[ret].name = strdup (strtok (name, "_"));
		remote_ver[ret].ver = strdup (strtok (NULL, "_"));
	}

	//per ogni applicazione installata riempi struttura da man 3 scandir
	struct dirent **namelist;
	int n;
	t_tab *local_ver;
	n = scandir ("/usr/local/var/fpkg/", &namelist, 0, alphasort);
	if (n < 0)
		perror ("scandir");
	else
	{
		local_ver = malloc (sizeof (t_tab) * n);
		while (n--)
		{
			local_ver[ret].name =
				strdup (strtok (namelist[n]->d_name, "_"));
			local_ver[ret].ver = strdup (strtok (NULL, "_"));
			free (namelist[n]);
		}
		free (namelist);
	}

	//Siamo pronti a verificare le strutture
	int ptr, inx;
	for (ptr = 0; ptr <= n; ptr++)
	{

		for (inx = 0; inx < app_count; inx++)
		{

			if (!strcmp
			    (local_ver[ptr].name, remote_ver[inx].name))
			{
				//ok i nomi sono uguali verifichiamo la versione                                
				if (strcmp
				    (local_ver[ptr].ver,
				     remote_ver[inx].ver) > 0)
				{
					upgrade (&local_ver[ptr],
						 &remote_ver[inx]);
				}
			}
		}
	}
	return 0;

}

int
upgrade (t_tab * loc, t_tab * rem)
{

	//rimuovi vecchia versione
	char old[255], new[255];
	if (verbose)
	{
		printf ("Preparing to update %s from version %s to %s\n",
			loc->name, loc->ver, rem->ver);
	}

	sprintf (old, "%s_%s", loc->name, loc->ver);
	remove_programm (old);

	sprintf (new, "%s_%s", rem->name, rem->ver);
	//odio questa interfaccia!!!!
	get_file_from_hive (hive_url[0], new, 0);
	return 0;
}
