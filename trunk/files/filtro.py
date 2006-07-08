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
import gobject
import os
import sys
import utils
import dbwindow

class Filtro (dbwindow.DBWindow):
	def __init__ (self):
		lst = gtk.ListStore (int, str, str, float, str)
		self.col_lst = [_('Id'), _('Data'), _('Prossima volta'), _('Note')]

		dbwindow.DBWindow.__init__ (self, 1, 2, self.col_lst,
				[utils.DataButton (), utils.DataButton (), utils.NoteEntry ()], lst)

		for y in utils.get ("select * from filtro"):
			lst.append ([y[0], y[1], y[2], y[3]])
		
		self.set_title (_("Filtro"))
		self.set_size_request (600, 400)
		self.set_icon_from_file ("pixmaps/logopyacqua.jpg")

	def after_refresh (self, it):
		mod, it = self.view.get_selection ().get_selected ()

		id = mod.get_value (it, 0)

		date = self.vars[0].get_text ()
		giorni = self.vars[1].get_text ()
		note = self.vars[2].get_text ()
		
		utils.cmd ("update filtro set date='%(date)s', giorni='%(giorni)s', note='%(note)s'" % vars ())

		self.update_status (dbwindow.NotifyType.SAVE, _("Row aggiornata (ID: %d)") % id)

	def add_entry (self, it):
		mod, id = self.view.get_selection ().get_selected ()

		id = mod.get_value (it, 0)

		utils.cmd ('insert into filtro values (?,?,?,?)',
				id,
				self.vars[0].get_text (),
				self.vars[1].get_text (),
				self.vars[2].get_text ())

		self.update_status (dbwindow.NotifyType.ADD, _("Row aggiunta (ID: %d)") % id)
		
	def remove_id (self, id):
		utils.cmd ('delete from filtro where id=%d' % id)
		self.update_status (dbwindow.NotifyType.DEL, _("Row rimossa (ID: %d)") % id)
	
	def decrement_id (self, id):
		utils.cmd ("update filtro set id=%d where id=%d" % (id -1, id))
			
	def on_row_activated(self, tree, path, col):
		mod = self.view.get_model ()
		it = mod.get_iter_from_string (str (path[0]))

		utils.InfoDialog (self, _("Riepilogo"), self.col_lst, self.vars)
