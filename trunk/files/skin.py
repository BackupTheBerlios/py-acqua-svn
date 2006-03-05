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
import sys
import shutil
import utils
import impostazioni

class Skin(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		self.set_title(_('Skin'))
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		#self.set_resizable(False)
		
		path = os.path.join(os.getcwd(), os.path.join("pixmaps", "skin"))
		
		box = gtk.VBox()
		box.set_spacing(4)
		box.set_border_width(4)
		
		i = 0
		
		for file in os.listdir(path):
			i += 1 
			frm = gtk.Frame("Skin" + str(i))
			
			self.check = gtk.CheckButton(file)
			self.hbox = gtk.HBox()
			#im = Image.open(os.path.join(path, file))
			#im = im.resize((120, 120))
			
			
			#pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(path, file))
			#w, h = make_thumb(50, pixbuf.get_width(), pixbuf.get_height())
			#return pixbuf.scale_simple(w, h, gtk.gdk.INTERP_HYPER)
			
			
			image = gtk.Image()
			image.set_from_file(os.path.join(path, file))
			self.hbox.pack_start(self.check)
			self.hbox.pack_start(image)
			
			frm.add(self.hbox)
			box.pack_start(frm)
			
			
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		bb.set_spacing(5)
		
		btn = gtk.Button(stock=gtk.STOCK_OK)
		btn.connect('clicked', self.on_skin_ok)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_CLOSE)
		btn.connect('clicked', self.exit)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_ADD)
		btn.connect('clicked', self.insert_skin)
		bb.pack_start(btn)
		box.pack_start(bb, False, False, 0)
		
		self.add(box)
		self.show_all()
		
	def exit(self, *w):
		self.hide()
		
	def insert_skin(self, widget):
		self.dialog = gtk.FileChooserDialog("Carica skin...", self, 
			buttons = (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
		
		filter = gtk.FileFilter()
		filter.set_name("Skin py-Acqua")
		filter.add_pattern("*.png")
		filter.add_pattern("*.jpg")
		self.dialog.add_filter(filter)
		
		self.dialog.connect('response', self.filename)
		
		id = self.dialog.run() 
		self.dialog.hide()		
		
		self.dialog.destroy()
		
	def on_skin_ok(self):
		if self.check.get_active():
			impostazioni.sfondo = file
		else:
			impostazioni.sfondo = file

		impostazioni.save()
	
	def filename(self, widget, data=None):
		file = self.dialog.get_filename()
		path = os.path.join(os.getcwd(), 'pixmaps/skin')
		#Copio tutto nella dir Plugin		
		if self.path != file:
			try:
				shutil.copy(file, 'pixmaps/skin')
			except:
				print "E' occorso un errore durante la copia: %s" % sys.exc_value
				
def make_thumb(twh, w, h):
	if w == h:
		return twh, twh
	if w < h:
		y = twh
		x = int(float(y*w)/float(h))
		return x, y
	if w > h:
		x = twh
		y = int(float(x*h)/float(w))
		return x, y
