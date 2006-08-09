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
import pango

class Vasca (dbwindow.DBWindow):
	def __init__ (self): 

		# id integer, vasca TEXT, date DATE, nome TEXT, litri TEXT, tipo TEXT, filtro TEXT, co TEXT, illuminazione TEXT, reattore TEXT, schiumatoio TEXT, riscaldamento TEXT, img TEXT
		lst = gtk.ListStore (int, str, str, str, float, str, str, str, str, str, str, str, str, gtk.gdk.Pixbuf, str)

		tmp = utils.Combo ([_("Dolce"), _("Dolce Tropicale"), _("Marino"), _("Marino Mediterraneo"), _("Paludario"), _("Salmastro")])
		tmp.connect ('changed', self.aggiorna)

		self.col_lst = [_('Id'), _('Vasca'), _('Data'), _('Nome'), _('Litri'),
			_('Tipo Acquario'), _('Tipo Filtro'),
			_('Impianto Co2'), _('Illuminazione'), 
			_('Reattore di calcio'), _('Schiumatoio'), _('Riscaldamento Refrigerazione'), _("Note"), _("Immagine")]
		
		dbwindow.DBWindow.__init__ (self, 2, 5, self.col_lst,
				[tmp, utils.DataButton (), gtk.Entry (), utils.FloatEntry (),
				 gtk.Entry (), gtk.Entry (), gtk.Entry (), gtk.Entry (), gtk.Entry (),
				 gtk.Entry (), gtk.Entry (), utils.NoteEntry (), utils.ImgEntry ()], lst, True)


		for y in utils.get ('select * from vasca'):
			lst.append([y[0], y[1], y[2], y[3], y[4],
					y[5], y[6], y[7], y[8], y[9], y[10], y[11], y[12], utils.make_image(y[13]), y[13]])
		
		self.view.get_column (12).get_cell_renderers ()[0].set_property ('ellipsize-set', True)
		self.view.get_column (12).get_cell_renderers ()[0].set_property ('ellipsize', pango.ELLIPSIZE_END)
		self.view.get_column (12).set_min_width (140)
		
		self.set_title (_("Vasche"))
		self.set_size_request (700, 500)
		self.set_icon_from_file ("pixmaps/logopyacqua.jpg")
		
		utils.set_icon (self)

		self.menu = gtk.Menu ()

		it = gtk.RadioMenuItem (None, label=_("Dolce"))
		it.connect ('activate', self.show_dolce)
		self.menu.append (it)
		
		it = gtk.RadioMenuItem (it, label=_("Dolce Tropicale"))
		it.connect ('activate', self.show_dolce)
		self.menu.append (it)

		it = gtk.RadioMenuItem (it, label=_("Marino"))
		it.connect ('activate', self.reset)
		self.menu.append (it)

		it = gtk.RadioMenuItem (it, label=_("Marino Mediterraneo"))
		it.connect ('activate', self.reset)
		self.menu.append (it)

		it = gtk.RadioMenuItem (it, label=_("Paludario"))
		it.connect ('activate', self.show_dolce)
		self.menu.append (it)

		it = gtk.RadioMenuItem (it, label=_("Salmastro"))
		it.connect ('activate', self.show_dolce)
		self.menu.append (it)
		
		self.menu.show_all ()
		self.view.connect ('button-press-event', self.on_btn)
	
	def on_btn (self, widget, evt):
		if evt.type == gtk.gdk.BUTTON_PRESS and evt.button == 3:
			self.menu.popup (None, None, None, evt.button, evt.time)
	
	def show_dolce (self, *w):
		self.reset ()
		self.view.get_column (8).set_visible (False)
		self.view.get_column (9).set_visible (False)
	
	def reset (self, *w):
		for i in range (len (self.col_lst)):
			self.view.get_column (i).set_visible (True)
		
	def aggiorna(self, widget):
		id = self.vars[0].get_active()

		for i in self.vars:
			self.reactivate (i)
		
		if id == 0 or id == 1: # Dolce || Dolce Tropicale
			# Reattore di calcio e Schiumatoio disabilitati
			self.deactivate (8, _("Assente"))
			self.deactivate (9, _("Assente"))
		elif id == 2 or id == 3: # Marino || Marino Mediterraneo
			pass
		elif id == 4 or id == 5: # Paludario
			self.deactivate (8, _("Assente"))
			self.deactivate (9, _("Assente"))
	
	def reactivate (self, widget):
		ret = widget.get_data ('old-value')

		if ret != None:
			widget.set_text (ret)

		widget.set_property ('sensitive', True)

	def deactivate (self, id, txt=None):
		self.vars[id].set_property ('sensitive', False)
		
		if txt != None:
			self.vars[id].set_data ('old-value', self.vars[id].get_text ())
			self.vars[id].set_text (txt)

	def after_refresh (self, it):
		mod, it = self.view.get_selection ().get_selected ()
		
		id = mod.get_value (it, 0)
		
		text  = self.vars[0].get_text ()
		date  = self.vars[1].get_text ()
		name  = self.vars[2].get_text ()
		litri = self.vars[3].get_text ()
		tacq  = self.vars[4].get_text ()
		tflt  = self.vars[5].get_text ()
		ico2  = self.vars[6].get_text ()
		illu  = self.vars[7].get_text ()
		reat  = self.vars[8].get_text ()
		schiu = self.vars[9].get_text ()
		risca = self.vars[10].get_text ()
		note  = self.vars[11].get_text ()
		img   = self.vars[12].get_text ()

		utils.cmd ("update vasca set vasca='%(text)s', date='%(date)s', nome='%(name)s', litri='%(litri)s', tipo='%(tacq)s', filtro='%(tflt)s', co='%(ico2)s', illuminazione='%(illu)s', reattore='%(reat)s', schiumatoio='%(schiu)s', riscaldamento='%(risca)s', note='%(note)s', img='%(img)s' where id = %(id)s" % vars())
		
		self.update_status (dbwindow.NotifyType.SAVE, _("Row aggiornata (ID: %d)") % id)

	def add_entry (self, it):
		mod, id = self.view.get_selection ().get_selected ()

		id = mod.get_value (it, 0)

		#for i in self.vars:
		#	print i.get_text ()
		
		utils.cmd ('insert into vasca values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
				id,
				self.vars[0].get_text (),
				self.vars[1].get_text (),
				self.vars[2].get_text (),
				self.vars[3].get_text (),
				self.vars[4].get_text (),
				self.vars[5].get_text (),
				self.vars[6].get_text (),
				self.vars[7].get_text (),
				self.vars[8].get_text (),
				self.vars[9].get_text (),
				self.vars[10].get_text (),
				self.vars[11].get_text (),
				self.vars[12].get_text ())
		
		self.update_status (dbwindow.NotifyType.ADD, _("Row aggiunta (ID: %d)") % id)
		
	def remove_id (self, id):
		utils.cmd ('delete from vasca where id=%d' % id)
		self.update_status (dbwindow.NotifyType.DEL, _("Row rimossa (ID: %d)") % id)
	
	def decrement_id (self, id):
		utils.cmd ("update vasca set id=%d where id=%d" % (id - 1, id))

	def on_row_activated(self, tree, path, col):
		mod = self.view.get_model()
		it = mod.get_iter_from_string(str(path[0]))

		utils.InfoDialog(self, _("Riepilogo"), self.col_lst, self.vars, mod.get_value (it, 14))
