#!/usr/bin/env python
# -*- coding: iso-8859-15 -*- 
#Copyright (C) 2005, 2006 Luca Sanna - Italy
#http://pyacqua.altervista.org
#email: pyacqua@gmail.com  
#
#   
#Py-Acqua is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#Py-Acqua is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Py-Acqua; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import pygtk
pygtk.require('2.0')
import gtk
import os
#from pysqlite2 import dbapi2 as sqlite

import files.finestre

### creiamo la directory che contiene le immagini

if not os.path.exists('Immagini'):
	os.system('mkdir Immagini') 
else:
	pass
	
### creiamo la directory che contiene il database

if not os.path.exists('Data'):
	os.system('mkdir Data') 
else:
	pass


### creiamo il database con sqlite

if not os.path.exists("Data/db"):
	
	
	connessione=sqlite.connect("Data/db")
	cursore=connessione.cursor()
	cursore.execute("create table test(id integer primary key, d DATE, vasca FLOAT, ph FLOAT, kh FLOAT, gh NUMERIC, no NUMERIC, noo NUMERIC, con NUMERIC, amm NUMERIC, fe NUMERIC, ra NUMERIC, fo NUMERIC)")
	cursore.execute("create table pesci(id integer primary key, da DATE, vasca FLOAT, d NUMERIC, testo TEXT, im TEXT,va FLOAT)")
	cursore.execute("create table piante(id integer primary key, da DATE, vasca FLOAT, d NUMERIC, testo TEXT, im TEXT,va FLOAT)")
	cursore.execute("create table fertilizzante (id integer primary key,da DATE, d TEXT, testo FLOAT, gio FLOAT)")
	cursore.execute("create table filtro (id integer primary key,d DATE, q FLOAT)")
	cursore.execute("create table datapesci (nome TEXT, cara TEXT)")
	cursore.execute("create table datapiante (nome TEXT, cara TEXT)")
	cursore.execute("create table vasca (id integer primary key, t TEXT, da DATE, a TEXT, aa TEXT, b TEXT, c TEXT, d TEXT, im TEXT)")
	connessione.commit()
else:
	pass

class Gui:
	def get_main_menu(self, main):
		accel_group = gtk.AccelGroup()
		item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
		item_factory.create_items(self.menu_items)
		main.add_accel_group(accel_group)
		self.item_factory = item_factory
		return item_factory.get_widget("<main>")
	
	def __init__(self):
### creiamo il menu
		self.menu_items = (
			( "/_Acquario",         None,         None, 0, "<Branch>" ),
			( "/Acquario/_Calcoli",     "<control>N", self.calcoli_apri, 0, None ),
			( "/Acquario/_Vasche",    "<control>O", self.vasca_apri, 0, None ),
			( "/Acquario/_Test",    "<control>S", self.test_apri, 0, None ),
			( "/Acquario/_Pesci", None,         self.pesci_apri, 0, None ),
			( "/Acquario/_Piante",     None,         self.piante_apri, 0, None ),
			( "/Acquario/_Database",	None,	None,	0,	"<Separator>" ),
			( "/Acquario/Quit",     "<control>Q", gtk.main_quit, 0, None ),
			( "/_Impostazioni",      None,         None, 0, "<Branch>" ),
			( "/Impostazioni/_Grafico",  None,         None, 0, None ),
			( "/Impostazioni/_Tips Tricks",	None,	self.tips_apri,	0,	None ),
			( "/Impostazioni/_Calendario",	None,	self.calendario_apri,	0,	None ),
			( "/Impostazioni/_Inserisci",	None,	self.inserisci_apri,	0,	None ),
			( "/Impostazioni/_Allarmi",	None,	None,	0,	None ),
			( "/_Aiuto",         None,         None, 0, "<LastBranch>" ),
			( "/_Aiuto/Informazioni",   None,         self.informazioni_apri, 0, None ),
			)
			
		win = files.finestre.main(467, 332, "py-Acqua", 0)
# inseriamo l' immagine nella finestra principale	
		image = gtk.Image()
		image.set_from_file("pixmaps/main.png")
		table = gtk.Table(2, 2, False)
		table.set_border_width(0)
		win.add(table)
				
		menubar = self.get_main_menu(win)
		table.attach(menubar, 0, 1, 0, 1)
		table.attach(image,0, 1, 1, 101)
		menubar.show()
		table.show()
		win.show_all()
		
	def calcoli_apri(self, widget, data=None):
		import files.calcoli
		return files.calcoli.win2()
		
	def test_apri(self, widget, data=None):
		import files.test
		return files.test.win3()
		
	def pesci_apri(self, widget, data=None):
		import files.pesci
		return files.pesci.win4()
	
	def piante_apri(self, widget, data=None):
		import files.piante
		return files.piante.win5()
	def vasca_apri(self, widget, data=None):
		import files.vasca
		return files.vasca.win6()
	def tips_apri(self, widget, data=None):
		import files.tips
		return files.tips.win7()
	def calendario_apri(self,widget, data=None):
		import files.calendario
		return files.calendario.win20()
	def inserisci_apri(self,widget, data=None):
		import files.inserisci
		return files.inserisci.win9()
	def informazioni_apri(self, widget, data=None):
		import files.informazioni
		return files.informazioni.win8()
		
		
	def main(self):
		gtk.main()

if __name__ == "__main__":
    menu = Gui()
    menu.main()
