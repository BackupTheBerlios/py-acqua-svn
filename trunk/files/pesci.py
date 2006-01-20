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
#from foto import *
#from pysqlite2 import dbapi2 as sqlite

class win4:
	def __init__(self):
		self.win = finestre.win(490, 350, "Py-Acqua Pesci", 5)
		# 400 560
		self.table = gtk.Table(2, 2, gtk.FALSE)
		self.win.add(self.table)
		
		self.notebook = gtk.Notebook()
		self.notebook.set_tab_pos(gtk.POS_TOP)
		self.table.attach(self.notebook, 0, 2, 0, 1)
		self.notebook.show()
		
#########Pagina Cancella########################################################
		self.label45 = gtk.Label("Cancella")
		self.fixed1 = gtk.Fixed()
		self.notebook.prepend_page(self.fixed1)
		self.label46 = gtk.Label("Id")
		self.fixed1.put(self.label46, 50, 13)
		self.spinbutton3 = gtk.SpinButton(None)
		self.spinbutton3.set_value(0)
		self.fixed1.put(self.spinbutton3, 150, 10)
		self.label47 = gtk.Label("Data")
		self.fixed1.put(self.label47, 50, 45)
		self.entry28 = gtk.Entry(30)
		self.fixed1.put(self.entry28, 150, 45)
		self.label48 = gtk.Label("Quantità")
		self.fixed1.put(self.label48, 50, 77)
		self.entry29 = gtk.Entry(30)
		self.fixed1.put(self.entry29, 150, 77)
		self.label49 = gtk.Label("Nome")
		self.fixed1.put(self.label49, 50, 109)
		self.entry30 = gtk.Entry(30)
		self.fixed1.put(self.entry30, 150, 109)
		#Label foto + immagine
		self.label51 = gtk.Label("Foto")
		self.fixed1.put(self.label51, 50, 141)
		#self.image = gtk.Image()
		#self.image.set_from_file("apple-red.png")
		#self.image.show()
		#self.fixed1.put(self.image, 150, 141)
		#Buttoni Cancella
		self.button15 = gtk.Button("Visualizza")
		#self.button15.connect("clicked", self.visuali_pesci)
		self.fixed1.put(self.button15, 75, 170)
		self.button16 = gtk.Button("Chiudi")
		self.button16.connect_object("clicked", gtk.Widget.destroy, self.win)
		self.fixed1.put(self.button16, 190, 170)
		self.button17 = gtk.Button("Modifica")
		#self.button17.connect("clicked", self.modifica_pesci)
		self.fixed1.put(self.button17, 75, 210)
		self.button18 = gtk.Button("Cancella")
		#self.button18.connect("clicked", self.cancella_nuovo_pesci)
		self.fixed1.put(self.button18, 190, 210)
		#Buttone Cancella Database
		self.label52 = gtk.Label("Cancella il database dei pesci")
		self.fixed1.put(self.label52, 70, 250)
		self.button19 = gtk.Button("Cancella")
		#self.button19.connect("clicked", self.cancella_attenzione_pesci)
		self.fixed1.put(self.button19, 133, 275)
################################################################################
#########Pagina Visualizza######################################################
		self.label50 = gtk.Label("Visualizza")
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
################################################################################
#########Pagina Inserisci#######################################################
		self.label53 = gtk.Label("Inserisci")
		self.fixed2 = gtk.Fixed()
		self.notebook.prepend_page(self.fixed2)
		self.label54 = gtk.Label("Id")
		self.fixed2.put(self.label54, 50, 13)
		self.spinbutton4 = gtk.SpinButton(None)
		self.spinbutton4.set_value(0)
		self.fixed2.put(self.spinbutton4, 150, 10)
		self.label55 = gtk.Label("Data")
		self.fixed2.put(self.label55, 50, 45)
		self.entry31 = gtk.Entry(30)
		self.fixed2.put(self.entry31, 150, 45)
		self.checkbutton1 = gtk.CheckButton("Data di oggi")
		#self.checkbutton1.connect("toggled", self.data, "Data di oggi")
		self.fixed2.put(self.checkbutton1, 225, 13)
		self.label56 = gtk.Label("Vasca")
		self.fixed2.put(self.label56, 50, 77)
		self.comboentry1 = gtk.ComboBoxEntry(model=None, column=-1)
		self.fixed2.put(self.comboentry1, 150, 77)
		self.label57 = gtk.Label("Quantità")
		self.fixed2.put(self.label57, 50, 109)
		self.entry32 = gtk.Entry(30)
		self.fixed2.put(self.entry32, 150, 109)
		self.label58 = gtk.Label("Nome")
		self.fixed2.put(self.label58, 50, 141)
		self.entry33 = gtk.Entry(30)
		self.fixed2.put(self.entry33, 150, 141)
		self.label59 = gtk.Label("Foto")
		self.fixed2.put(self.label59, 50, 173)
		self.entry34 = gtk.Entry(30)
		self.fixed2.put(self.entry34, 150, 173)
		self.button21 = gtk.Button("Apri ", gtk.STOCK_OPEN)
		self.button21.connect("clicked", self.apri)
		self.fixed2.put(self.button21, 320, 173)
		# Immagine
		self.image = gtk.Image()
		self.image.set_from_file("files/pesci.jpg")
		self.fixed2.put(self.image, 340, 30)
		self.button22 = gtk.Button("Inserisci")
		self.fixed2.put(self.button22, 60, 275)
		self.button23 = gtk.Button("Pulisci")
		self.fixed2.put(self.button23, 180, 275)
		self.button24 = gtk.Button("Chiudi")
		self.button24.connect_object("clicked", gtk.Widget.destroy, self.win)
		self.fixed2.put(self.button24, 280, 275)

################################################################################
		
		self.notebook.set_current_page(1)
		self.table.show()
		self.win.show_all()
		
	def apri(self, title):
		file = finestre.file()
