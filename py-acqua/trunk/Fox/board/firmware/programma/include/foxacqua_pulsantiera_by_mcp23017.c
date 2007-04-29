#include "foxacqua_pulsantiera_by_mcp23017.h"
#ifndef  lcdMcp23017_id
	#define lcdMcp23017_id	0x27
#endif
int p_status(){
	unsigned char valore;
	valore=mcp23017_regLeggi(lcdMcp23017_id,GPIOB);
	if (valore==8) return (P_OK);
	else if (valore==1)return (P_UP);
	else if (valore==16)return (P_DOWN);
	else if (valore==2)return (P_RIGHT);
	else if (valore==4)return (P_LEFT);
}
