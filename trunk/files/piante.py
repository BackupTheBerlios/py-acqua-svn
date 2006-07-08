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
import dbwindow

class Piante (dbwindow.DBWindow):
	def __init__(self):
		
		lst = gtk.ListStore (int, str, str, int, str, gtk.gdk.Pixbuf, str)
		self.col_lst = [_('Id'), _('Data'), _('Vasca'), _('Quantita'), _('Nome'), _("Note"), _("Immagine")]
		
		dbwindow.DBWindow.__init__ (self, 2, 2, self.col_lst,
			[utils.DataButton (), utils.Combo (), utils.IntEntry (), gtk.Entry (), utils.NoteEntry (), utils.ImgEntry ()], lst)
		
		for y in utils.get ("select * from piante"):
			lst.append([y[0], y[1], y[2], y[3], y[4], y[5], utils.make_image(y[6]), y[6]])
		
		for y in utils.get ("select * from vasca"):
			self.vars[1].append_text (y[3])
		
		self.set_title (_("Piante"))
		self.set_size_request (600, 400)
		self.set_icon_from_file ("pixmaps/logopyacqua.jpg")
		
	def after_refresh (self, it):
		mod, it = self.view.get_selection().get_selected()
		
		id = mod.get_value (it, 0)
		
		date = self.vars[0].get_text ()
		vasca = self.vars[1].get_text ()
		quantita = self.vars[2].get_text ()
		nome = self.vars[3].get_text ()
		note = self.vars[4].get_text ()
		img = self.vars [5].get_text ()
		
		utils.cmd ("update piante set date='%(date)s', vasca='%(vasca)s', quantita='%(quantita)s', nome='%(nome)s', note='%(note)s', img='%(img)s' where id = %(id)s" % vars ())
		
		self.update_status (dbwindow.NotifyType.SAVE, _("Row aggiornata (ID: %d)") % id)

	def add_entry (self, it):
		mod, id = self.view.get_selection ().get_selected ()

		id = mod.get_value (it, 0)

		for i in self.vars:
			print i.get_text ()
		
		utils.cmd ('insert into piante values(?,?,?,?,?,?,?)',
				id,
				self.vars[0].get_text (),
				self.vars[1].get_text (),
				self.vars[2].get_text (),
				self.vars[3].get_text (),
				self.vars[4].get_text (),
				self.vars[5].get_text ())
		
		self.update_status (dbwindow.NotifyType.ADD, _("Row aggiunta (ID: %d)") % id)
		
	def remove_id (self, id):
		utils.cmd ('delete from piante where id=%d' % id)
		self.update_status (dbwindow.NotifyType.DEL, _("Row rimossa (ID: %d)") % id)
	
	def decrement_id (self, id):
		utils.cmd ("update piante set id=%d where id=%d" % (id - 1, id))

	def on_row_activated(self, tree, path, col):
		mod = self.view.get_model()
		it = mod.get_iter_from_string(str(path[0]))

		utils.InfoDialog(self, _("Riepilogo"), self.col_lst, self.vars, mod.get_value (it, 6))
