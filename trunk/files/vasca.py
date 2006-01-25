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
from finestre import *
import gobject
from pysqlite2 import dbapi2 as sqlite
#from sqlite import *
#data1 = data()
as = "Data/db"
class win6:
	def __init__(self):
		
		self.win = finestre.win(450, 600, "Py-Acqua Vasche", 5)
		
		self.table = gtk.Table(2, 2, gtk.FALSE)
		self.win.add(self.table)
		
		self.notebook = gtk.Notebook()
		self.notebook.set_tab_pos(gtk.POS_TOP)
		self.table.attach(self.notebook, 0, 2, 0, 1)
		self.notebook.connect("switch-page", self.funziona_vasca)
		self.notebook.show()
		
		#Pagina Cancella
		
		self.label16 = gtk.Label("Cancella")
		self.fixed1 = gtk.Fixed()
		self.notebook.prepend_page(self.fixed1, self.label16)
		
		
		
		self.spinbutton2 = gtk.SpinButton(None)
		self.spinbutton2.set_value(0)
		self.fixed1.put(self.spinbutton2, 250, 13)
		self.label32 = gtk.Label("Id")
		self.fixed1.put(self.label32, 90, 45)
		self.entry17 = gtk.Entry(30)
		self.fixed1.put(self.entry17, 210, 45)
		self.label33 = gtk.Label("Nome")
		self.fixed1.put(self.label33, 90, 77)
		self.entry18 = gtk.Entry(30)
		self.fixed1.put(self.entry18, 210, 77)
		self.label34 = gtk.Label("Tipo di acquario")
		self.fixed1.put(self.label34, 90, 109)
		self.entry19 = gtk.Entry(30)
		self.fixed1.put(self.entry19, 210, 109)
		self.label35 = gtk.Label("Tipo di filtro")
		self.fixed1.put(self.label35, 90, 141)
		self.entry20 = gtk.Entry(30)
		self.fixed1.put(self.entry20, 210, 141)
		self.label36 = gtk.Label("Tipo di C02")
		self.fixed1.put(self.label36, 90, 173)
		self.entry21 = gtk.Entry(30)
		self.fixed1.put(self.entry21, 210, 173)
		self.label37 = gtk.Label("Illuminazione")
		self.fixed1.put(self.label37, 90, 205)
		self.entry22 = gtk.Entry(30)
		self.fixed1.put(self.entry22, 210, 205)
		
		#Bottoni
		
		self.button10 = gtk.Button("Visualizza")
		self.button10.connect("clicked", self.visualizza_vasca)
		self.fixed1.put(self.button10, 70, 440)
		self.button11 = gtk.Button("Modifica")
		self.button11.connect("clicked", self.modifica_vasca)
		self.fixed1.put(self.button11, 70, 475)
		self.button12 = gtk.Button("Chiudi")
		self.button12.connect_object("clicked", gtk.Widget.destroy, self.win)
		self.fixed1.put(self.button12, 270, 440)
		self.button13 = gtk.Button("Cancella")
		self.button13.connect("clicked", self.cancella_nuovo_vasca)
		self.fixed1.put(self.button13, 270, 475)
		
		#Cancella Database
		
		self.label44 = gtk.Label("Cancella tutto il database dei test")
		self.fixed1.put(self.label44, 100, 515)
		self.button14 = gtk.Button("Cancella")
		self.button14.connect("clicked", self.cancella_attenzione_vasca)
		self.fixed1.put(self.button14, 170, 540)
		
		#Pagina Visualizza
		
		self.label17 = gtk.Label("Visualizza")
		self.scrolled = gtk.ScrolledWindow()
		self.scrolled.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
		
		self.notebook.prepend_page(self.scrolled, self.label17)
		
		
		self.listore = gtk.ListStore(int, str, str, str, str, str, str, str, str)
		self.treeview1 = gtk.TreeView(self.listore)
		self.scrolled.add_with_viewport(self.treeview1)
		
		#Pagina Inserisci
		
		self.label18 = gtk.Label("Inserisci")
		self.fixed3 = gtk.Fixed()
		self.notebook.prepend_page(self.fixed3, self.label18)
		self.label19 = gtk.Label("Id")
		self.fixed3.put(self.label19, 90, 13)
		
		####per spinbutton#####
		
		self.spinbutton1 = gtk.SpinButton(climb_rate=0, digits=0)
		self.spinbutton1.set_digits(0)
		self.spinbutton1.set_wrap(True)
		self.spinbutton1.set_range(0, 100)
		#self.spinbutton1.set_value(13)
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
		
		###per il comboentry1#####
		
		store = gtk.ListStore(gobject.TYPE_STRING)
		store.append (["Dolce"])
		store.append (["Dolce Tropicale"])
		store.append (["Marino"])
		store.append (["Marino Tropicale"])
		
		self.comboentry1 = gtk.ComboBoxEntry(model=None, column=-1)
		self.comboentry1.set_model(store)
		self.comboentry1.set_text_column(0)
		
		self.fixed3.put(self.comboentry1, 210, 77)
		self.label22 = gtk.Label("Nome")
		
		
		
		self.fixed3.put(self.label22, 90, 109)
		self.entry6 = gtk.Entry(30)
		self.fixed3.put(self.entry6, 210, 109)
		self.label23 = gtk.Label("Tipo di acquario")
		self.fixed3.put(self.label23, 90, 141)
		self.entry7 = gtk.Entry(30)
		self.fixed3.put(self.entry7, 210, 141)
		self.label24 = gtk.Label("Tipo di filtro")
		self.fixed3.put(self.label24, 90, 173)
		self.entry8 = gtk.Entry(30)
		self.fixed3.put(self.entry8, 210, 173)
		self.label25 = gtk.Label("Impianto Co2")
		self.fixed3.put(self.label25, 90, 205)
		self.entry9 = gtk.Entry(30)
		self.fixed3.put(self.entry9, 210, 205)
		self.label26 = gtk.Label("Illuminazione")
		self.fixed3.put(self.label26, 90, 237)
		self.entry10 = gtk.Entry(30)
		self.fixed3.put(self.entry10, 210, 237)
		self.label27 = gtk.Label("Foto")
		self.fixed3.put(self.label27, 90, 269)
		self.entry11 = gtk.Entry(30)
		self.fixed3.put(self.entry11, 210, 269)
		
		#Bottoni
		self.button4 = gtk.Button("Inserisci")
		self.button4.connect("clicked", self.inserisci_vasca)
		self.fixed3.put(self.button4, 70, 440)
		self.button5 = gtk.Button("Pulisci")
		self.button5.connect("clicked", self.pulisci_vasca)
		self.fixed3.put(self.button5, 175, 440)
		self.button6 = gtk.Button("Chiudi")
		self.button6.connect_object("clicked", gtk.Widget.destroy, self.win)
		self.fixed3.put(self.button6, 270, 440)
		
		self.button21 = gtk.Button("Apri ", gtk.STOCK_OPEN)
		self.button21.connect("clicked", self.apri)
		self.fixed3.put(self.button21, 380, 269)
		
		self.notebook.set_current_page(1)
		
		self.table.show()
		self.win.show_all()
		
	def apri(self, title):
		file = finestre.file()
		
