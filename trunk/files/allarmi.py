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

import gtk

from data import *
from inserisci import *
from finestre import *

class Allarmi(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		
		self.set_title('Allarmi')

		vbox = gtk.VBox()

		nb = gtk.Notebook()

		# Aggiungiamo i tab
		self.ph = self.gh = self.no2 = self.no3 = self.cond = None
		self.ammoniaca = self.ferro = self.rame = self.fosfati = None

		nb.append_page(self.make_test_page(), gtk.Label('Test'))
		nb.append_page(self.make_fert_page(), gtk.Label('Fertilizzante'))
		nb.append_page(self.make_filt_page(), gtk.Label('Filtro'))
		
		vbox.pack_start(nb)

		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)

		btn = gtk.Button(stock=gtk.STOCK_CLOSE)
		btn.connect('clicked', self.exit)
		
		bb.pack_start(btn)

		vbox.pack_start(bb, False, False, 0)
		
		self.add(vbox)
		self.show_all()
	def make_filt_page(self):
		return gtk.Label('Not yet implemented')
	def make_fert_page(self):
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		return sw
	def make_test_page(self):
		# Pagina Test
		tbl = gtk.Table(10, 2)
		tbl.set_border_width(5)
		
		tbl.attach(self.new_label('Ph'), 0, 1, 0, 1)
		tbl.attach(self.new_label('Kh'), 0, 1, 1, 2)
		tbl.attach(self.new_label('Gh'), 0, 1, 2, 3)
		tbl.attach(self.new_label('No2'), 0, 1, 3, 4)
		tbl.attach(self.new_label('No3'), 0, 1, 4, 5)
		tbl.attach(self.new_label('Conducibilità'), 0, 1, 5, 6)
		tbl.attach(self.new_label('Ammoniaca'), 0, 1, 6, 7)
		tbl.attach(self.new_label('Ferro'), 0, 1, 7, 8)
		tbl.attach(self.new_label('Rame'), 0, 1, 8, 9)
		tbl.attach(self.new_label('Fosfati'), 0, 1, 9, 10)
		
		self.ph = self.new_label('0', False); self.kh = self.new_label('0', False)
		self.gh = self.new_label('0', False); self.no2 = self.new_label('0', False)
		self.no3 = self.new_label('0', False); self.cond = self.new_label('0', False)
		self.rame = self.new_label('0', False); self.fosfati = self.new_label('0', False)
		self.ammoniaca = self.new_label('0', False); self.ferro = self.new_label('0', False)

		tbl.attach(self.ph, 1, 2, 0, 1)
		tbl.attach(self.kh, 1, 2, 1, 2)
		tbl.attach(self.gh, 1, 2, 2, 3)
		tbl.attach(self.no2, 1, 2, 3, 4)
		tbl.attach(self.no3, 1, 2, 4, 5)
		tbl.attach(self.cond, 1, 2, 5, 6)
		tbl.attach(self.ammoniaca, 1, 2, 6, 7)
		tbl.attach(self.ferro, 1, 2, 7, 8)
		tbl.attach(self.rame, 1, 2, 8, 9)
		tbl.attach(self.fosfati, 1, 2, 9, 10)

		return tbl
		
	def new_label(self, txt, bold=True):
		lbl = gtk.Label()
		if bold:
			lbl.set_use_markup(True)
			lbl.set_label('<b>' + txt + '</b>')
			lbl.set_alignment(0, 0.5)
		else:
			lbl.set_label(txt)
			lbl.set_alignment(0.5, 0)
		
		return lbl
		
	def exit(self, *w):
		self.hide()
