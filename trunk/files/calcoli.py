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
import finestre

class win2(gtk.Window):
	def __init__(self): 
		gtk.Window.__init__(self)
		self.set_title("Calcoli")
		
		vbox = gtk.VBox()
		vbox.set_spacing(4)
		vbox.set_border_width(4)
		
		tbl = gtk.Table(8, 2)
		
		tbl.attach(self.new_label("Altezza:"), 0, 1, 0, 1)
		tbl.attach(self.new_label("Lunghezza:"), 1, 2, 0, 1)
		tbl.attach(self.new_label("Larghezza:"), 2, 3, 0, 1)
		
		self.e_altezza, self.e_lunghezza, self.e_larghezza = gtk.Entry(), gtk.Entry(), gtk.Entry()
		tbl.attach(self.e_altezza, 0, 1, 1, 2)
		tbl.attach(self.e_lunghezza, 1, 2, 1, 2)
		tbl.attach(self.e_larghezza, 2, 3, 1, 2)
		
		tbl.attach(self.new_label("Volume:"), 0, 1, 2, 3)
		tbl.attach(self.new_label("Piante Inseribili:"), 1, 2, 2, 3)
		tbl.attach(self.new_label("Numero di pesci 3-4 cm:"), 2 ,3, 2, 3)
		tbl.attach(self.new_label("0"), 0, 1, 3, 4)
		tbl.attach(self.new_label("0"), 1, 2, 3, 4)
		tbl.attach(self.new_label("0"), 2, 3, 3, 4)
		
		tbl.attach(self.new_label("Numero di pesci 5-6 cm:"), 0, 1, 4, 5)
		tbl.attach(self.new_label("Watt per piante esigenti:"), 1, 2, 4, 5)
		tbl.attach(self.new_label("Watt per piante poco esigenti:"), 2, 3, 4, 5)
		tbl.attach(self.new_label("0"), 0, 1, 5, 6)
		tbl.attach(self.new_label("0"), 1, 2, 5, 6)
		tbl.attach(self.new_label("0"), 2, 3, 5, 6)
		
		
		vbox.pack_start(tbl)

		
		
	
		
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		
		
		
		btn = gtk.Button(stock=gtk.STOCK_REFRESH)
		#btn.connect('clicked', self.on_refresh)
		bb.pack_start(btn)
		
		
		
		vbox.pack_start(bb, False, False, 0)
		
		self.add(vbox)
		
		self.show_all()
		
	def calcola(self, obj):
		try:
			a = int(self.entry1.get_text())
			b = int(self.entry2.get_text())
			c = int(self.entry3.get_text())
			
			
		except ValueError:
			a = 0
			b = 0
			c = 0
			#Finestra dialog con errore
		
		e = a*b*c/1000
		f = b*a/50
		g = e/(1.5*4)
		h = e / (3*6)
		i = e*0.5
		l = e*0.35

		self.label7.set_text(str(e))
		self.label8.set_text(str(f))
		self.label9.set_text(str(g))
		self.label13.set_text(str(h))
		self.label14.set_text(str(i))
		self.label15.set_text(str(l))
	
	def pulisci_calcoli(self, obj):
		self.entry1.set_text("")
		self.entry2.set_text("")
		self.entry3.set_text("")
	def new_label(self, txt):
		lbl = gtk.Label()
		lbl.set_use_markup(True)
		lbl.set_label('<b>' + txt + '</b>')
		lbl.set_alignment(0.0, 0.5)
		
		return lbl
