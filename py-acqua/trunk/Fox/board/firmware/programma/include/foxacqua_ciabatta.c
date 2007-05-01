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

//richiede che sia incluso il file dei pulsanti

char prese_nomi[8][15][2]={
				{"P","r","e","s","a","1"},
				{"P","r","e","s","a","2"},
				{"P","r","e","s","a","3"},
				{"P","r","e","s","a","4"},
				{"P","r","e","s","a","5"},
				{"P","r","e","s","a","6"},
				{"P","r","e","s","a","7"}
			}; // 8 nomi da 15 caratterri 

#define preseMcp23008_id	0x27
#define presa1			0
#define presa2			1
#define presa3			2
#define presa4			3
#define presa5			4
#define presa6			5
#define presa7			6
#define	reg_prese		0X09 // = GPIO

void ciabatta_init(){
	mcp230xx_regScrivi(preseMcp23008_id,mcp23008IODIR,0);
	mcp230xx_regScrivi(preseMcp23008_id,reg_prese,0);

}
void presa_set_level(unsigned char presa,unsigned char level){
// presa 1..7
// level 0..1
	mcp230xx_pinWriteLevel(preseMcp23008_id,reg_prese,--presa,level);
}

unsigned char presa_read_level(unsigned char presa){
// presa 1..7
	return mcp230xx_pinReadLevel(preseMcp23008_id, reg_prese,--presa);
}



unsigned char imposta_stato(unsigned char presa){
	unsigned char level,press;
	y_pos(1,1);
	lcd_printf("Scegli lo stato");
	y_pos(6,2);
	lcd_printf(" 0     1");
	level=presa_read_level(presa);
	//porta il cursore sullivello del pin	
	if (level) 	y_pos(6,2);					
	else		y_pos(12,2);			
	lcd_printf(">");	
	while(p_status() != P_OK){
		press=p_status();
		if (press==P_LEFT)	{
			y_pos(12,2);			
			lcd_printf(" ");
			y_pos(6,2);			
			lcd_printf(">");
			level=1;	
			while (p_status()==P_LEFT) msDelay(10);		
		}
		if (press==P_RIGHT)	{
			y_pos(6,2);			
			lcd_printf(" ");
			y_pos(12,2);			
			lcd_printf(">");
			level=0;		
			while (p_status()==P_RIGHT) msDelay(10);		
		}
		//mcp230xx_regScrivi(preseMcp23008_id,reg_prese,++valore);
		msDelay(50);
	}
	return level;
}



unsigned char scegli_presa(){
// ritorna 1..7
	unsigned char scelta,presa,press,i;
	y_pos(1,1);
	lcd_printf("Scegli la presa");
	y_pos(4,2);
	lcd_printf(">1 2 3 4 5 6 7");
	y_pos(3,3);	
	for (i=0;i<15;i++) lcd_printf(prese_nomi[0][i]);
			
	scelta=4;
	y_pos(scelta,2);
	presa=1;
	while(p_status() != P_OK){
		press=p_status();
		if (press!=0)	{
			y_pos(scelta,2);
			lcd_printf(" ");	
			if (press==P_RIGHT)	{
				scelta+=2;
				presa++; 			
				if (scelta>17){
					scelta=4;
					presa=0;
				}
			}
			if (press==P_LEFT)	{
				scelta-=2;
				presa--; 			
				if (scelta<4){
					scelta=16;
					presa=6;
				}
			}
			y_pos(scelta,2);
			lcd_printf(">");
			y_pos(3,3);
			for (i=0;i<15;i++) lcd_printf(prese_nomi[presa-1][i]);
			while (p_status()!=0) msDelay(10);		
		msDelay(50);
		}
	}
	clean_row(2);
	return presa; // da1..7
}


//da spostare in qualke altro file, viene comoda anke x assegnare i nomi alle sonde.... oppure il nome esce in automatiko...
// kidere al gruppo.... boh..
void assegna_nome(unsigned x, unsigned y, unsigned char presa){
//presa 1..7
char alfabeto[37][2]={"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," ","0","1","2","3","4","5","6","7","8","9"};
	char nome[15][2];
	unsigned char lettera,carattere,press,i;
	y_pos(x,y);						
	lettera=0;
	carattere=0;
	while(p_status() != P_OK){
		press=p_status();
		if (press!=0){
			if (press==P_DOWN)	{
				if(lettera<26) lettera++;
				else lettera=0;	
			}
			else if (press==P_UP)	{
				if(lettera<26) lettera++;
				else lettera=0;		
			}	
			if (press==P_RIGHT)	{
				if(carattere<15){
					nome[carattere][0]=alfabeto[lettera][0];
					carattere++;
					x++; // avanza di un carattere
					lettera=0;// il prox carattere partirà dalla lettere a.
				}
			}
			y_pos(x,y);	
			lcd_printf(alfabeto[lettera]);
			while (p_status()!=0) msDelay(10);	
			
				
		}	
		msDelay(50);
	}
presa--;
for(i=0;i<carattere;i++) prese_nomi[presa][i][0]=nome[i][0];
//for(i=carattere;i<15;i++) prese_nomi[presa][i][0]=" ";//azera gli altri caratteri


}




