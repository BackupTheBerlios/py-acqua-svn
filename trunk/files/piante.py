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

class win5:
	def __init__(self):
		self.win = finestre.win(490, 350, "py-Acqua Piante", 5)
		
		self.table = gtk.Table(2, 2, gtk.FALSE)
		self.win.add(self.table)
		
		self.notebook = gtk.Notebook()
		self.notebook.set_tab_pos(gtk.POS_TOP)
		self.table.attach(self.notebook, 0, 2, 0, 1)
		self.notebook.show()
		
#########Pagina Cancella########################################################
		self.label70 = gtk.Label("Cancella")
		self.fixed1 = gtk.Fixed()
		self.notebook.prepend_page(self.fixed1)
		self.label71 = gtk.Label("Id")
		self.fixed1.put(self.label71, 50, 13)
		self.spinbutton3 = gtk.SpinButton(None)
		self.spinbutton3.set_value(0)
		self.fixed1.put(self.spinbutton3, 150, 10)
		self.label72 = gtk.Label("Data")
		self.fixed1.put(self.label72, 50, 45)
		self.entry37 = gtk.Entry(30)
		self.fixed1.put(self.entry37, 150, 45)
		self.label73 = gtk.Label("Quantità")
		self.fixed1.put(self.label73, 50, 77)
		self.entry38 = gtk.Entry(30)
		self.fixed1.put(self.entry38, 150, 77)
		self.label74 = gtk.Label("Nome")
		self.fixed1.put(self.label74, 50, 109)
		self.entry39 = gtk.Entry(30)
		self.fixed1.put(self.entry39, 150, 109)
		#Label foto + immagine
		self.label75 = gtk.Label("Foto")
		self.fixed1.put(self.label75, 50, 141)
		#self.image = gtk.Image()
		#self.image.set_from_file("apple-red.png")
		#self.image.show()
		#self.fixed1.put(self.image, 150, 141)
		#Buttoni Cancella
		self.button27 = gtk.Button("Visualizza")
		#self.button27.connect("clicked", self.visuali_pesci)
		self.fixed1.put(self.button27, 75, 170)
		self.button28 = gtk.Button("Chiudi")
		self.button28.connect_object("clicked", gtk.Widget.destroy, self.win)
		#self.button28.connect("clicked", self.destroy)
		self.fixed1.put(self.button28, 190, 170)
		self.button29 = gtk.Button("Modifica")
		#self.button29.connect("clicked", self.modifica_pesci)
		self.fixed1.put(self.button29, 75, 210)
		self.button30 = gtk.Button("Cancella")
		#self.button30.connect("clicked", self.cancella_nuovo_pesci)
		self.fixed1.put(self.button30, 190, 210)
		#Buttone Cancella Database
		self.label76 = gtk.Label("Cancella il database delle piante")
		self.fixed1.put(self.label76, 70, 250)
		self.button31 = gtk.Button("Cancella")
		#self.button31.connect("clicked", self.cancella_attenzione_pesci)
		self.fixed1.put(self.button31, 133, 275)
################################################################################
#########Pagina Visualizza######################################################
		self.label77 = gtk.Label("Visualizza")
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
		self.label78 = gtk.Label("Inserisci")
		self.fixed2 = gtk.Fixed()
		self.notebook.prepend_page(self.fixed2)
		self.label79 = gtk.Label("Id")
		self.fixed2.put(self.label79, 50, 13)
		self.spinbutton4 = gtk.SpinButton(None)
		self.spinbutton4.set_value(0)
		self.fixed2.put(self.spinbutton4, 150, 10)
		self.label80 = gtk.Label("Data")
		self.fixed2.put(self.label80, 50, 45)
		self.entry40 = gtk.Entry(30)
		self.fixed2.put(self.entry40, 150, 45)
		self.checkbutton1 = gtk.CheckButton("Data di oggi")
		#self.checkbutton1.connect("toggled", self.data, "Data di oggi")
		self.fixed2.put(self.checkbutton1, 225, 13)
		self.label82 = gtk.Label("Vasca")
		self.fixed2.put(self.label82, 50, 77)
		self.comboentry1 = gtk.ComboBoxEntry(model=None, column=-1)
		self.fixed2.put(self.comboentry1, 150, 77)
		self.label83 = gtk.Label("Quantità")
		self.fixed2.put(self.label83, 50, 109)
		self.entry41 = gtk.Entry(30)
		self.fixed2.put(self.entry41, 150, 109)
		self.label84 = gtk.Label("Nome")
		self.fixed2.put(self.label84, 50, 141)
		self.entry42 = gtk.Entry(30)
		self.fixed2.put(self.entry42, 150, 141)
		self.label85 = gtk.Label("Foto")
		self.fixed2.put(self.label85, 50, 173)
		self.entry43 = gtk.Entry(30)
		self.fixed2.put(self.entry43, 150, 173)
		self.button32 = gtk.Button("Apri ", gtk.STOCK_OPEN)
		self.button32.connect("clicked", self.apri)
		self.fixed2.put(self.button32, 320, 173)
		# Immagine
		self.image = gtk.Image()
		self.image.set_from_file("painte.jpg")
		self.fixed2.put(self.image, 340, 30)
		self.button33 = gtk.Button("Inserisci")
		self.fixed2.put(self.button33, 60, 275)
		self.button34 = gtk.Button("Pulisci")
		self.fixed2.put(self.button34, 180, 275)
		self.button35 = gtk.Button("Chiudi")
		self.button35.connect_object("clicked", gtk.Widget.destroy, self.win)
		self.fixed2.put(self.button35, 280, 275)

################################################################################
		
		self.notebook.set_current_page(1)
		
		self.table.show()
		self.win.show_all()
		
	def apri(self, title):
		file = finestre.file()
