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
//#
//#  MCP230xx ROUTINES

#ifndef MCP230XX_SUB_H
#define MCP230XX_SUB_H


//N.B. : 'id' è comprensivo del bit r/w impostato a zero



//REGISTRI IN GENERALE
unsigned char 	mcp230xx_regLeggi(unsigned char id, unsigned char reg);	//ritorna il valore del registro
void 		mcp230xx_regScrivi(unsigned char id, unsigned char registro,unsigned char value);//scrive il valore del registro

// SEMPLIFICA GESTIONE I/O
void 		mcp230xx_pinWriteLevel(unsigned char id, unsigned char gp,unsigned char pin,unsigned char level);//cambia stato ad un pin
unsigned char 	mcp230xx_pinReadLevel(unsigned char id, unsigned char gp,unsigned char pin);//ritorna lo stato logico di un pin

#endif			
