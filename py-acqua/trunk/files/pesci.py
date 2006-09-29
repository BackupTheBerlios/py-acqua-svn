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

class Pesci (dbwindow.DBWindow):
	def __init__(self):
		
		lst = gtk.ListStore (int, str, str, int, str, str, gtk.gdk.Pixbuf, str)
		self.col_lst = [_('Id'), _('Data'), _('Vasca'), _('Quantita'), _('Nome'), _('Note'), _("Immagine")]
		
		dbwindow.DBWindow.__init__ (self, 2, 2, self.col_lst,
			[utils.DataButton (), utils.Combo (), utils.IntEntry (), gtk.Entry (), utils.NoteEntry (), utils.ImgEntry ()], lst)
		
		for y in utils.get ("select * from pesci"):
			lst.append ([y[0], y[1], y[2], y[3], y[4], y[5], utils.make_image(y[6]), y[6]])
		for y in utils.get ("select * from vasca"):
			self.vars[1].append_text (y[3])
		
		
		self.set_title (_("Pesci"))
		self.set_size_request (600, 400)
		
		utils.set_icon (self)

		self.menu = gtk.Menu ()

		for y in utils.get ('select * from vasca'):
			w = gtk.CheckMenuItem (y[3])
			w.set_property ("active", True)
			self.menu.append (w)

		self.filter = lst.filter_new ()
		self.filter.set_visible_func (self.apply_filter)
		self.view.set_model (self.filter)
		
		self.note.set_current_page(0)

	def after_refresh (self, it):
		mod, it = self.view.get_selection().get_selected()
		
		id = mod.get_value (it, 0)
		
		date = self.vars[0].get_text ()
		vasca = self.vars[1].get_text ()
		quantita = self.vars[2].get_text ()
		nome = self.vars[3].get_text ()
		note = self.vars[4].get_text ()
		img = self.vars[5].get_text ()
		
		utils.cmd ("update pesci set date='%(date)s', vasca='%(vasca)s', quantita='%(quantita)s', nome='%(nome)s', note='%(note)s', img='%(img)s' where id = %(id)s" % vars ())
		
		self.update_status (dbwindow.NotifyType.SAVE, _("Row aggiornata (ID: %d)") % id)

	def add_entry (self, it):
		mod = self.store

		id = mod.get_value (it, 0)

		for i in self.vars:
			print i.get_text ()
		
		utils.cmd ('insert into pesci values(?,?,?,?,?,?,?)',
				id,
				self.vars[0].get_text (),
				self.vars[1].get_text (),
				self.vars[2].get_text (),
				self.vars[3].get_text (),
				self.vars[4].get_text (),
				self.vars[5].get_text ())
		
		self.update_status (dbwindow.NotifyType.ADD, _("Row aggiunta (ID: %d)") % id)
		
	def remove_id (self, id):
		utils.cmd ('delete from pesci where id=%d' % id)
		self.update_status (dbwindow.NotifyType.DEL, _("Row rimossa (ID: %d)") % id)
	
	def decrement_id (self, id):
		utils.cmd ("update pesci set id=%d where id=%d" % (id - 1, id))
			
	def on_row_activated(self, tree, path, col):
		mod = self.view.get_model()
		it = mod.get_iter_from_string(str(path[0]))

		utils.InfoDialog(self, _("Riepilogo"), self.col_lst, self.vars, mod.get_value (it, 6))

	def pack_before_button_box (self, hb):
		cmb = utils.Combo ()
		cmb.append_text (_("Modifica"))
		cmb.append_text (_("Spesa"))
		cmb.set_active (0)
		cmb.connect ('changed', self.on_change_view)
		align = gtk.Alignment (0, 0.5)
		align.add (cmb)
		hb.pack_start (align, False, True, 0)
		cmb.show ()
		
		# Creiamo un filtro
		btn = utils.new_button (_("Filtro"), gtk.STOCK_APPLY)
		btn.set_relief (gtk.RELIEF_NONE)

		btn.connect ("clicked", self.apply)
		btn.connect ("button_press_event", self.on_popup)
		
		alg = gtk.Alignment (1, 0.5)
		alg.add (btn)

		hb.pack_start (alg, False, True, 0)
	def on_change_view (self, widget):
		id = widget.get_active ()
		
		if id == 1:
			#self.on_popup
			self.note.set_current_page (id)
		else:
			self.note.set_current_page (id)
			#self.on_popup
	def custom_page (self, edt_frame):
		import files.spesa
		
		self.note = gtk.Notebook ()
		self.vbox.pack_start (self.note, False, False, 0)
		
		self.note.set_show_tabs (False)
		self.note.set_show_border (False)
		self.note.append_page (edt_frame)
		
		
		self.note.append_page (files.spesa.Spesa ())
		#self.on_popup
		# C'e' la custom page qui :P
		return True
	def apply (self, widget):
		self.filter.refilter ()

	def apply_filter (self, mod, iter):
		filters = list ()

		for i in self.menu.get_children ():
			if i.active:
				filters.append (i.get_children ()[0].get_text ())
		print filters
		val = mod.get_value (iter, 2)
		print val
		
		if val in filters:
			return True
		else:
			return False

	def on_popup (self, widget, event):
		if event.button == 3:
			self.menu.popup (None, None, None, event.button, event.time)
			self.menu.show_all ()
