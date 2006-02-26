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
import os
import utils
import impostazioni
#from inserisci import *
from pysqlite2 import dbapi2 as sqlite

class Inserisci(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		
		self.set_title(_('Inserisci Test'))
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		box = gtk.VBox()
		box.set_spacing(4)
		box.set_border_width(4)
		
		tbl = gtk.Table(11, 3)
		tbl.set_border_width(5)
		
		tbl.attach(self.new_label(_('Minimo')), 1, 2, 0, 1, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Massimo')), 2, 3, 0, 1, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Ph')), 0, 1, 1, 2, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Kh')), 0, 1, 2, 3, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Gh')), 0, 1, 3, 4, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('No2')), 0, 1, 4, 5, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('No3')), 0, 1, 5, 6, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Conducibilita\'')), 0, 1, 6, 7, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Ammoniaca')), 0, 1, 7, 8, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Ferro')), 0, 1, 8, 9, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Rame')), 0, 1, 9, 10, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Fosfati')), 0, 1, 10, 11, yoptions=gtk.SHRINK)
		
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

		tbl.attach(self.ph_minimo, 1, 2, 1, 2, yoptions=gtk.SHRINK)
		tbl.attach(self.ph_massimo, 2, 3, 1, 2, yoptions=gtk.SHRINK)
		tbl.attach(self.kh_minimo, 1, 2, 2, 3, yoptions=gtk.SHRINK)
		tbl.attach(self.kh_massimo, 2, 3, 2, 3, yoptions=gtk.SHRINK)
		tbl.attach(self.gh_minimo, 1, 2, 3, 4, yoptions=gtk.SHRINK)
		tbl.attach(self.gh_massimo, 2, 3, 3, 4, yoptions=gtk.SHRINK)
		tbl.attach(self.no2_minimo, 1, 2, 4, 5, yoptions=gtk.SHRINK)
		tbl.attach(self.no2_massimo, 2, 3, 4, 5, yoptions=gtk.SHRINK)
		tbl.attach(self.no3_minimo, 1, 2, 5, 6, yoptions=gtk.SHRINK)
		tbl.attach(self.no3_massimo,2, 3, 5, 6, yoptions=gtk.SHRINK)
		tbl.attach(self.cond_minimo, 1, 2, 6, 7, yoptions=gtk.SHRINK)
		tbl.attach(self.cond_massimo, 2, 3, 6, 7, yoptions=gtk.SHRINK)
		tbl.attach(self.ammoniaca_minimo, 1, 2, 7, 8, yoptions=gtk.SHRINK)
		tbl.attach(self.ammoniaca_massimo, 2, 3, 7, 8, yoptions=gtk.SHRINK)
		tbl.attach(self.ferro_minimo, 1, 2, 8, 9, yoptions=gtk.SHRINK)
		tbl.attach(self.ferro_massimo, 2, 3, 8, 9, yoptions=gtk.SHRINK)
		tbl.attach(self.rame_minimo, 1, 2, 9, 10, yoptions=gtk.SHRINK)
		tbl.attach(self.rame_massimo, 2, 3, 9, 10, yoptions=gtk.SHRINK)
		tbl.attach(self.fosfati_minimo, 1, 2, 10, 11, yoptions=gtk.SHRINK)
		tbl.attach(self.fosfati_massimo, 2, 3, 10, 11, yoptions=gtk.SHRINK)
		
		box.pack_start(tbl)
		
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		bb.set_spacing(4)
		
		btn = gtk.Button(stock=gtk.STOCK_CLOSE)
		btn.connect('clicked', self.exit)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_ADD)
		btn.connect('clicked', self.inserisci_test)
		bb.pack_start(btn)
		box.pack_start(bb, False, False, 0)
		
		
		self.add(box)
		self.show_all()
		
	
	def inserisci_test(self, widget):
	
		impostazioni.minph = self.ph_minimo.get_text()
		impostazioni.maxph = self.ph_massimo.get_text()
		impostazioni.minkh = self.kh_minimo.get_text()
		impostazioni.maxkh = self.kh_massimo.get_text()
		impostazioni.mingh = self.gh_minimo.get_text()
		impostazioni.maxgh = self.gh_massimo.get_text()
		impostazioni.minno2 = self.no2_minimo.get_text()
		impostazioni.maxno2 = self.no2_massimo.get_text()
		impostazioni.minno3 = self.no3_minimo.get_text()
		impostazioni.maxno3 = self.no3_massimo.get_text()
		impostazioni.mincon = self.cond_minimo.get_text()
		impostazioni.maxcon = self.cond_massimo.get_text()
		impostazioni.minam = self.ammoniaca_minimo.get_text()
		impostazioni.maxam = self.ammoniaca_massimo.get_text()
		impostazioni.minfe = self.ferro_minimo.get_text()
		impostazioni.maxfe = self.ferro_massimo.get_text()
		impostazioni.minra = self.rame_minimo.get_text()
		impostazioni.maxra = self.rame_massimo.get_text()
		impostazioni.minfo = self.fosfati_minimo.get_text()
		impostazioni.maxfo = self.fosfati_massimo.get_text()
		
		impostazioni.save()
	
		
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