##########Funzioni per Inserisci################################################
		
	def inserisci_vasca(self, obj):
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
		vasca = self.comboentry1.get_children()[0].get_text()
		nome = self.entry6.get_text()
		tipo = self.entry7.get_text()
		filtro = self.entry8.get_text()
		co2 = self.entry9.get_text()
		illumi = self.entry10.get_text()
		foto = self.entry11.get_text()
		
		
		
		
					
		connessione = sqlite.connect(as)
		cursore = connessione.cursor()
		cursore.execute("insert into vasca values (?,?,?,?,?,?,?,?,?)",(id, vasca, data, nome, tipo, filtro, co2, illumi, foto))
		connessione.commit()
		#Finestra dialog con dati inseriti
		#window = finestre("Dati inseriti", "I dati sono stati inseriti con successo  ", "Chiudi")		
		
		self.spinbutton1.set_value(id+1)	
		
	def inserisci_2(self, obj):
		connessione=sqlite.connect(as)
		cursore=connessione.cursor()
		cursore.execute("select * from vasca")
		for x in cursore.fetchall():
			print x[0]
			self.spinbutton1.set_value(x[0]+1)
			
			self.menu_vasca_nomi()
	
	def pulisci_vasca(self, obj):
		self.entry6.set_text("")
		self.entry7.set_text("")
		self.entry8.set_text("")
		self.entry9.set_text("")
		self.entry10.set_text("")
		self.entry11.set_text("")
		self.entry4.set_text("")
		
		
		
		
	def data(self, widget, data=None):
		data1.giorno()
		self.entry4.set_text(data1.wine)
		
