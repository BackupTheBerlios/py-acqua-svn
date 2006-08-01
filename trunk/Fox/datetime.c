#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <errno.h>
#include "i2c_routine.c"

int  main (void)
{
     if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }

	ds1307_init();

	input_data();
	set_data(giorno_in,mese_in,anno_in);
	input_ora();
	set_ora(ora_in,minuto_in);

        //timenow(0);
        //datanow();

	//printf ("%s \r\n", " ");
	//printf("Data: %s \r\n",data_attuale);
	//printf("Ora: %s \r\n",orario);
	//printf ("%s \r\n", " ");
	
	printf ("%s \r\n", " ");
	setsystemdate();
	printf ("%s \r\n", " ");
}
