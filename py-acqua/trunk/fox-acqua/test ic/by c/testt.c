//#Copyright (C) 2005, 2006 Luca Sanna - Italy
//#http://pyacqua.altervista.org
//#email: pyacqua@gmail.com  
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
//*************************************************


//#*********************************************************************
//# 
//#   TEST DELL'INTEGRATO MCP23016 
//#
//#*********************************************************************



#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "sys/ioctl.h"
#include "fcntl.h"
#include "time.h"
#include "string.h"
#include "linux/gpio_syscalls.h"


int main(int argc, char **argv) {
int i;

// set IOG8-15 as output
  gpiosetdir(PORTG, DIROUT, PG8_15);


	gpiosetdir(PORTG, DIROUT, PG24);//iog24
	gpiosetdir(PORTA, DIROUT, PA3);

for(;;){
	printf(".\n");
	gpiotogglebit(PORTG, PG24);
	gpiotogglebit(PORTA, PA3);
	sleep(1);
}




/*



	if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }

  while(1) {




	printf("\nGPIO0 = %d - GPIO1 = %d",mcp230xx_regLeggi(lcdMcp23016_id,GPIO0),mcp230xx_regLeggi(lcdMcp23016_id,GPIO1));
	

	sleep(1);

  }*/



  return(0);
}



