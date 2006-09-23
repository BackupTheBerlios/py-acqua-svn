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
import utils
import impostazioni
from pysqlite2 import dbapi2 as sqlite
from copy import copy

class Manutenzione(gtk.ScrolledWindow):
	def __init__(self):
		gtk.ScrolledWindow.__init__(self)
		
		self.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
		box = gtk.VBox()
		box.set_spacing(4)
		box.set_border_width(4)
		
		# Iniziamo con la tabella
		tbl = gtk.Table (5, 4, False)
		
		self.store = gtk.ListStore (str)
		self.view = gtk.TreeView (self.store)
		
		self.view.append_column ( gtk.TreeViewColumn (None, gtk.CellRendererText (), text=0) )
		self.view.set_headers_visible (False)
		
		self.view.get_selection ().connect ('changed', self.on_change_selection)
		
		
		labels = (
			 _('Data'),
			 _('Tipo'),
			 _('Nome'),
			 _('Quantita'),
			 _('Prossima volta'),
			 _('Note')
		)
		
		self.widgets = []
		
		x = 0
		for i in labels:
			tbl.attach (utils.new_label (i), 0, 1, x, x+1)
			x += 1
	
		self.e_data = utils.DataButton ()
		self.e_tipo = utils.Combo ([_("Fertilizzante"), _("Filtro")])
		self.e_nome = gtk.Entry()
		self.e_quantita = utils.FloatEntry ()
		self.e_prossima = utils.DataButton()
		self.e_note = utils.NoteEntry()
		tbl.attach(self.e_data, 1, 2, 0, 1, xoptions=0)
		tbl.attach(self.e_tipo, 1, 2, 1, 2, xoptions=0)
		tbl.attach(self.e_nome, 1, 2, 2, 3, xoptions=0)
		tbl.attach(self.e_quantita, 1, 2, 3, 4, xoptions=0)
		tbl.attach(self.e_prossima, 1, 2, 4, 5, xoptions=0)
		tbl.attach(self.e_note, 1, 2, 5, 6, xoptions=0)
		
		
		box.pack_start(tbl)
		
		
		
		btn = gtk.Button(stock=gtk.STOCK_APPLY)
		btn.connect('clicked', self.on_apply_changes)
		btn.set_relief (gtk.RELIEF_NONE)
		
		
		
		self.add_with_viewport (box)
		self.show_all ()
	
	def on_change_selection (self, selection):
		pass
	
	def populate_combo (self):
		pass
	
	def on_del_collection (self, widget):
		pass
			
	def on_add_collection (self, widget):
		pass
	
	def on_apply_changes (self, widget):
		pass
	def exit(self, *w):
		# dovrebbe bastare
		impostazioni.save ()
		
		self.hide()
