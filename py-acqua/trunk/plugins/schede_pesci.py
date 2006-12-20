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



import pyacqua.app as app
import gtk
import os
import ConfigParser
import pyacqua.utils as utils

# creiamo le dir se non ci sono gia dove contenere le schede dei pesci

#if not os.path.exists ("Schede"):
#	os.mkdir('Schede')
#	
#else:
#	
#	if not os.path.exists ("Schede/Pesci"):
#		os.mkdir('Schede/Pesci')
#	else:
#		pass
#		
#par = os.path.join('Schede', 'Pesci', 'chanda_ranga', 'chanda_ranga.cfg')
#
#cfg = ConfigParser.ConfigParser()
#
#	
#cfg.read(par)
#global nomeporco
#			
#nomeporco = cfg.get("nomescientifico", "nm")
	
		
#qua dopo aver creato le dir in futuro bisognera decomprimere il file con tutte le schede
#oppure far in modo di scaricarle da internet
		
class schede_pesci(gtk.Window):
	__name__ = "Schede Pesci"
	__desc__ = "Plugin per schede pesci"
	__ver__ = "0.0.1"
	__author__ = "PyAcqua team"
	__preferences__ = {}

	def __init__(self):
		gtk.Window.__init__ (self)
		self.create_gui ()
		self.set_title(_("Schede Pesci"))
		self.set_size_request (600, 400)
		utils.set_icon (self)

	def start (self):
		print ">> Starting", self.__name__
		
		menu = app.App.get_plugin_menu ()

		self.item = gtk.MenuItem ("Schede Pesci")
		self.item.connect ('activate', self.on_activated)
		self.item.show ()
		
		menu.append (self.item)
	def create_gui (self):
	
		box = gtk.VBox()
		box.set_spacing(4)
		box.set_border_width(4)
		
		tbl = gtk.Table(11, 3)
		tbl.set_border_width(5)
		
		tbl.attach(utils.new_label(_('Nome Scientifico')), 0, 1, 0, 1, yoptions=gtk.SHRINK)
		
		self.nome_scientifico = gtk.Entry ()
		
		tbl.attach(self.nome_scientifico, 1, 2, 0, 1, yoptions=gtk.SHRINK)
		
		#self.nome_scientifico.set_text (str (nomeporco))
		box.pack_start(tbl)
		self.add(box)
		
		self.connect ('delete_event', self.exit)
		
	def stop (self):
		print "** Stopping", self.__name__

		self.item.hide ()
		self.item.destroy ()
	
	def on_activated(self, widget):
		self.show_all()
		
	def exit(self, *w):
		self.hide()
		return True # Per non distruggere il contenuto
