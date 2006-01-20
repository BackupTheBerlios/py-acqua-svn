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

class win9:
	def __init__(self):
		self.win = finestre.win(620, 610, "Py-Acqua Inserisci", 5)
		
		self.table = gtk.Table(2, 2, gtk.FALSE)
		self.win.add(self.table)
		
		self.notebook = gtk.Notebook()
		self.notebook.set_tab_pos(gtk.POS_TOP)
		self.table.attach(self.notebook, 0, 2, 0, 1)
		self.notebook.show()
		
		#Pagina pulizia filtro
		self.label16 = gtk.Label("Cancella")
		self.fixed1 = gtk.Fixed()
		self.notebook.prepend_page(self.fixed1)
		self.spinbutton2 = gtk.SpinButton(None)
		self.spinbutton2.set_value(0)
		self.fixed1.put(self.spinbutton2, 100, 13)
		self.label400 = gtk.Label("Data gg/mm/aaaa")
		self.fixed1.put(self.label400, 20, 50)
		self.entry400 = gtk.Entry(30)
		self.fixed1.put(self.entry400, 150, 50)
		self.label401 = gtk.Label("Ogni quanti giorni?")
		self.fixed1.put(self.label401, 20, 80)
		self.entry401 = gtk.Entry(30)
		self.fixed1.put(self.entry401, 150, 80)
		#pulsanti per pulizia filtro
		
		self.button400 = gtk.Button("Inserisci")
		#self.button4.connect("clicked", self.inserisci_test)
		self.fixed1.put(self.button400, 50, 150)
		
		self.button401 = gtk.Button("Pulisci")
		#self.button4.connect("clicked", self.inserisci_test)
		self.fixed1.put(self.button401, 150, 150)
		self.button402 = gtk.Button("Chiudi")
		#self.button4.connect("clicked", self.inserisci_test)
		self.fixed1.put(self.button402, 250, 150)
		
		
		
		
		#Pagina fertilizzante
		self.label17 = gtk.Label("Visualizza")
		#self.scrolled = gtk.ScrolledWindow()
		#self.scrolled.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
		self.fixed2 = gtk.Fixed()
		self.notebook.prepend_page(self.fixed2)
		self.spinbutton3 = gtk.SpinButton(None)
		self.spinbutton3.set_value(0)
		self.fixed2.put(self.spinbutton3, 100, 13)
		self.checkbutton1 = gtk.CheckButton("Data di oggi")
		#self.checkbutton1.connect("toggled", self.data, "Data di oggi")
		self.fixed2.put(self.checkbutton1, 200, 13)
		self.label300 = gtk.Label("Data gg/mm/aaaa")
		self.fixed2.put(self.label300, 20, 50)
		self.entry300 = gtk.Entry(30)
		self.fixed2.put(self.entry300, 170, 50)
		self.label301 = gtk.Label("Nome")
		self.fixed2.put(self.label301, 20, 80)
		self.entry301 = gtk.Entry(30)
		self.fixed2.put(self.entry301, 170, 80)
		self.label302 = gtk.Label("Quantita fertilizzante")
		self.fixed2.put(self.label302, 20, 120)
		self.entry302 = gtk.Entry(30)
		self.fixed2.put(self.entry302, 170, 120)
		self.label303 = gtk.Label("Ogni quanti giorni?")
		self.fixed2.put(self.label303, 20, 150)
		self.entry303 = gtk.Entry(30)
		self.fixed2.put(self.entry303, 170, 150)
		
		#pulsanti fertilizzanti
		
		self.button300 = gtk.Button("Inserisci")
		#self.button4.connect("clicked", self.inserisci_test)
		self.fixed2.put(self.button300, 50, 200)
		
		self.button301 = gtk.Button("Pulisci")
		#self.button4.connect("clicked", self.inserisci_test)
		self.fixed2.put(self.button301, 150, 200)
		self.button302 = gtk.Button("Chiudi")
		#self.button4.connect("clicked", self.inserisci_test)
		self.fixed2.put(self.button302, 250, 200)
		
		
		
		
		#Pagina Inserisci test
		self.label18 = gtk.Label("Inserisci")
		self.fixed3 = gtk.Fixed()
		self.notebook.prepend_page(self.fixed3)
		self.label19 = gtk.Label("Ph")
		self.fixed3.put(self.label19, 90, 13)
		self.label100 = gtk.Label("Alto")
		self.fixed3.put(self.label100, 20, 45)
		#self.spinbutton1 = gtk.SpinButton(None)
		#self.spinbutton1.set_value(0)
		#self.fixed3.put(self.spinbutton1, 210, 10)
		#self.checkbutton1 = gtk.CheckButton("Data di oggi")
		#self.checkbutton1.connect("toggled", self.data, "Data di oggi")
		#self.fixed3.put(self.checkbutton1, 280, 13)
		#self.label20 = gtk.Label("Inserisci la data gg/mm/aaaa")
		#self.fixed3.put(self.label20, 3, 45)
		self.entry4 = gtk.Entry(30)
		self.fixed3.put(self.entry4, 70, 40)
		self.label21 = gtk.Label("Basso")
		self.fixed3.put(self.label21, 20, 85)
		self.entry40 = gtk.Entry(30)
		self.fixed3.put(self.entry40, 70, 80)
		#self.comboentry1 = gtk.ComboBoxEntry(model=None, column=-1)
		#self.fixed3.put(self.comboentry1, 210, 77)
		self.label22 = gtk.Label("Kh")
		self.fixed3.put(self.label22, 90, 120)
		
		self.label23 = gtk.Label("Alto")
		self.fixed3.put(self.label23, 20, 160)
		self.entry7 = gtk.Entry(30)
		self.fixed3.put(self.entry7, 70, 155)
		self.label24 = gtk.Label("Basso")
		self.fixed3.put(self.label24, 20, 190)
		self.entry8 = gtk.Entry(30)
		self.fixed3.put(self.entry8, 70, 190)
		self.label25 = gtk.Label("Gh")
		self.fixed3.put(self.label25, 90, 220)
		self.entry9 = gtk.Entry(30)
		self.fixed3.put(self.entry9, 70, 250)
		self.label26 = gtk.Label("Alto")
		self.fixed3.put(self.label26, 20, 250)
		#self.entry10 = gtk.Entry(30)
		#self.fixed3.put(self.entry10, 70, 237)
		self.label27 = gtk.Label("Basso")
		self.fixed3.put(self.label27, 20, 280)
		self.entry11 = gtk.Entry(30)
		self.fixed3.put(self.entry11, 70, 280)
		self.label28 = gtk.Label("No2")
		self.fixed3.put(self.label28, 90, 310)
		#self.entry12 = gtk.Entry(30)
		#self.fixed3.put(self.entry12, 210, 301)
		self.label29 = gtk.Label("Alto")
		self.fixed3.put(self.label29, 20, 340)
		self.entry13 = gtk.Entry(30)
		self.fixed3.put(self.entry13, 70, 340)
		self.label30 = gtk.Label("Basso")
		self.fixed3.put(self.label30, 20, 365)
		self.entry14 = gtk.Entry(30)
		self.fixed3.put(self.entry14, 70, 365)
		self.label31 = gtk.Label("No3")
		self.fixed3.put(self.label31, 90, 397)
		self.label200 = gtk.Label("Alto")
		self.fixed3.put(self.label200, 20, 420)
		self.entry15 = gtk.Entry(30)
		self.fixed3.put(self.entry15, 70, 420)
		self.label201 = gtk.Label("Basso")
		self.fixed3.put(self.label201, 20, 450)
		self.entry200 = gtk.Entry(30)
		self.fixed3.put(self.entry200, 70, 450)
		self.label202 = gtk.Label("Conducibilità")
		self.fixed3.put(self.label202, 350, 13)
		self.label203 = gtk.Label("Alto")
		self.fixed3.put(self.label203, 280, 45)
		self.entry201 = gtk.Entry(30)
		self.fixed3.put(self.entry201, 340, 40)
		self.label204 = gtk.Label("Basso")
		self.fixed3.put(self.label204, 280, 85)
		self.entry202 = gtk.Entry(30)
		self.fixed3.put(self.entry202, 340, 80)
		self.label205 = gtk.Label("Ammoniaca")
		self.fixed3.put(self.label205, 350, 120)
		self.label206 = gtk.Label("Alto")
		self.fixed3.put(self.label206, 280, 160)
		self.entry203 = gtk.Entry(30)
		self.fixed3.put(self.entry203, 340, 155)
		self.label207 = gtk.Label("Basso")
		self.fixed3.put(self.label207, 280, 190)
		self.entry204 = gtk.Entry(30)
		self.fixed3.put(self.entry204, 340, 190)
		self.label208 = gtk.Label("Ferro")
		self.fixed3.put(self.label208, 350, 220)
		self.label209 = gtk.Label("Alto")
		self.fixed3.put(self.label209, 280, 250)
		self.entry205 = gtk.Entry(30)
		self.fixed3.put(self.entry205, 340, 250)
		self.label210 = gtk.Label("Basso")
		self.fixed3.put(self.label210, 280, 280)
		self.entry206 = gtk.Entry(30)
		self.fixed3.put(self.entry206, 340, 280)
		self.label208 = gtk.Label("Rame")
		self.fixed3.put(self.label208, 350, 310)
		self.label209 = gtk.Label("Alto")
		self.fixed3.put(self.label209, 280, 340)
		self.entry205 = gtk.Entry(30)
		self.fixed3.put(self.entry205, 340, 340)
		self.label210 = gtk.Label("Basso")
		self.fixed3.put(self.label210, 280, 365)
		self.entry206 = gtk.Entry(30)
		self.fixed3.put(self.entry206, 340, 365)
		
		self.label208 = gtk.Label("Fosfati")
		self.fixed3.put(self.label208, 350, 397)
		self.label209 = gtk.Label("Alto")
		self.fixed3.put(self.label209, 280, 420)
		self.entry205 = gtk.Entry(30)
		self.fixed3.put(self.entry205, 340, 420)
		self.label210 = gtk.Label("Basso")
		self.fixed3.put(self.label210, 280, 450)
		self.entry206 = gtk.Entry(30)
		self.fixed3.put(self.entry206, 340, 450)
		#Bottoni
		self.button4 = gtk.Button("Inserisci")
		#self.button4.connect("clicked", self.inserisci_test)
		self.fixed3.put(self.button4, 100, 550)
		self.button5 = gtk.Button("Pulisci")
		self.button5.connect("clicked", self.pulisci_test)
		self.fixed3.put(self.button5, 300, 550)
		self.button6 = gtk.Button("Chiudi")
		self.button6.connect_object("clicked", gtk.Widget.destroy, self.win)
		self.fixed3.put(self.button6, 500, 550)
		
		self.notebook.set_current_page(1)
		
		self.table.show()
		self.win.show_all()
		
##########Funzioni per Inserisci################################################
		
	

	
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
