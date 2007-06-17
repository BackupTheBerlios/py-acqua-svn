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

/***************
//	SCHERMATE
//
//	MENU
//
***************
//0,0	riga1 
//0,20  riga2
//1,0   riga3
//1,20  riga4*/


void sk_clear(){
	lcd_clear(); 
}
void sk_init(){
 	y_pos(7,0);
	lcd_printf("VISITA");	
		
 	y_pos(2,1);
	lcd_printf("www.pyacqua.net"); 
	y_pos(0,3);
	lcd_printf("--------------------");	
	msDelay(3000);
	sk_clear();
	
}
void sk_main(){
unsigned char i;
	y_pos(1,0);
	lcd_printf(" P:");
	for(i=1;i<8;i++) lcd_printf("%X",presa_read_level(i));
			
	y_pos(1,3);
	lcd_printf("Menu");			
	cursore_scegli_opz(3);
}






void sk_menu_1_3_1(){
unsigned char sonda;
	y_pos(1,0);
	lcd_printf("<<  ASSEGNA NOMI");
	sonda=scegli_sonda();
	assegna_nome(3,2,sonda); //x,y
}
void sk_menu_1_3_2(){

unsigned char sonda;

	y_pos(1,0);
	lcd_printf("<<  LEGGI VALORI");
	sonda=scegli_sonda();
sk_clear();
 //ad_regLeggi(mcp_ad1);
	//printf("valor %d\n",valo[0]); 

	//printf("valor %d\n",valo[1]);



}



void sk_menu_1_2_1(){
unsigned char presa;
	y_pos(1,0);
	lcd_printf("<<  ASSEGNA NOMI");
	presa=scegli_presa();
	assegna_nome(3,2,presa); //x,y
}
void sk_menu_1_2_2(){
unsigned char scelta,stato;
	y_pos(1,0);
	lcd_printf("<<  CAMBIA STATO ");	
	scelta=scegli_presa();
	stato=imposta_stato(scelta);
	presa_set_level(scelta,stato);
}
void sk_menu_1_2_3(){
unsigned char scelta;
	y_pos(1,0);
	lcd_printf("<< IMPOSTA TIMER");	
	scelta=scegli_presa();
//cursore su linea x

}






void sk_menu_1_3b(){
unsigned char scelta;
	y_pos(1,0);
	lcd_printf("<<     INFO");			
	y_pos(1,1);
	lcd_printf("Progetto opensource");			
	y_pos(1,2);
	lcd_printf("  per la gestione   ");			
	y_pos(1,3);
	lcd_printf("     di acquari     ");		
	scelta=aggiorna_cursore_opz(0,0);//min,max quindi solo ritornare indietro
	
}
void sk_menu_1_2b(){
unsigned char scelta,level;
	y_pos(1,0);
	lcd_printf("<<  PERISTALTICA");			
	y_pos(1,1);

	level=peristaltica_read_level();
	level=sk_chose_onoff(level);
	peristaltica_set_level(level);

	
}
void sk_menu_1_1b(){
unsigned char scelta,level;

	y_pos(1,0);
	lcd_printf("><<  LIVELLO ACQUA");

	while	(p_status() != P_OK){			
		y_pos(1,2);
		lcd_printf("G1= ");	
		if(galleggiante_read_level(1)==1)lcd_printf("Ok ");
		else if(galleggiante_read_level(1)==0)lcd_printf("Bad");
	
		y_pos(10,2);
		lcd_printf("G2= ");	
		if(galleggiante_read_level(2)==1)lcd_printf("Ok ");
		else if(galleggiante_read_level(2)==0)lcd_printf("Bad");
	}
}

