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
import gtk
import os
import utils
import impostazioni
#from inserisci import *
#from pysqlite2 import dbapi2 as sqlite

class Inserisci(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		
		self.set_title('Inserisci')

		vbox = gtk.VBox()
		vbox.set_spacing(4)
		vbox.set_border_width(4)

		nb = gtk.Notebook()

		# Aggiungiamo i tab
		#self.ph = self.gh = self.no2 = self.no3 = self.cond = None
		#self.ammoniaca = self.ferro = self.rame = self.fosfati = None

		nb.append_page(self.make_test_page(), gtk.Label('Test'))
		nb.append_page(self.make_fert_page(), gtk.Label('Fertilizzante'))
		nb.append_page(self.make_filt_page(), gtk.Label('Filtro'))
		
		vbox.pack_start(nb)

		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		bb.set_spacing(4)

		btn = gtk.Button(stock=gtk.STOCK_CLOSE)
		btn.connect('clicked', self.exit)

		bb.pack_start(btn)

		btn = gtk.Button(stock=gtk.STOCK_ADD)
		btn.connect('clicked', self.inserisci)
		
		bb.pack_start(btn)

		vbox.pack_start(bb, False, False, 0)
		
		self.add(vbox)
		self.show_all()

		self.set_size_request(400, 300)
		#self.refresh(None)
		
	def inserisci(self, widget):
	
		impostazioni.minph = self.ph_minimo
		impostazioni.maxph = self.ph_massimo
		impostazioni.minkh = self.kh_minimo
		impostazioni.maxkh = self.kh_massimo
		impostazioni.save()
		
	def make_filt_page(self):
	
		# Pagina filtro

		box = gtk.VBox()
		
		tbl = gtk.Table(2, 2)
		tbl.set_border_width(5)
		
		tbl.attach(self.new_label('Data'), 0, 1, 0, 1)
		tbl.attach(self.new_label('Ogni quanti giorni'), 0, 1, 1, 2)
		
		self.data = utils.DataButton()
		self.giorni = gtk.Entry()
		
		tbl.attach(self.data, 1, 2, 0, 1)
		tbl.attach(self.giorni, 1, 2, 1, 2)
		
		box.pack_start(tbl, False, False, 0)
		return box
		
	def make_fert_page(self):
	
		# Pagina fertilizzante

		box = gtk.VBox()
		
		tbl = gtk.Table(4, 2)
		tbl.set_border_width(5)
		
		tbl.attach(self.new_label('Data'), 0, 1, 0, 1)
		tbl.attach(self.new_label('Nome'), 0, 1, 1, 2)
		tbl.attach(self.new_label('Quantita'), 0, 1, 2, 3)
		tbl.attach(self.new_label('Ogni quanti giorni'), 0, 1, 3, 4)
		
		self.data = utils.DataButton(); self.nome = gtk.Entry()
		self.quantita = gtk.Entry(); self.giorni = gtk.Entry()
		
		tbl.attach(self.data, 1, 2, 0, 1)
		tbl.attach(self.nome, 1, 2, 1, 2)
		tbl.attach(self.quantita, 1, 2, 2, 3)
		tbl.attach(self.giorni, 1, 2, 3, 4)
		
		box.pack_start(tbl, False, False, 0)
		return box
		
	def make_test_page(self):
		# Pagina Test

		box = gtk.VBox()
		
		tbl = gtk.Table(11, 3)
		tbl.set_border_width(5)
		
		tbl.attach(self.new_label('Minimo'), 1, 2, 0, 1)
		tbl.attach(self.new_label('Massimo'), 2, 3, 0, 1)
		tbl.attach(self.new_label('Ph'), 0, 1, 1, 2)
		tbl.attach(self.new_label('Kh'), 0, 1, 2, 3)
		tbl.attach(self.new_label('Gh'), 0, 1, 3, 4)
		tbl.attach(self.new_label('No2'), 0, 1, 4, 5)
		tbl.attach(self.new_label('No3'), 0, 1, 5, 6)
		tbl.attach(self.new_label('Conducibilità'), 0, 1, 6, 7)
		tbl.attach(self.new_label('Ammoniaca'), 0, 1, 7, 8)
		tbl.attach(self.new_label('Ferro'), 0, 1, 8, 9)
		tbl.attach(self.new_label('Rame'), 0, 1, 9, 10)
		tbl.attach(self.new_label('Fosfati'), 0, 1, 10, 11)
		
		self.ph_minimo = gtk.Entry(); self.ph_massimo = gtk.Entry()
		self.kh_minimo = gtk.Entry(); self.kh_massimo = gtk.Entry()
		self.gh_minimo = gtk.Entry(); self.gh_massimo = gtk.Entry()
		self.no2_minimo = gtk.Entry(); self.no2_massimo = gtk.Entry()
		self.no3_minimo = gtk.Entry(); self.no3_massimo = gtk.Entry()
		self.cond_minimo = gtk.Entry(); self.cond_massimo = gtk.Entry()
		self.rame_minimo = gtk.Entry(); self.rame_massimo = gtk.Entry()
		self.fosfati_minimo = gtk.Entry(); self.fosfati_massimo = gtk.Entry()
		self.ammoniaca_minimo = gtk.Entry(); self.ammoniaca_massimo = gtk.Entry()
		self.ferro_minimo = gtk.Entry(); self.ferro_massimo = gtk.Entry()

		tbl.attach(self.ph_minimo, 1, 2, 1, 2)
		tbl.attach(self.ph_massimo, 2, 3, 1, 2)
		tbl.attach(self.kh_minimo, 1, 2, 2, 3)
		tbl.attach(self.kh_massimo, 2, 3, 2, 3)
		tbl.attach(self.gh_minimo, 1, 2, 3, 4)
		tbl.attach(self.gh_massimo, 2, 3, 3, 4)
		tbl.attach(self.no2_minimo, 1, 2, 4, 5)
		tbl.attach(self.no2_massimo, 2, 3, 4, 5)
		tbl.attach(self.no3_minimo, 1, 2, 5, 6)
		tbl.attach(self.no3_massimo,2, 3, 5, 6)
		tbl.attach(self.cond_minimo, 1, 2, 6, 7)
		tbl.attach(self.cond_massimo, 2, 3, 6, 7)
		tbl.attach(self.ammoniaca_minimo, 1, 2, 7, 8)
		tbl.attach(self.ammoniaca_massimo, 2, 3, 7, 8)
		tbl.attach(self.ferro_minimo, 1, 2, 8, 9)
		tbl.attach(self.ferro_massimo, 2, 3, 8, 9)
		tbl.attach(self.rame_minimo, 1, 2, 9, 10)
		tbl.attach(self.rame_massimo, 2, 3, 9, 10)
		tbl.attach(self.fosfati_minimo, 1, 2, 10, 11)
		tbl.attach(self.fosfati_massimo, 2, 3, 10, 11)
		
		

		box.pack_start(tbl, False, False, 0)
		return box
		
	def new_label(self, txt, bold=True):
		lbl = gtk.Label()
		if bold:
			lbl.set_use_markup(True)
			lbl.set_label('<b>' + txt + '</b>')
			lbl.set_alignment(0, 0.5)
		else:
			lbl.set_label(txt)
			lbl.set_alignment(0.5, 0.5)
		
		return lbl
		
	def exit(self, *w):
		self.hide()
