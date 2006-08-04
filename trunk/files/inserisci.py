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
		
		# Iniziamo con la tabella
		tbl = gtk.Table (5, 3, False)
		
		self.combo = utils.Combo ()
		
		self.combo.append_text (_("Crea Nuovo"))
		
		for i in impostazioni.get_names_of_collections ():
			self.combo.append_text (i)
		
		self.combo.set_active (0)
		
		tbl.attach (utils.new_label (_("Modelli:")), 0, 1, 0, 1)
		tbl.attach (self.combo, 1, 3, 0, 1)
		
		tbl.attach (utils.new_label (_("Minimo")), 1, 2, 1, 2)
		tbl.attach (utils.new_label (_("Massimo")), 2, 3, 1, 2)
		
		labels = (
			 _('Ph'),
			 _('Kh'),
			 _('Gh'),
			 _('No2'),
			 _('No3'),
			 _('Conducibilita\''),
			 _('Ammoniaca'),
			 _('Ferro'),
			 _('Rame'),
			 _('Fosfati'),
			 _('Calcio'),
			 _('Magnesio'),
			 _('Densita\'')
		)
		
		widgets = []
		
		x = 2
		for i in labels:
			tbl.attach (utils.new_label (i), 0, 1, x, x+1)
			
			min_entry = utils.FloatEntry ()
			max_entry = utils.FloatEntry ()
			
			tbl.attach (min_entry, 1, 2, x, x+1)
			tbl.attach (max_entry, 2, 3, x, x+1)
			
			widgets.append ([min_entry, max_entry])
			
			x += 1
		
		box.pack_start(tbl)
		
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		bb.set_spacing(4)
		
		btn = gtk.Button(stock=gtk.STOCK_CANCEL)
		#btn.connect('clicked', self.exit)
		btn.set_relief (gtk.RELIEF_NONE)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_SAVE)
		#btn.connect('clicked', self.inserisci_test)
		btn.set_relief (gtk.RELIEF_NONE)
		bb.pack_start(btn)
		box.pack_start(bb, False, False, 0)
		
		
		self.add_with_viewport (box)
		self.show_all ()
		
	def exit(self, *w):
		self.hide()
