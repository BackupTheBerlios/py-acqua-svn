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
from data import *
import finestre
#from pysqlite2 import dbapi2 as sqlite
#from sqlite import *
#data1 = data()

class win3:
	def __init__(self):
		self.win = finestre.win(420, 610, "Py-Acqua Test", 5)
		
		self.table = gtk.Table(2, 2, gtk.FALSE)
		self.win.add(self.table)
		
		self.notebook = gtk.Notebook()
		self.notebook.set_tab_pos(gtk.POS_TOP)
		self.table.attach(self.notebook, 0, 2, 0, 1)
		self.notebook.show()
		
		#Pagina Cancella
		self.label16 = gtk.Label("Cancella")
		self.fixed1 = gtk.Fixed()
		self.notebook.prepend_page(self.fixed1)
		self.spinbutton2 = gtk.SpinButton(None)
		self.spinbutton2.set_value(0)
		self.fixed1.put(self.spinbutton2, 250, 13)
		self.label32 = gtk.Label("Id")
		self.fixed1.put(self.label32, 90, 45)
		self.entry17 = gtk.Entry(30)
		self.fixed1.put(self.entry17, 210, 45)
		self.label33 = gtk.Label("Data")
		self.fixed1.put(self.label33, 90, 77)
		self.entry18 = gtk.Entry(30)
		self.fixed1.put(self.entry18, 210, 77)
		self.label34 = gtk.Label("Ph")
		self.fixed1.put(self.label34, 90, 109)
		self.entry19 = gtk.Entry(30)
		self.fixed1.put(self.entry19, 210, 109)
		self.label35 = gtk.Label("kh")
		self.fixed1.put(self.label35, 90, 141)
		self.entry20 = gtk.Entry(30)
		self.fixed1.put(self.entry20, 210, 141)
		self.label36 = gtk.Label("Gh")
		self.fixed1.put(self.label36, 90, 173)
		self.entry21 = gtk.Entry(30)
		self.fixed1.put(self.entry21, 210, 173)
		self.label37 = gtk.Label("No2")
		self.fixed1.put(self.label37, 90, 205)
		self.entry22 = gtk.Entry(30)
		self.fixed1.put(self.entry22, 210, 205)
		self.label38 = gtk.Label("No3")
		self.fixed1.put(self.label38, 90, 237)
		self.entry23 = gtk.Entry(30)
		self.fixed1.put(self.entry23, 210, 237)
		self.label39 = gtk.Label("Conducibilita'")
		self.fixed1.put(self.label39, 90, 269)
		self.entry24 = gtk.Entry(30)
		self.fixed1.put(self.entry24, 210, 269)
		self.label40 = gtk.Label("Ammoniaca")
		self.fixed1.put(self.label40, 90, 301)
		self.entry25 = gtk.Entry(30)
		self.fixed1.put(self.entry25, 210, 301)
		self.label41 = gtk.Label("Ferro")
		self.fixed1.put(self.label41, 90, 333)
		self.entry26 = gtk.Entry(30)
		self.fixed1.put(self.entry26, 210, 333)
		self.label42 = gtk.Label("Rame")
		self.fixed1.put(self.label42, 90, 365)
		self.entry27 = gtk.Entry(30)
		self.fixed1.put(self.entry27, 210, 365)
		self.label43 = gtk.Label("Fosfati")
		self.fixed1.put(self.label43, 90, 397)
		self.entry28 = gtk.Entry(30)
		self.fixed1.put(self.entry28, 210, 397)
		#Bottoni
		self.button10 = gtk.Button("Visualizza")
		self.button10.connect("clicked", self.visualizza_test)
		self.fixed1.put(self.button10, 70, 440)
		self.button11 = gtk.Button("Modifica")
		self.button11.connect("clicked", self.modifica_test)
		self.fixed1.put(self.button11, 70, 475)
		self.button12 = gtk.Button("Chiudi")
		self.button12.connect_object("clicked", gtk.Widget.destroy, self.win)
		self.fixed1.put(self.button12, 270, 440)
		self.button13 = gtk.Button("Cancella")
		self.button13.connect("clicked", self.cancella_nuovo_test)
		self.fixed1.put(self.button13, 270, 475)
		#Cancella Database
		self.label44 = gtk.Label("Cancella tutto il database dei test")
		self.fixed1.put(self.label44, 100, 515)
		self.button14 = gtk.Button("Cancella")
		self.button14.connect("clicked", self.cancella_attenzione_test)
		self.fixed1.put(self.button14, 170, 540)
		
		#Pagina Visualizza
		self.label17 = gtk.Label("Visualizza")
		self.scrolled = gtk.ScrolledWindow()
		self.scrolled.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
		self.notebook.prepend_page(self.scrolled)
		self.listore = gtk.ListStore(int, str, str, str, str, str, str, str, str, str, str, str, str)
		self.treeview1 = gtk.TreeView(self.listore)
		self.tvcolumn = gtk.TreeViewColumn('Colonna1')
		self.tvcolumn1 = gtk.TreeViewColumn('Colonna2')
		self.treeview1.append_column(self.tvcolumn)
		self.treeview1.append_column(self.tvcolumn1)
		self.scrolled.add_with_viewport(self.treeview1)
		
		#Pagina Inserisci
		self.label18 = gtk.Label("Inserisci")
		self.fixed3 = gtk.Fixed()
		self.notebook.prepend_page(self.fixed3)
		self.label19 = gtk.Label("Id")
		self.fixed3.put(self.label19, 90, 13)
		self.spinbutton1 = gtk.SpinButton(None)
		self.spinbutton1.set_value(0)
		self.fixed3.put(self.spinbutton1, 210, 10)
		self.checkbutton1 = gtk.CheckButton("Data di oggi")
		#self.checkbutton1.connect("toggled", self.data, "Data di oggi")
		self.fixed3.put(self.checkbutton1, 280, 13)
		self.label20 = gtk.Label("Inserisci la data gg/mm/aaaa")
		self.fixed3.put(self.label20, 3, 45)
		self.entry4 = gtk.Entry(30)
		self.fixed3.put(self.entry4, 210, 40)
		self.label21 = gtk.Label("Vasca")
		self.fixed3.put(self.label21, 90, 77)
		self.comboentry1 = gtk.ComboBoxEntry(model=None, column=-1)
		self.fixed3.put(self.comboentry1, 210, 77)
		self.label22 = gtk.Label("Ph")
		self.fixed3.put(self.label22, 90, 109)
		self.entry6 = gtk.Entry(30)
		self.fixed3.put(self.entry6, 210, 109)
		self.label23 = gtk.Label("kh")
		self.fixed3.put(self.label23, 90, 141)
		self.entry7 = gtk.Entry(30)
		self.fixed3.put(self.entry7, 210, 141)
		self.label24 = gtk.Label("Gh")
		self.fixed3.put(self.label24, 90, 173)
		self.entry8 = gtk.Entry(30)
		self.fixed3.put(self.entry8, 210, 173)
		self.label25 = gtk.Label("No2")
		self.fixed3.put(self.label25, 90, 205)
		self.entry9 = gtk.Entry(30)
		self.fixed3.put(self.entry9, 210, 205)
		self.label26 = gtk.Label("No3")
		self.fixed3.put(self.label26, 90, 237)
		self.entry10 = gtk.Entry(30)
		self.fixed3.put(self.entry10, 210, 237)
		self.label27 = gtk.Label("Conducibilita'")
		self.fixed3.put(self.label27, 90, 269)
		self.entry11 = gtk.Entry(30)
		self.fixed3.put(self.entry11, 210, 269)
		self.label28 = gtk.Label("Ammoniaca")
		self.fixed3.put(self.label28, 90, 301)
		self.entry12 = gtk.Entry(30)
		self.fixed3.put(self.entry12, 210, 301)
		self.label29 = gtk.Label("Ferro")
		self.fixed3.put(self.label29, 90, 333)
		self.entry13 = gtk.Entry(30)
		self.fixed3.put(self.entry13, 210, 333)
		self.label30 = gtk.Label("Rame")
		self.fixed3.put(self.label30, 90, 365)
		self.entry14 = gtk.Entry(30)
		self.fixed3.put(self.entry14, 210, 365)
		self.label31 = gtk.Label("Fosfati")
		self.fixed3.put(self.label31, 90, 397)
		self.entry15 = gtk.Entry(30)
		self.fixed3.put(self.entry15, 210, 397)
		#Bottoni
		self.button4 = gtk.Button("Inserisci")
		self.button4.connect("clicked", self.inserisci_test)
		self.fixed3.put(self.button4, 70, 440)
		self.button5 = gtk.Button("Pulisci")
		self.button5.connect("clicked", self.pulisci_test)
		self.fixed3.put(self.button5, 175, 440)
		self.button6 = gtk.Button("Chiudi")
		self.button6.connect_object("clicked", gtk.Widget.destroy, self.win)
		self.fixed3.put(self.button6, 270, 440)
		
		self.notebook.set_current_page(1)
		
		self.table.show()
		self.win.show_all()
		
