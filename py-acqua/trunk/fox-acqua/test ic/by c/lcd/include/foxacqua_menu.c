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

/***************
//	SCHERMATE
//
//	MENU
//
***************
//0,0	riga1
//0,20  riga2
//1,0   riga3
//1,20  riga4*/



//#inline
inline void
sk_clear ()
{
	lcd_clear ();
}

inline void
sk_init ()
{
	y_pos (7, 0);

	lcd_printf ("VISITA");
	y_pos (2, 1);
	delay_ms (1000);
	lcd_printf ("www.pyacqua.net");
	y_pos (0, 3);
	delay_ms (1000);
	lcd_printf ("--------------------");

	delay_ms (3000);
	sk_clear ();

}





inline void
sk_menu_1_3_1 ()
{
	unsigned char sonda;
	y_pos (1, 0);

	lcd_printf ("<<  ASSEGNA NOMI");
	sonda = scegli_sonda ();
	while (p_status () == P_OK) ;
	assegna_nome (3, 2, sonda);	//x,y
}

inline void
sk_menu_1_3_2 ()
{

	unsigned char sonda;

	y_pos (1, 0);
	lcd_printf ("<<  LEGGI VALORI");
	sonda = scegli_sonda ();
	sk_clear ();
	//ad_regLeggi(mcp_ad1);
	//printf("valor %d\n",valo[0]);

	//printf("valor %d\n",valo[1]);

}

inline void
sk_menu_1_2_1 ()
{
	unsigned char presa;
	y_pos (1, 0);
	lcd_printf ("<<  ASSEGNA NOMI");
	presa = scegli_presa ();
	assegna_nome (3, 2, presa);	//x,y
}

inline void
sk_menu_1_2_2 ()
{
	unsigned char scelta, stato;
	y_pos (1, 0);
	lcd_printf ("<<  CAMBIA STATO");
	scelta = scegli_presa ();

	stato = imposta_stato (scelta);	//1..7
	presa_set_level (scelta, stato);
}




void
sk_menu_1_2_3_1 ()
{				//IMPOSTA TIMER

	time_t now;
	struct tm *tm_now;
	char conv[3];
	char buff[10];

	int presa, stato, timer, i, hr = 0, min = 0;
	int fp;
	presa = scegli_presa ();	//1..7
	presa--;		//0..6
	sk_clear ();
	//controla se x questa presa ci sn timer liberi
	timer = 99;		// se dopo il ciclo for timer non vale 0, significa ke nn c'� nessun timer libero
	for (i = 0; i < 10; i++)
		if (presa_timer_stato[presa][i] == 99)
		{		//CONTROLLA SE � LIBERO
			timer = i;	//trovato!
			goto SKIP;
		}
      SKIP:
	if (timer != 99)
	{
		y_pos (1, 0);
		lcd_printf ("<< IMPOSTA TIMER %d", timer);	//,numero del timer


		now = time (NULL);
		tm_now = localtime (&now);

		strftime (conv, sizeof conv, "%H", tm_now);
		hr = atoi (conv);
		strftime (conv, sizeof conv, "%M", tm_now);
		min = atoi (conv);


		y_pos (2, 2);
		lcd_printf ("%d:%d", hr, min);
		hr = inc_cifra (2, 2, hr, 0, 24);	//va ad incrementarla
		min = inc_cifra (5, 2, min, 0, 59);
		//chiede lo stato a cui la presa dovr� portarsi
		stato = imposta_stato (presa + 1);	//1..7


		// salvo i timer in un file
		s_timer a;
		a.num=presa*timer;
		a.pin=presa;
		a.ora=hr*100+min;
		a.stato=stato;

		set_timer(&a);


		presa_timer[presa][timer][0] = hr;	// 8 prese x 10 eventi l'una x [0]ora e [1]min
		presa_timer[presa][timer][1] = min;	// 8 prese x 10 eventi l'una x [0]ora e [1]min
		presa_timer_stato[presa][i] = stato;
		sk_clear ();

		y_pos (5, 1);
		lcd_printf ("Presa ,%d,", presa + 1);
		y_pos (2, 2);
		lcd_printf ("Timer %d salvato", timer);

		delay_ms (2000);

	}
	else
	{			// nessun timer ibero
		y_pos (2, 2);
		lcd_printf ("Timer occupati");
		delay_ms (2000);
	}
}



