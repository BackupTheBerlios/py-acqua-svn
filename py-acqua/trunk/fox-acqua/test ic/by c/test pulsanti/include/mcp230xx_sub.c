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


#include "mcp230xx_sub.h"

unsigned char mcp230xx_regLeggi(unsigned char id, unsigned char reg){
	unsigned char data;

	i2c_start();
	i2c_outbyte(id); 
	i2c_outbyte(reg);
	i2c_start();
	i2c_outbyte(id+1);  
	data=i2c_inbyte(0);
	i2c_stop();
	return data;
}
void mcp230xx_regScrivi(unsigned char id, unsigned char registro,unsigned char value){
	i2c_start();
	i2c_outbyte(id);
	i2c_outbyte(registro);
	i2c_outbyte(value);
	i2c_stop();
}
void mcp230xx_pinWriteLevel(unsigned char id, unsigned char gp,unsigned char pin,unsigned char level){
	unsigned char value;
		
	value=mcp230xx_regLeggi(id,gp);
	if (level==1) value=value | (1 << pin ); // = 2^pin
	else  value=value & ( 0xff -(1 << pin ));	
	mcp230xx_regScrivi(id,gp,value);
	
}
unsigned char mcp230xx_pinReadLevel(unsigned char id, unsigned char gp,unsigned char pin){
	unsigned char value;
			
	value=mcp230xx_regLeggi(id,gp);
	value=value & (1 << pin );
	if (value==(1 << pin )) return 1;
	else return 0;
}

			
