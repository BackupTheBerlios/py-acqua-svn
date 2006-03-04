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
from pysqlite2 import dbapi2 as sqlite
import Image

class Skin(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		self.set_title(_('Skin'))
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		self.set_resizable(False)
		
		path = os.path.join("pixmaps", "skin")
		
		box = gtk.VBox()
		box.set_spacing(4)
		box.set_border_width(4)
		
		i = 0
		
		for file in os.listdir(path):
			i += 1 
			frm = gtk.Frame("Skin" + str(i))
			
			self.check = gtk.CheckButton(file)
			self.hbox = gtk.HBox()
			image = gtk.Image()
			image.set_from_file(os.path.join(path, file))
			self.hbox.pack_start(self.check)
			self.hbox.pack_start(image)
			
			frm.add(self.hbox)
			box.pack_start(frm)
			
			
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		bb.set_spacing(5)
		
		btn = gtk.Button(stock=gtk.STOCK_CLOSE)
		btn.connect('clicked', self.exit)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_ADD)
		#btn.connect('clicked', self.inserisci_test)
		bb.pack_start(btn)
		box.pack_start(bb, False, False, 0)
		
		self.add(box)
		self.show_all()
		
	def exit(self, *w):
		self.hide()
		
	def insert_skin(self, widget):
		pass
