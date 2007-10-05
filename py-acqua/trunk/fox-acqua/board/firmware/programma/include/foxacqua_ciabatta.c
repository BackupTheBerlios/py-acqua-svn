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



unsigned char prese_nomi[7][10];//7 nomi da 10 caratteri


//99 sar� il valore x far capire ke quell'ora nn � attiva la sveglia
unsigned char presa_timer[7][10][2];// 7 prese x 10 eventi l'una x [0]ora e [1]min
unsigned char presa_timer_stato[7][10];// stato di 7 prese x 10 eventi al momento del match tra rtc e tempo qui impostato.
                             // ogni presa ha 10 timer. un timer non attivo presenta valore 99.
                             // se la presa deve essere impostata in spento, conterr� 0, altrimenti 1.




#define preseMcp23008_id	0x27
#define presa1			0
#define presa2			1
#define presa3			2
#define presa4			3
#define presa5			4
#define presa6			5
#define presa7			6
#define	reg_prese		0X09 // = GPIO




//#inline
unsigned char  sk_chose_onoff(unsigned char level){
	unsigned char press;
	y_pos(1,1);
	lcd_printf("Scegli lo stato");
	y_pos(1,2);

	lcd_printf("      0     1      ");
	//porta il cursore sullivello del pin
	if (!level) 	y_pos(6,2);
	else		y_pos(12,2);

	lcd_printf(">");
	press=0;
	while(p_status() != P_OK){
		press=p_status();
		if (press!=0)	{
			if (press==P_LEFT)	{
				y_pos(12,2);
				lcd_printf(" ");

				y_pos(6,2);
				lcd_printf(">");
				level=0;
				while (p_status()==P_LEFT) ;
			}
			if (press==P_RIGHT)	{
				y_pos(6,2);
				lcd_printf(" ");
				y_pos(12,2);
				lcd_printf(">");
				level=1;
				while (p_status()==P_RIGHT) ;
			}
		}
	}
	while(p_status()== P_OK);
	return level;
}

//#inline
void ciabatta_init(){
  unsigned char i,j;

   mcp230xx_regScrivi(preseMcp23008_id,mcp23008IOCON,0x24); //slew rate su sda, interrupt disablitati, no pull up // 00011000
	mcp230xx_regScrivi(preseMcp23008_id,mcp23008IPOL,0x00);//lettura non complementata
	mcp230xx_regScrivi(preseMcp23008_id,mcp23008GPINTEN,0x00);//nessun interrupt
	mcp230xx_regScrivi(preseMcp23008_id,mcp23008IODIR,0x00);//tutti out
	mcp230xx_regScrivi(preseMcp23008_id,reg_prese,0x00);//tutti accesi
   for (i=0;i<7;i++){
      for (j=0;j<10;j++){
         presa_timer_stato[i][j]=99;// nessun timer impostato
         presa_timer[i][j][0]=0; // ora visualizzata= 00:00
         presa_timer[i][j][1]=0; // ora visualizzata= 00:00
         //azzera nomi
         prese_nomi[i][j]=0;//' '
      }
   }
}

//#inline
void presa_set_level(unsigned char presa,unsigned char level){
// presa 1..7
// level 0..1
	mcp230xx_pinWriteLevel(preseMcp23008_id,reg_prese,--presa,level);
}
//#inline
unsigned char presa_read_level(unsigned char presa){
// presa 1..7
	return mcp230xx_pinReadLevel(preseMcp23008_id, reg_prese,--presa);
}
//#inline
unsigned char imposta_stato(unsigned char presa){//1..7
	return sk_chose_onoff(presa_read_level(presa));
}

unsigned char scegli_presa(){
// ritorna 1..7
	unsigned char scelta,presa=1,press,i;
	y_pos(1,1);

	lcd_printf("Scegli la presa");
	y_pos(4,2);
	lcd_printf(">1 2 3 4 5 6 7");
	y_pos(3,3);
	for (i=0;i<10;i++)   lcd_printf("%c",*alfabeto[prese_nomi[presa-1][i]]);

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
					presa=1;
				}
			}
			else if (press==P_LEFT)	{
				scelta-=2;
				presa--;
				if (scelta<4){
					scelta=16;
					presa=7;
				}
			}
			y_pos(scelta,2);
			lcd_printf(">");
			y_pos(3,3);
			for (i=0;i<10;i++)   lcd_printf("%c",*alfabeto[prese_nomi[presa-1][i]]);
		}
	}
	clean_row(3);
	while(p_status()== P_OK);
	return presa; // da1..7
}


//da spostare in qualke altro file, viene comoda anke x assegnare i nomi alle sonde.... oppure il nome esce in automatiko...
// kidere al gruppo.... boh..
void assegna_nome(unsigned x, unsigned y, unsigned char presa){
//presa 1..7

	unsigned char nome[10];
	unsigned char lettera,carattere,press,i;
	
	for(i=0;i<10;i++) nome[i]=0;
	y_pos(3,2);
	lcd_printf("__________      ");

	lettera=0; // ' '
	carattere=0;
	y_pos(x,y+1);
	lcd_printf("^");
	while(p_status() != P_OK){

		press=p_status();
		if (press!=0){
			if (press==P_DOWN)	{
				if(lettera>0) lettera--;
				else lettera=36;
			}
			else if (press==P_UP)	{
				if(lettera<36) lettera++;
				else lettera=0;
			}
			else if (press==P_RIGHT)	{
				if(carattere<9){
					nome[carattere]=lettera;//alfabeto[lettera]
					carattere++;
					x++; // avanza di un carattere
					lettera=0;// il prox carattere partir�� dalla lettera ' '.
				}
			}
			y_pos(x,y);
			lcd_printf("%c",alfabeto[lettera]);
			y_pos(x-1,y+1);
			lcd_printf(" ^");
			while (p_status()!=0) ;
		}
 	}
	//salva ultimo carattere
	nome[carattere]=lettera;   
	//salva il nome
	presa--;
	
	for(i=0;i<10;i++) prese_nomi[presa][i]= nome[i];
	
	lcd_clear();
	y_pos(2,2);
	lcd_printf("DATI SALVATI");
	delay_ms(2000);
}


