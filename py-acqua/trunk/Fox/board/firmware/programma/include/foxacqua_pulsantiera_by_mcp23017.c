#include "foxacqua_pulsantiera_by_mcp23017.h"
#ifndef  lcdMcp23017_id
	#define lcdMcp23017_id	0x20
#endif
int p_status(){
	unsigned char valore;
	valore=mcp230xx_regLeggi(lcdMcp23017_id,mcp23017GPIOB);
	if (valore==0) return 0;
	else if (valore==8) return (P_OK);
	else if (valore==1)return (P_UP);
	else if (valore==16)return (P_DOWN);
	else if (valore==2)return (P_RIGHT);
	else if (valore==4)return (P_LEFT);
}