##########Funzioni per Inserisci################################################
		
	def inserisci_test(self, obj):
		id = self.spinbutton1.get_value()
		data = self.entry4.get_text()
		campi = data.split('/')
		
		if len(campi)<>3:
			#errore()
			print "errore"
		else:
			print ""
					
		gg,mm,aa = campi					
		
		if (1 <= int(gg) <=31) and (1 <= int(mm) <= 12) and (int(aa) >= 1900):
			print ""
		else:
			#errore()
			print "errore"
		
		self.ph = float(self.entry6.get_text())
		self.kh = float(self.entry7.get_text())
		self.gh = float(self.entry8.get_text())
		self.no = float(self.entry9.get_text())
		self.noo = float(self.entry10.get_text())
		self.con = float(self.entry11.get_text())
		self.am = float(self.entry12.get_text())
		self.fe = float(self.entry13.get_text())
		self.ra = float(self.entry14.get_text())
		self.fo = float(self.entry15.get_text())
					
		connessione = sqlite.connect("Data/db")
		cursore = connessione.cursor()
		cursore.execute("insert into test values (?,?,?,?,?,?,?,?,?,?,?,?)",(id, data, ph, kh, gh, no, noo, con, am, fe, ra, fo))
		connessione.commit()
		#Finestra dialog con dati inseriti
		window = finestre("Dati inseriti", "I dati sono stati inseriti con successo  ", "Chiudi")		
		
		self.spinbutton1.set_value(id+1)	
		
	def inserisci_2(self, obj):
		connessione=sqlite.connect("Data/db")
		cursore=connessione.cursor()
		cursore.execute("select * from test")
		for x in cursore.fetchall():
			self.spinbutton1.set_value(x[0]+1)
	
		self.menu_test_nomi()
	
	def pulisci_test(self, obj):
		self.entry6.set_text("")
		self.entry7.set_text("")
		self.entry8.set_text("")
		self.entry9.set_text("")
		self.entry10.set_text("")
		self.entry11.set_text("")
		self.entry12.set_text("")
		self.entry13.set_text("")
		self.entry14.set_text("")
		self.entry15.set_text("")
		
	def data(self, widget, data=None):
		data1.giorno()
		self.entry4.set_text(data1.wine)
		
