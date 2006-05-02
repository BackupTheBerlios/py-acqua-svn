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

class Data_Pesci (dbwindow.DBWindow):
	def __init__(self):
		
		lst = gtk.ListStore (int, str, str, str, gtk.gdk.Pixbuf, str)
		
		dbwindow.DBWindow.__init__(self, 1, 4,
				[_('Id'), _('Data'), _('Nome'), _('Famiglia\''), _('Note')],
				[utils.DataButton(), gtk.Entry(), gtk.Entry(), gtk.Entry()],
				lst)
		
		
		
		
		
		
		
		
		self.set_title (_("Database Pesci"))
		self.set_size_request (600, 400)
		self.set_icon_from_file ("pixmaps/logopyacqua.jpg")

	def on_row_activated(self, tree, path, col):
		mod = self.view.get_model()
		it = mod.get_iter_from_string(str(path[0]))

		utils.InfoDialog(self, _("Riepilogo"), self.col_lst, self.vars, mod.get_value (it, 6))
