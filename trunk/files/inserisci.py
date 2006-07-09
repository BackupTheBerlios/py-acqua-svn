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

class Inserisci(gtk.ScrolledWindow):
	def __init__(self):
		gtk.ScrolledWindow.__init__(self)
		
		self.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
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
		tbl.attach(self.new_label(_('Calcio')), 0, 1, 11, 12, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Magnesio')), 0, 1, 12, 13, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Densita\'')), 0, 1, 13, 14, yoptions=gtk.SHRINK)
		
		
		self.ph_minimo = utils.FloatEntry (); self.ph_massimo = utils.FloatEntry ()
		self.kh_minimo = utils.FloatEntry (); self.kh_massimo = utils.FloatEntry ()
		self.gh_minimo = utils.FloatEntry (); self.gh_massimo = utils.FloatEntry ()
		self.no2_minimo = utils.FloatEntry (); self.no2_massimo = utils.FloatEntry ()
		self.no3_minimo = utils.FloatEntry (); self.no3_massimo = utils.FloatEntry ()
		self.cond_minimo = utils.FloatEntry (); self.cond_massimo = utils.FloatEntry ()
		self.rame_minimo = utils.FloatEntry (); self.rame_massimo = utils.FloatEntry ()
		self.fosfati_minimo = utils.FloatEntry (); self.fosfati_massimo = utils.FloatEntry ()
		self.ammoniaca_minimo = utils.FloatEntry (); self.ammoniaca_massimo = utils.FloatEntry ()
		self.ferro_minimo = utils.FloatEntry (); self.ferro_massimo = utils.FloatEntry ()
		self.calcio_minimo = utils.FloatEntry (); self.calcio_massimo = utils.FloatEntry ()
		self.magnesio_minimo = utils.FloatEntry (); self.magnesio_massimo = utils.FloatEntry ()
		self.densita_minimo = utils.FloatEntry (); self.densita_massimo = utils.FloatEntry ()
		
		

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
		tbl.attach(self.calcio_minimo, 1, 2, 11, 12, yoptions=gtk.SHRINK)
		tbl.attach(self.calcio_massimo, 2, 3, 11, 12, yoptions=gtk.SHRINK)
		tbl.attach(self.magnesio_minimo, 1, 2, 12, 13, yoptions=gtk.SHRINK)
		tbl.attach(self.magnesio_massimo, 2, 3, 12, 13, yoptions=gtk.SHRINK)
		tbl.attach(self.densita_minimo, 1, 2, 13, 14, yoptions=gtk.SHRINK)
		tbl.attach(self.densita_massimo, 2, 3, 13, 14, yoptions=gtk.SHRINK)
		
		self.ph_minimo.set_text (str (impostazioni.minph)); self.ph_massimo.set_text (str (impostazioni.maxph))
		self.kh_minimo.set_text (str (impostazioni.minkh)); self.kh_massimo.set_text (str (impostazioni.maxkh))
		self.gh_minimo.set_text (str (impostazioni.mingh)); self.gh_massimo.set_text (str (impostazioni.maxgh))
		self.no2_minimo.set_text (str (impostazioni.minno2)); self.no2_massimo.set_text (str (impostazioni.maxno2))
		self.no3_minimo.set_text (str (impostazioni.minno3)); self.no3_massimo.set_text (str (impostazioni.maxno3))
		self.cond_minimo.set_text (str (impostazioni.mincon)); self.cond_massimo.set_text (str (impostazioni.maxcon))
		self.rame_minimo.set_text (str (impostazioni.minra)); self.rame_massimo.set_text (str (impostazioni.maxra))
		self.fosfati_minimo.set_text (str (impostazioni.minfo)); self.fosfati_massimo.set_text (str (impostazioni.maxfo))
		self.ammoniaca_minimo.set_text (str (impostazioni.minam)); self.ammoniaca_massimo.set_text (str (impostazioni.maxam))
		self.ferro_minimo.set_text (str (impostazioni.minfe)); self.ferro_massimo.set_text (str (impostazioni.maxfe))
		self.calcio_minimo.set_text (str (impostazioni.mincal)); self.calcio_massimo.set_text (str (impostazioni.maxcal))
		self.magnesio_minimo.set_text (str (impostazioni.minmag)); self.magnesio_massimo.set_text (str (impostazioni.maxmag))
		self.densita_minimo.set_text (str (impostazioni.minden)); self.densita_massimo.set_text (str (impostazioni.maxden))
		
		
		box.pack_start(tbl)
		
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		bb.set_spacing(4)
		
		btn = gtk.Button(stock=gtk.STOCK_CANCEL)
		btn.connect('clicked', self.exit)
		btn.set_relief (gtk.RELIEF_NONE)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_SAVE)
		btn.connect('clicked', self.inserisci_test)
		btn.set_relief (gtk.RELIEF_NONE)
		bb.pack_start(btn)
		box.pack_start(bb, False, False, 0)
		
		
		self.add_with_viewport (box)
		self.show_all ()
		
	
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
		impostazioni.mincal = self.calcio_minimo.get_text()
		impostazioni.maxcal = self.calcio_massimo.get_text()
		impostazioni.minmag = self.magnesio_minimo.get_text()
		impostazioni.maxmag = self.magnesio_massimo.get_text()
		impostazioni.minden = self.densita_minimo.get_text()
		impostazioni.maxden = self.densita_massimo.get_text()
		
		
		
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
