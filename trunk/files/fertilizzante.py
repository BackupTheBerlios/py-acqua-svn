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

import utils
import dbwindow

class Fertilizzante(dbwindow.DBWindow):
	def __init__(self): 
		# id integer,date DATE, nome TEXT, quantita FLOAT, giorni NUMERIC
		
		lst = gtk.ListStore(int, str, str, float, str)
		dbwindow.DBWindow.__init__(self, 1, 4,
				[_('Id'), _('Data'), _('Nome'), _('Quantita\''), _('Prossima volta')],
				[utils.DataButton(), gtk.Entry(), utils.FloatEntry(), utils.DataButton()],
				lst)
		
		for y in utils.get ('select * from fertilizzante'):
			lst.append([y[0], y[1], y[2], y[3], y[4]])
	
	def after_refresh (self, it):
		mod, it = self.view.get_selection().get_selected()

		id = mod.get_value (it, 0)
		date = self.vars[0].get_text ()
		nome = self.vars[1].get_text ()
		quantita = self.vars[2].get_text ()
		giorni = self.vars[3].get_text ()
		
		utils.cmd ("update fertilizzante set date='%(date)s', nome='%(nome)s', quantita='%(quantita)s', giorni='%(giorni)s' where id=%(id)s" %vars())
			
		self.update_status(dbwindow.NotifyType.SAVE, _("Row aggiornata (ID: %d)") % id)
	
	def add_entry (self, it):
		mod, id = self.view.get_selection().get_selected()

		id = mod.get_value (it, 0)
		
		utils.cmd ('insert into fertilizzante values(?,?,?,?,?)', id,
				self.vars[0].get_text (),
				self.vars[1].get_text (),
				self.vars[2].get_text (),
				self.vars[3].get_text ())

		self.update_status(dbwindow.NotifyType.ADD, _("Row aggiunta (ID: %d)") % id)
	
	def remove_id (self, id):
		utils.cmd ('delete from fertilizzante where id=%d' % id)
		self.update_status(dbwindow.NotifyType.DEL, _("Row rimossa (ID: %d)" % id))
	
	def decrement_id (self, id):
		utils.cmd ('update fertilizzante set id=%d where id=%d' % (id - 1, id))
