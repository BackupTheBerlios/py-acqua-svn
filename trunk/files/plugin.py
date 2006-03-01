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

import os, sys, tarfile, shutil, time

class plugin(gtk.Window):
	
	def __init__(self):
		gtk.Window.__init__(self)
		self.set_title("Plug-in")
		self.set_resizable(False)
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		self.set_size_request(500, 150)
		
		box = gtk.VBox()
		
		self.vasca_store = gtk.ListStore(int, str, str, str, str)
		self.view = view = gtk.TreeView(self.vasca_store)
		lst = ['Id', 'Nome', 'Autore', 'Email', 'Data']
		
		render = gtk.CellRendererText()
		
		for i in lst:
			id = lst.index(i)
			col = gtk.TreeViewColumn(i, render, text = id)
			col.set_sort_column_id(id)
			col.set_clickable(True)
			col.set_resizable(True)
			view.append_column(col)
			
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		
		sw.add(view)
		box.pack_start(sw)
		
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		
		btn = gtk.Button(stock=gtk.STOCK_ADD)
		btn.connect('clicked', self.on_add)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_REFRESH)
		btn.connect('clicked', self.on_refresh)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_REMOVE)
		btn.connect('clicked', self.on_del)
		bb.pack_start(btn)
		
		box.pack_start(bb, False, False, 0)
		
		self.status = gtk.Statusbar()
		#self.status.push(0, "Prova")
		box.pack_start(self.status)
		
		self.add(box)
		self.show_all()
			
	def on_del(self, widget):
		pass
			
	def on_refresh(self, widget):
		pass
		
	def on_add(self, widget):
		self.dialog = gtk.FileChooserDialog("Carica Plug-in...", self, 
			buttons = (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
		
		filter = gtk.FileFilter()
		filter.set_name("Plug-in py-Acqua")
		filter.add_pattern("*.py")
		filter.add_pattern("*.tar.gz")
		self.dialog.add_filter(filter)
		
		self.dialog.connect('response', self.filename)
		
		id = self.dialog.run() 
		self.dialog.hide()		
		
		self.dialog.destroy()
		
	def filename(self, widget, data=None):
		file = self.dialog.get_filename()
		file_split = os.path.splitext(file)
		self.path = os.path.join(os.getcwd(), 'Plugin')
		
		#Estraggo dai file tar.gz
		if file_split[1] == '.gz':
			try:
				tar_file = tarfile.open(mode = "r|", fileobj = file)
				for tarinfo in tar_file:
					tar_file.extract(tarinfo)
				tar.close()
			except:
				print "Errore durante l'estrazione: %s" % sys.exc_value
		
		#Copio tutto nella dir Plugin		
		if self.path != file:
			try:
				shutil.copy(file, 'Plugin')
			except:
				print "E' occorso un errore durante la copia: %s" % sys.exc_value
				
		#Cerca nella dir i file e le cartelle
		for dir_file in os.listdir(self.path):
			if os.path.isfile(os.path.join(self.path, dir_file)):
				pass
			elif os.path.isdir(os.path.join(self.path, dir_file)):
				pass
