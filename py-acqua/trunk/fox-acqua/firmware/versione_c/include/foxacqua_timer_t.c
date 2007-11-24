//#    File test per il modulo foxacqua_timer.c

//compilare con:
//	gcc -o test -g include/foxacqua_timer.c include/foxacqua_timer_t.c 

#include "foxacqua_time.h"

int main (void) {
	
	s_timer a,b,c;

	a.ora=1801;
	a.pin=22;
	a.num=10;
	a.stato= 3;

	set_timer(&a);

	read_timer(&b,10);

	del_timer(10);

	read_timer(&c,10);


}
	
