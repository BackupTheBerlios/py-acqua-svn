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
//#   TEST 
//#
//#*********************************************************************

//pin iog17 e iog24

#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "sys/ioctl.h"
#include "fcntl.h"
#include "time.h"
#include "string.h"
#include "linux/gpio_syscalls.h"

#define SDA	PG17
#define SCL	PG24


int main(int argc, char **argv) {

  // set PA0 as output
  gpiosetdir(PORTG, DIROUT, SCL);

  // set PB7 as output
  gpiosetdir(PORTG, DIROUT, SDA);


  while(1) {
    printf(".\n");
    gpiosetbits(PORTG, SDA);
    gpiosetbits(PORTG, SCL);
    sleep(1);
    
    printf(".\n");
    gpioclearbits(PORTG, SDA);
    gpioclearbits(PORTG, SCL);   
    sleep(1);
  }
  return(0);
}