void
mod_timer (int presa, int timer)
{				// e se uno lo vuole eliminare???
//presa arriva nel range 0..6
//timer arriva nel range 0..9

	unsigned char stato, hr, min;
	y_pos (1, 0);
	lcd_printf ("<< MODIFICA TIMER %d", timer);

	y_pos (2, 2);
	hr = presa_timer[presa][timer][0];
	min = presa_timer[presa][timer][1];


//mostra i dati di questo timer da modificare
	lcd_printf ("%d:%d", hr, min);
	hr = inc_cifra (2, 2, hr, 0, 24);	//va ad incrementarla
	min = inc_cifra (5, 2, min, 0, 59);


//chiede il nuovo stato
	stato = imposta_stato (presa + 1);	//1..7




	presa_timer[presa][timer][0] = hr;	// 8 prese x 10 eventi l'una x [0]ora e [1]min
	presa_timer[presa][timer][1] = min;	// 8 prese x 10 eventi l'una x [0]ora e [1]min
	presa_timer_stato[presa][timer] = stato;
	sk_clear ();
	y_pos (2, 2);
	lcd_printf ("Modifica salvata");
	delay_ms (2000);
}

inline void
sk_menu_1_2_3_2 ()
{
	int presa, i, j, num, scelta;
	y_pos (1, 0);
	lcd_printf ("<< GESTIONE TIMER ");	//,numero del timer
	presa = scegli_presa ();	//1..7
	presa--;		//0..6
	num = 0;
	for (j = 0; j < 3; j++)
	{
//RIMOSTRA:
		//mostra 3 timer x volta
		sk_clear ();
		y_pos (1, 0);
		lcd_printf ("<< GESTIONE TIMER ");	//,numero del timer

		for (i = 0; i < 3; i++)
		{
			y_pos (1, i + 1);
			lcd_printf ("%d: ", num);

			if (presa_timer_stato[presa][num] < 99)
			{
				lcd_printf ("%d:%d => %d ",
					    presa_timer[presa][num][0],
					    presa_timer[presa][num][1],
					    presa_timer_stato[presa][num]);
			}
			else
				lcd_printf ("--:-- => -");
			num++;
		}
		//disegna barra
		if (j == 0)
			barra_menu_vert (0);	//j==limite inf
		else if (j == 2)
			barra_menu_vert (2);	//j==limite sup
		else
			barra_menu_vert (1);	//casi centrali


		scelta = aggiorna_cursore_opz (0, 4);
		sk_clear ();
		//   if (scelta==0) => mostra i sucessivi
		if (scelta >= 1)
		{
			if (scelta < 4)
			{

				if (j == 0)
					mod_timer (presa, scelta - 1);	// MODIFICA QUESTO TIMER
				// scelta va da 1 a 3,
				// il timer dv andare da 0 a 2
				else if (j == 1)
					mod_timer (presa, scelta + 2);
				else if (j == 2)
					mod_timer (presa, scelta + 5);
				//  goto RIMOSTRA; non funziona
			}
		}

		//   if (scelta==4) avanza e mostra altri 3 timer
	}

//SKIP:
	delay_us (1);

}


inline void
sk_menu_1_2_3_3 ()
{
	unsigned char presa, i;
	y_pos (1, 0);
	lcd_printf ("<< ELIMINA TIMER ");	//,numero del timer
	presa = scegli_presa ();	//1..7
	presa--;
	sk_clear ();
	y_pos (1, 0);
	lcd_printf ("<< ELIMINA TIMER ");	//,numero del timer

	for (i = 0; i < 10; i++)
	{
		presa_timer[presa][i][0] = 0;
		presa_timer[presa][i][1] = 0;
		presa_timer_stato[presa][i] = 99;
	}
	y_pos (1, 2);
	lcd_printf ("TIMER DELLA PRESA %d", presa);
	y_pos (5, 3);
	lcd_printf ("ELIMINATI");

}




