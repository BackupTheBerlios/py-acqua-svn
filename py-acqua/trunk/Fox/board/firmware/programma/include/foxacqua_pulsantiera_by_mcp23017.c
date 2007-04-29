#include "foxacqua_pulsantiera_by_mcp23017.h"
#ifndef  lcdMcp23017_id
	#define lcdMcp23017_id	0x27
#endif
int p_status(){
	int value;
	value=mcp23017_regLeggi(lcdMcp23017_id,GPIOB);
	if (value==8) return (P_OK);
	else if (value==1)return (P_UP);
	else if (value==16)return (P_DOWN);
	else if (value==2)return (P_RIGHT);
	else if (value==4)return (P_LEFT);
}
