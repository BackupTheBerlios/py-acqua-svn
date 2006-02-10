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

class Test(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		
		self.set_title("Test")
		#self.set_size_request(420, 610)
		
		mbox = gtk.VBox()
		self.add(mbox)
		
		self.notebook = gtk.Notebook()
		mbox.pack_start(self.notebook)
		
		# Pagina Inserisci

		tbl = gtk.Table(12, 3)
		
		attach = lambda x, y, z: tbl.attach(x, 0, 1, y, z)
		
		attach(self.new_label('Data: (gg/mm/aa)'), 0, 1)
		attach(self.new_label('Vasca:'), 1, 2)
		attach(self.new_label('Ph:'), 2, 3)
		attach(self.new_label('Kh:'), 3, 4)
		attach(self.new_label('Gh:'), 4, 5)
		attach(self.new_label('No2:'), 5, 6)
		attach(self.new_label('No3:'), 6, 7)
		attach(self.new_label('Conducibilita\':'), 7, 8)
		attach(self.new_label('Ammoniaca:'), 8, 9)
		attach(self.new_label('Ferro:'), 9, 10)
		attach(self.new_label('Rame:'), 10, 11)
		attach(self.new_label('Fosfati:'), 11, 12)

		def make_inst(num):
			a = list()
			for i in range(num):
				a.append(gtk.Entry())
			return a
		
		self.e_data, self.e_vasca = make_inst(2)
		self.e_ph, self.e_kh, self.e_gh = make_inst(3)
		self.e_no2, self.e_no3, self.e_cond = make_inst(3)
		self.e_ammo, self.e_fe, self.e_rame, self.e_fosf = make_inst(4)
		
		attach = lambda x, y, z: tbl.attach(x, 1, 2, y, z)
		
		attach(self.e_data, 0, 1)
		attach(self.e_vasca, 1, 2)
		attach(self.e_ph, 2, 3)
		attach(self.e_kh, 3, 4)
		attach(self.e_gh, 4, 5)
		attach(self.e_no2, 5, 6)
		attach(self.e_no3, 6, 7)
		attach(self.e_cond, 7, 8)
		attach(self.e_ammo, 8, 9)
		attach(self.e_fe, 9, 10)
		attach(self.e_rame, 10, 11)
		attach(self.e_fosf, 11, 12)

		self.notebook.append_page(tbl, gtk.Label('Inserisci'))

		self.show_all()
	def new_label(self, txt, bold=True):
		lbl = gtk.Label()
		
		lbl.set_use_markup(True)
		lbl.set_label('<b>' + txt + '</b>')
		lbl.set_alignment(0.0, 0.5)
		
		return lbl
		
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
