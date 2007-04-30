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


// EEPROM id: A0,A2,A4,A6,A8,AA,AC,AE



int ext_eeprom_ready(unsigned char id){
	int ack;
	i2c_start();
	ack=i2c_outbyte(id);
	i2c_stop();
	return ack;

}

void write_ext_eeprom(unsigned char id,long int address, unsigned char data){

while(!ext_eeprom_ready(id));
	i2c_start();
	i2c_outbyte((id|(int)(address>>7))&0xfe);
	i2c_outbyte(address);
	i2c_outbyte(data);
	i2c_stop();

}

unsigned chat read_ext_eeprom(unsigned char id, long int address){
unsigned char data;
while(!ext_eeprom_ready(id));
	i2c_start();
	i2c_outbyte((id|(int)(address>>7))&0xfe);
	i2c_outbyte(address);
	i2c_start();
	i2c_outbyte((id|(int)(address>>7))|1);
	data=i2c_inbyte(0);
	i2c_stop();
	return data;//tra parentesi data (data)
}


int  main (void) {
int scelta;
int cella,dato,dato_chek;

    if (i2c_open()<0) { printf("Apertura del bus I2C fallita\n"); return 1; }


    for(;;){

	printf("GESTIONE EEPROM 24xx\n");
	printf("Operazioni possibili:\n");
	printf("1:Lettura\n");
	printf("2:Scrittura\n");
	printf("3:Esci\n");
	
	scanf ("%X",&scelta);
	if (scelta==1){
		printf("Inserisci il numero della cella da leggere ( 0..FF) ");
		scanf ("%X",&cella);
		dato=read_ext_eeprom(0xa0,cella);
		printf("dato= %d\n",dato);
	}
	else if (scelta==2){
		printf("Inserisci il numero della cella (0..FF) da scrivere ");
		scanf ("%X",&cella);
		printf("Inserisci il numero del dato (0..FF) da memorizare ");
		scanf ("%X",&dato);
		write_ext_eeprom(0xa0,cella,dato); // A0= ID
		//verifica il dato	
		dato_chek=read_ext_eeprom(0xa0,cella); // A0= ID EEPRM
		if (dato==dato_chek) printf("dato scritto correttamente");
		else printf("errore, dato scritto= %d",dato_chek);
	}
	else if (scelta==3) return 1;
    
}
}

unsigned char sonde_plugin(){
unsigned char i;
for(i=0xa0;i<0xb0;i=i+2) dato=read_ext_eeprom(0xa0,cella);


}




