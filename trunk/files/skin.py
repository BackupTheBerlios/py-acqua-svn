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
		self.set_title(_("Skin"))
		
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		self.set_resizable(False)
		
		path = os.path.join(os.getcwd(), os.path.join("pixmaps", "skin"))
		
		box = gtk.VBox()
		box.set_spacing(4)
		box.set_border_width(4)

		# Hbox per contenere una scrolled e un image
		hbox = gtk.HBox()
		
		# Una Scrolled Window per contenere
		# la Treeview
		
		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
		# Due colonne una per il nome dello skin
		# l'altra per il percorso al file main.png
		
		list = gtk.ListStore(str, str)
		self.view = view = gtk.TreeView(list)
		
		view.append_column(gtk.TreeViewColumn(_("Skin"), gtk.CellRendererText(), text=0))
		view.get_selection().connect('changed', self.on_selection_changed)

		sw.add(view)

		# Creiamo self.image
		
		self.image = gtk.Image()
		
		# Pacchiamo
		
		hbox.pack_start(sw, False, False, 0)
		hbox.pack_start(self.image)

		box.pack_start(hbox)
		
		for file in os.listdir(path):
			current = os.path.join(path, file)
			if os.path.isdir(current):
				self.add_skin(current, list)
			
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
		
	def add_skin(self, path, list):
		back = os.path.join(path, "main.png")
		print back
		
		if not os.path.exists(back):
			return

		list.append([os.path.basename(path), back])
	
	def on_selection_changed(self, selection):
		mod, it = selection.get_selected()
		self.update_image(mod.get_value(it, 1))
	
	def update_image(self, path):
		self.image.set_from_file(path)
		
	def exit(self, *w):
		self.hide()
		
	def insert_skin(self, widget):
		dialog = gtk.FileChooserDialog(_("Inserisci skin..."), self,
			buttons = (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
		
		filter = gtk.FileFilter()
		filter.set_name(_("Skin py-Acqua"))
		filter.add_pattern("*.png")
		filter.add_pattern("*.jpg")
		dialog.add_filter(filter)
		
		id = self.dialog.run() 

		if id == gtk.RESPONSE_OK:
			file = self.dialog.get_filename()
			path = os.path.join(os.getcwd(), 'pixmaps/skin')
			
			#Copio tutto nella dir skin
			if self.path != file:
				try:
					shutil.copy(file, 'pixmaps/skin')
				except:
					print _("E' occorso un errore durante la copia: %s") % sys.exc_value
		
		dialog.hide()
		dialog.destroy()
		
	def on_skin_ok(self, widget):
		mod, it = self.view.get_selection().get_selected()
		
		if it == None:
			return
		else:
			impostazioni.sfondo = mod.get_value(it, 1)

		impostazioni.save()
		self.exit()
		
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