inline void
sk_menu_1_2_3 ()
{
	unsigned char scelta;
	y_pos (1, 0);
	lcd_printf ("<<    TIMER");

	y_pos (1, 1);
	lcd_printf ("Imposta timer");

	y_pos (1, 2);
	lcd_printf ("Mostra timer");

	y_pos (1, 3);
	lcd_printf ("Elimina timer");

	scelta = aggiorna_cursore_opz (0, 3);	//12=menu = 1_2
	sk_clear ();

	if (scelta == 0) ;	//ritorna
	else if (scelta == 1)
		sk_menu_1_2_3_1 ();	// imposta timer
	else if (scelta == 2)
		sk_menu_1_2_3_2 ();	// mostra timer
	else if (scelta == 3)
		sk_menu_1_2_3_3 ();	// elimina timer

}



inline void
sk_menu_1_3b ()
{

	y_pos (1, 0);
	lcd_printf ("<<     INFO");
	y_pos (1, 1);
	lcd_printf ("Progetto opensource");
	y_pos (1, 2);
	lcd_printf ("  per la gestione   ");
	y_pos (1, 3);
	lcd_printf ("     di acquari     ");
	aggiorna_cursore_opz (0, 0);	//min,max quindi solo ritornare indietro

}
inline void
sk_menu_1_2b ()
{
	unsigned char level;
	y_pos (1, 0);
	lcd_printf ("<<  PERISTALTICA");
	y_pos (1, 1);
	level = peristaltica_read_level ();
	level = sk_chose_onoff (level);
	peristaltica_set_level (level);

}

inline void
sk_menu_1_1b ()
{


	y_pos (1, 0);
	lcd_printf ("><<  LIVELLO ACQUA");

	while (p_status () != P_OK)
	{
		y_pos (1, 2);
		lcd_printf ("G1= ");

		if (galleggiante_read_level (1) == 1)
		{
			lcd_printf ("Ok ");

		}
		else if (galleggiante_read_level (1) == 0)
		{
			lcd_printf ("Bad");
		}
		y_pos (10, 2);
		lcd_printf ("G2= ");
		if (galleggiante_read_level (2) == 1)
		{
			lcd_printf ("Ok ");
		}
		else if (galleggiante_read_level (2) == 0)
		{
			lcd_printf ("Bad");
		}
	}
}
inline void
sk_menu_1_3 ()
{
	unsigned char scelta;
	y_pos (1, 0);

	lcd_printf ("<< GESTIONE SONDE");
	y_pos (1, 1);

	lcd_printf ("Assegna nomi");
	y_pos (1, 2);

	lcd_printf ("Leggi valori");

	scelta = aggiorna_cursore_opz (0, 3);	//12=menu = 1_2
	sk_clear ();
	if (scelta == 0) ;	//ritorna
	else if (scelta == 1)
		sk_menu_1_3_1 ();
	else if (scelta == 2)
		sk_menu_1_3_2 ();

}


inline void
sk_menu_1_2 ()
{
	unsigned char scelta;
	y_pos (1, 0);

	lcd_printf ("<< GESTIONE PRESE");
	y_pos (1, 1);
	lcd_printf ("Assegna nomi");

	y_pos (1, 2);
	lcd_printf ("Cambia stato");

	y_pos (1, 3);
	lcd_printf ("Timer");

	scelta = aggiorna_cursore_opz (0, 3);	//12=menu = 1_2
	sk_clear ();
	if (scelta == 0) ;	//ritorna
	else if (scelta == 1)
		sk_menu_1_2_1 ();	//ASSEGNA NOMI
	else if (scelta == 2)
		sk_menu_1_2_2 ();	//caMBIA STATO
	else if (scelta == 3)
		sk_menu_1_2_3 ();	//timer

}