void sk_menu_1_3(){
unsigned char scelta;
	y_pos(1,0);
	lcd_printf("<< GESTIONE SONDE");
	y_pos(1,1);
	lcd_printf("Assegna nomi");		
	y_pos(1,2);
	lcd_printf("Leggi valori");		
	
	scelta=aggiorna_cursore_opz(0,3);//12=menu = 1_2
	sk_clear();
	if (scelta==0) udelay(1);//ritorna
	else if (scelta==1) sk_menu_1_3_1(); 
	else if (scelta==2) sk_menu_1_3_2();

}
void sk_menu_1_2(){
unsigned char scelta;
	y_pos(1,0);
	lcd_printf("<< GESTIONE PRESE");
	y_pos(1,1);
	lcd_printf("Assegna nomi");		
	y_pos(1,2);
	lcd_printf("Cambia stato");		
	y_pos(1,3);
	lcd_printf("Imposta timer");
	
	scelta=aggiorna_cursore_opz(0,3);//12=menu = 1_2
	sk_clear();
	if (scelta==0) udelay(1);//ritorna
	else if (scelta==1) sk_menu_1_2_1(); 
	else if (scelta==2) sk_menu_1_2_2();
	else if (scelta==3) sk_menu_1_2_3();
	
}
void sk_menu_1_1(){
	
	char valore[5];
//	int intervalli[6];
	// leggi rtc
	y_pos(0,0);
	lcd_printf("<<  CAMBIA  DATA");			
	y_pos(2,2);
	//lcd_printf("15:00   25/04/07");
//ora 
  valore[0]=read_hour();
  lcd_printf("%02d:",valore[0]);
  valore[1]=read_min();
  lcd_printf("%02d  ",valore[1]);

//data 
  valore[2]=read_day();
  lcd_printf("%02d",valore[2]);
  valore[3]=read_month();
  lcd_printf("/%02d",valore[3]);
  valore[4]=read_year();
  lcd_printf("/%02d",valore[4]);

	// x,y,partenza,min,max
	valore[0]=inc_cifra(2,2,valore[0],0,24);// hh 
	valore[1]=inc_cifra(5,2,valore[1],0,59);// mm
	set_ora(valore[0],valore[1]);
	
	valore[2]=inc_cifra(9,2,valore[2],0,31);// gg
	valore[3]=inc_cifra(12,2,valore[3],0,12);// m
	valore[4]=inc_cifra(15,2,valore[4],7,20);// aa
	// verifica data x gg bisestili e gg de mesi
	set_data(valore[2],valore[3],valore[4]);
	
	//se ok salva il valore
	y_pos(4,3);
		
	if (true) lcd_printf("DATA SALVATA");
	else lcd_printf("DATA ERRATA");
	msDelay(2000);		

}

unsigned char sk_menu_1a(){
	unsigned char scelta;
	y_pos(1,0);
	lcd_printf("<<     MENU ");			
	y_pos(1,1);
	lcd_printf("Cambia la data");			
	y_pos(1,2);
	lcd_printf("Gestione prese");			
	y_pos(1,3);
	lcd_printf("Gestione sonde");
	barra_menu_vert(0);
	scelta=aggiorna_cursore_opz(0,4);
	sk_clear();
	if (scelta==0) udelay(1);//ritorna
	else if (scelta==1) sk_menu_1_1(); 
	else if (scelta==2) sk_menu_1_2();
	else if (scelta==3) sk_menu_1_3();
	
	if (scelta==4) return 1;
	else return 0;	

}

unsigned char  sk_menu_1b(){
	unsigned char scelta;
	y_pos(1,0);
	lcd_printf("<<     MENU ");			
	y_pos(1,1);
	lcd_printf("Livello acqua");			
	y_pos(1,2);
	lcd_printf("Peristaltica");			
	y_pos(1,3);
	lcd_printf("Info");
	barra_menu_vert(2);
	scelta=aggiorna_cursore_opz(0,3);
	sk_clear();

	if (scelta==1) sk_menu_1_1b();
	else if (scelta==2) sk_menu_1_2b();
	else if (scelta==3) sk_menu_1_3b();


	if (scelta==0) return 1;
	else return 0;	
	}

void sk_menu_1(){
unsigned char sk_last,sk_next;
	sk_last=1;
	sk_next=0;

	while (sk_last==1) {
		sk_next=sk_menu_1a();
		if (sk_next==1) {
			sk_last=sk_menu_1b();
			//if (sk_last==0) break ;// ritorna zero se è entrato in una voce del 2° menu
		}
		//else break;
	
	}
}