################################################################################
#########Funzioni per Visualizza################################################

	def funziona_test(self, obj, notebookpage, page_number):
		if page_number == 0:
			print ""
		elif page_number == 1: 
			print ""
			self.tree_test()

	
		
	def tree_test(self):
		self.renderer = gtk.CellRendererText()
		
		i = 0
		for c in ['Id', 'Data', 'Vasca', 'Ph', 'Kh', 'Gh', 'No2', 'No3', 'Conducibilità', 'Ammoniaca', 'Ferro', 'Rame', 'Fosfati']:
			self.column = gtk.TreeViewColumn(c, renderer, text=i)
			i += 1
			self.column.set_sort_column_id(i)
			self.column.set_clickable(True)
			self.column.set_resizable(True)
			self.listview1.append_column(column)
		
	
		connessione=sqlite.connect("Data/db")
		cursore=connessione.cursor()
		cursore.execute("select * from test")
		for y in cursore.fetchall():
		
			connessione=sqlite.connect("Data/db")
			cursore=connessione.cursor()
			cursore.execute("select * from vasca")
			for a in cursore.fetchall():
				self.listore.append([y[0], y[1], a[3], y[2], y[3], y[4], y[5], y[6], y[7], y[8], y[9], y[10], y[11]])
################################################################################		
#########Funzioni per Cancella##################################################
	def visualizza_test(self, obj):
		
		cercatest = self.spinbutton2.get_value()
		connessione=sqlite.connect("Data/db")
		cursore=connessione.cursor()
		cursore.execute("select * from test")
		for a in cursore.fetchall(): 
		
			if (a[0]==cercatest):
				self.entry32.set_text(str(a[0]))
				self.entry33.set_text(str(a[1]))
				self.entry34.set_text(str(a[2]))
				self.entry35.set_text(str(a[3]))
				self.entry36.set_text(str(a[4]))
				self.entry37.set_text(str(a[5]))
				self.entry38.set_text(str(a[6]))
				self.entry39.set_text(str(a[7]))
				self.entry40.set_text(str(a[8]))
				self.entry41.set_text(str(a[9]))
				self.entry42.set_text(str(a[10]))
				self.entry43.set_text(str(a[11]))
		
			else:
				#Dire che c'è un errore e di riprovare (Finestra Dialog)
				print ""
			
	def modifica_test(self, obj):
		id = self.entry32.get_text()
		data = self.entry33.get_text()
		ph = self.entry34.get_text()
		kh = self.entry35.get_text()
		gh = self.entry36.get_text()
		no = self.entry37.get_text()
		noo = self.entry38.get_text()
		con = self.entry39.get_text()
		am = self.entry40.get_text()
		fe = self.entry41.get_text()
		ra = self.entry42.get_text()
		fo = self.entry43.get_text()
	
		connessione=sqlite.connect("Data/db")
		cursore=connessione.cursor()
		cursore.execute("update test set ph= %(ph)s, kh = %(kh)s, gh = %(gh)s, no = %(no)s, noo = %(noo)s, con = %(con)s, amm = %(am)s, fe = %(fe)s, ra = %(ra)s, fo = %(fo)s" %vars())
		connessione.commit()

	def cancella_nuovo_test(self, obj):
		id1 = self.spinbutton2.get_value()
		connessione=sqlite.connect("db")
		cursore=connessione.cursor()
		cursore.execute("delete from test where id= %(id1)s" %vars())
		connessione.commit()
		self.spinbutton2.set_value(id1-1)
	
	def cancella_attenzione_test(self, obj):
		#Visualizza finestra dialog di conferma
		connessione=sqlite.connect("Data/db")
		cursore=connessione.cursor()
		cursore.execute("delete from test")
		connessione.commit()
		self.spinbutton2.set_value(0)
		#Visualizzare finestra di cancellazione avvenuta
	
		def menu_test_nomi():
			data = []
			connessione=sqlite.connect("Data/db")
			cursore=connessione.cursor()
			cursore.execute("select * from vasca")
			for a in cursore.fetchall():
				data.append(a[3])
				
			self.store = gtk.ListStore(gobject.TYPE_STRING)
			for d in data: store.append([d])
			
			self.comboentry1.set_model(self.store)
			self.comboentry1.set_text_column(0)
