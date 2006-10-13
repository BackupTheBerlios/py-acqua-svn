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
from dbwindow import BaseDBWindow
from pysqlite2 import dbapi2 as sqlite
from copy import copy

class Manutenzione(BaseDBWindow):
	def __init__(self, window_db):
		self.main_db = window_db
	
	def bind_context (self):
		lst = gtk.ListStore (int, str, str, str, str, str, str, str)
		
		self.context_id = self.main_db.create_context (1, 7, [_('Id'),
									  _('Vasca'),
									  _('Data'),
									  _('Tipo'),
									  _('Nome'),
									  _('Quantita'),
									  _('Prossima volta'),
									  _('Note')],
									 [utils.Combo (),
									  utils.DataButton (),
									  utils.Combo ([_("Fertilizzante"), _("Filtro")]),
									  gtk.Entry (),
									  utils.IntEntry (),
									  utils.DataButton (),
									  utils.NoteEntry ()], lst, True)
		
		for y in utils.get ("select * from vasca"):
			self.main_db.vars[0].append_text (y[3])
	
	# TODO:
	# Qui ci pensi te luca... odio ripetermi :P
	
	def after_selection_changed (self, mod, it):
		pass

	def on_row_activated (self, tree, path, col):
		pass
		
	def after_refresh (self, it):
		# Implementata dalla sovraclasse
		pass
				
	def add_entry (self, it):
		# Aggiunge la entry nel database
		pass
	
	def remove_id (self, id):
		# Passa l'id da rimuovere nel database
		pass
	def decrement_id (self, id):
		# cur.execute("update vasca set id=%d where id=%d" % (id-1, id))
		pass
	
	def pack_before_button_box (self, hb):
		pass