inline void
sk_menu_1_1 ()
{
	unsigned char min = 0, hr = 0, gg = 0, mese = 0, anno = 0;
	char buff[50];
	char conv[5];


	time_t now;
	struct tm *tm_now;



	y_pos (0, 0);
	lcd_printf ("<<  CAMBIA  DATA");


	now = time (NULL);
	tm_now = localtime (&now);
	strftime (conv, sizeof conv, "%H", tm_now);
	hr = atoi (conv);
	strftime (conv, sizeof conv, "%M", tm_now);
	min = atoi (conv);
	strftime (conv, sizeof conv, "%d", tm_now);
	gg = atoi (conv);
	strftime (conv, sizeof conv, "%m", tm_now);
	mese = atoi (conv);
	strftime (conv, sizeof conv, "%y", tm_now);
	anno = atoi (conv);



	y_pos (2, 2);
	lcd_printf ("%d:%d  %d/%d/%d", hr, min, gg, mese, anno);

	// x,y,partenza,min,max
	hr = inc_cifra (2, 2, hr, 0, 24);	// hh
	min = inc_cifra (5, 2, min, 0, 59);	// mm
	gg = inc_cifra (9, 2, gg, 0, 31);	// gg
	mese = inc_cifra (12, 2, mese, 0, 12);	// m
	anno = inc_cifra (15, 2, anno, 7, 50);	// aa
	// verifica data x gg bisestili e gg de mesi

	//se ok salva il valore
	strcpy (buff, "date ");
	if (mese < 10)
		strcat (buff, "0");
	strcat (buff, itoa (mese));
	if (gg < 10)
		strcat (buff, "0");
	strcat (buff, itoa (gg));
	if (hr < 10)
		strcat (buff, "0");
	strcat (buff, itoa (hr));
	if (min < 10)
		strcat (buff, "0");
	strcat (buff, itoa (min));
	strcat (buff, itoa (2000 + anno));
	printf ("Data impostata: %s", buff);
	system (buff);		// imposta la data
	//la salva nell rtc
	system ("hwclock -w");
	sk_clear ();
	y_pos (4, 3);
	lcd_printf ("DATA SALVATA");
	delay_ms (1000);
}

inline unsigned char
sk_menu_1a ()
{
	unsigned char scelta;
	y_pos (1, 0);
	lcd_printf ("<<     MENU ");
	y_pos (1, 1);
	lcd_printf ("Cambia la data");
	y_pos (1, 2);
	lcd_printf ("Gestione prese");
	y_pos (1, 3);
	lcd_printf ("Gestione sonde");
	barra_menu_vert (0);

	scelta = aggiorna_cursore_opz (0, 4);
	sk_clear ();
	if (scelta == 0)
		delay_ms (1);	//ritorna
	else if (scelta == 1)
		sk_menu_1_1 ();
	else if (scelta == 2)
		sk_menu_1_2 ();
	else if (scelta == 3)
		sk_menu_1_3 ();

	if (scelta == 4)
		return 1;
	else
		return 0;

}

inline unsigned char
sk_menu_1b ()
{
	unsigned char scelta;
	y_pos (1, 0);
	lcd_printf ("<<     MENU ");
	y_pos (1, 1);
	lcd_printf ("Livello acqua");
	y_pos (1, 2);
	lcd_printf ("Peristaltica");
	y_pos (1, 3);
	lcd_printf ("Info");

	barra_menu_vert (2);
	scelta = aggiorna_cursore_opz (0, 3);
	sk_clear ();

	if (scelta == 1)
		sk_menu_1_1b ();
	else if (scelta == 2)
		sk_menu_1_2b ();
	else if (scelta == 3)
		sk_menu_1_3b ();


	if (scelta == 0)
		return 1;
	else
		return 0;
}

inline void
sk_menu_1 ()
{

	if (sk_menu_1a () == 1)
		sk_menu_1b ();
	//else ritorna

}