################################################################################
#########Funzioni per Visualizza################################################

	def funziona_vasca(self, obj, notebookpage, page_number):
		if page_number == 0:
			print ""
		elif page_number == 1: 
			
			self.tree_vasca()

	
		
	def tree_vasca(self):
		
		
		renderer = gtk.CellRendererText()
		
		i = 0
		for c in ['Id', 'Vasca', 'Data', 'Nome', 'Tipo Acquario', 'Tipo Filtro', 'Impianto Co2', 'Illuminazione']:
			self.column = gtk.TreeViewColumn(c, renderer, text=i)
			i += 1
			self.column.set_sort_column_id(i)
			self.column.set_clickable(True)
			self.column.set_resizable(True)
			self.treeview1.append_column(self.column)
		
		
		connessione=sqlite.connect(as)
		cursore=connessione.cursor()
		cursore.execute("select * from vasca")
		for y in cursore.fetchall():
			self.listore.append([y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[8]])
			
################################################################################
#########Funzioni per Cancella##################################################

	def visualizza_vasca(self, obj):
		
		cercatest = self.spinbutton2.get_value()
		connessione=sqlite.connect(as)
		cursore=connessione.cursor()
		cursore.execute("select * from vasca")
		for a in cursore.fetchall(): 
		
			if (a[0]==cercatest):
				self.entry17.set_text(str(a[0]))
				self.entry18.set_text(str(a[3]))
				self.entry19.set_text(str(a[4]))
				self.entry20.set_text(str(a[5]))
				self.entry21.set_text(str(a[6]))
				self.entry22.set_text(str(a[7]))
				
		
			else:
				#Dire che c'è un errore e di riprovare (Finestra Dialog)
				print ""
			
	def modifica_vasca(self, obj):
		id = self.entry17.get_text()
		nome = self.entry18.get_text()
		tipo = self.entry19.get_text()
		filtro = self.entry20.get_text()
		co2 = self.entry21.get_text()
		illumi = self.entry22.get_text()
		
	
		connessione=sqlite.connect(as)
		cursore=connessione.cursor()
		cursore.execute("update vasca set a= %('nome')s, aa = %('tipo')s, b = %('filtro')s, c = %('co2')s, d = %('illumi')s" %vars())
		connessione.commit()

	def cancella_nuovo_vasca(self, obj):
		id1 = self.spinbutton2.get_value()
		connessione=sqlite.connect(as)
		cursore=connessione.cursor()
		cursore.execute("delete from vasca where id= %(id1)s" %vars())
		connessione.commit()
		self.spinbutton2.set_value(id1-1)
	
	def cancella_attenzione_vasca(self, obj):
		#Visualizza finestra dialog di conferma
		connessione=sqlite.connect(as)
		cursore=connessione.cursor()
		cursore.execute("delete from vasca")
		connessione.commit()
		self.spinbutton2.set_value(0)
		
		#Visualizzare finestra di cancellazione avvenuta
	
		def menu_vasca_nomi():
			data = []
			connessione=sqlite.connect(as)
			cursore=connessione.cursor()
			cursore.execute("select * from vasca")
			for a in cursore.fetchall():
				data.append(a[3])
				
			self.store = gtk.ListStore(gobject.TYPE_STRING)
			for d in data: store.append([d])
			
			self.comboentry1.set_model(self.store)
			self.comboentry1.set_text_column(0)
