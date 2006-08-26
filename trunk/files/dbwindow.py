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

class NotifyType:
	SAVE = 0
	ADD  = 1
	DEL  = 2

class DBWindow (gtk.Window):

	def __init__ (self, n_row, n_col, cols, widgets, lst_store, different_renderer=False):

		assert (len (cols) - 1 == len (widgets))
		
		# Inizializziamo la finestra
		gtk.Window.__init__ (self)

		self.vbox = gtk.VBox ()

		# Creiamo la store e la view
		self.store = lst_store
		self.view = gtk.TreeView (self.store)
		self.last = len (cols) + 1
		self.vars = widgets

		# Callback per la selection
		self.view.get_selection ().connect ('changed', self.on_selection_changed)
		self.view.connect ('row-activated', self.on_row_activated)

		#for i in range(len(cols)-1):
		#	print cols[i+1], widgets[i], lst_store.get_column_type(i+1)

		# Le Colonne ..
		
		if not different_renderer:
			renderer = gtk.CellRendererText ()
			pix_rend = gtk.CellRendererPixbuf()

		# i nomi sono in cols
		for name in cols:
			id = cols.index (name)
			
			#print "Adding %d" % id
			
			
			if self.store.get_column_type (id) == gobject.TYPE_DOUBLE:
				
				if different_renderer:
					renderer = gtk.CellRendererText ()
				
				self.view.insert_column_with_data_func (-1, name, renderer, self.float_func, id)
				
			else:
				col = None

				if self.store.get_column_type (id).pytype == gtk.gdk.Pixbuf:
				
					if different_renderer:
						pix_rend = gtk.CellRendererPixbuf()
						
					col = gtk.TreeViewColumn (name, pix_rend, pixbuf=id)
					self.last -= 1
				else:
				
					if different_renderer:
						renderer = gtk.CellRendererText ()
					
					col = gtk.TreeViewColumn (name, renderer, text=id)
				
				col.set_sort_column_id (id + 1)
				col.set_clickable (True)
				col.set_resizable (True)
				
				self.view.append_column (col)

		#print "Pixmap init at %d" % self.last

		# La ScrolledWindow
		self.sw = gtk.ScrolledWindow ()
		self.sw.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.sw.set_shadow_type (gtk.SHADOW_ETCHED_IN)

		# Pacchiamo
		self.sw.add (self.view)
		self.vbox.pack_start(self.sw)

		# La ButtonBox per le modifiche
		self.button_box = bb = gtk.HButtonBox ()
		bb.set_layout (gtk.BUTTONBOX_END)

		btn = gtk.Button (stock=gtk.STOCK_ADD)
		btn.set_relief (gtk.RELIEF_NONE)
		btn.connect ('clicked', self.on_add)
		bb.pack_start(btn)

		btn = gtk.Button (stock=gtk.STOCK_REFRESH)
		btn.set_relief (gtk.RELIEF_NONE)
		btn.connect ('clicked', self.on_refresh)
		bb.pack_start(btn)

		btn = gtk.Button (stock=gtk.STOCK_REMOVE)
		btn.set_relief (gtk.RELIEF_NONE)
		btn.connect ('clicked', self.on_remove)
		bb.pack_start(btn)
		
		hb = gtk.HBox (2, False)
		
		self.pack_before_button_box (hb)
		
		hb.pack_start (bb)
		
		self.vbox.pack_start(hb, False, False, 0)

		# Creiamo la zona editing
		edt_frame = gtk.Frame ("Editing:")
		edt_frame.set_shadow_type (gtk.SHADOW_ETCHED_IN)
		
		if not self.custom_page(edt_frame):
			self.vbox.pack_start (edt_frame, False, False, 0)
		
		# Eliminiamo la colonna id che nn ci serve
		cols.remove(cols[0])
		
		# Andiamo a creare la table per l'editing		
		self.table = e_tbl = gtk.Table (n_row, n_col)
		self.table.set_border_width (4)
		self.table.set_col_spacings (8)

		x, y = 0, 0

		for name in cols:
			# Se superiamo il limite ci spostiamo sull'altra colonna e resettiamo x
			
			idx = cols.index (name)
			tmp = self.vars[idx]

			#print "Creating e_%s at %d %d %d %d" % (name[:5], x, x+1, y, y+1)
			
			self.__dict__ ["e_" + name [:5]] = tmp
			e_tbl.attach (tmp, x+1, x+2, y, y+1)

			e_tbl.attach (utils.new_label (name, x=0, y=0.5), x, x+1, y, y+1, yoptions=gtk.SHRINK)

			if idx == n_col:
				x += 2; y = 0
			else:
				y += 1
		
		edt_frame.add (e_tbl)

		# Aggiungiamo la StatusBar
		self.status = gtk.Statusbar ()
		self.image = gtk.Image ()

		hbox = gtk.HBox ()
		hbox.pack_start (self.image, False, False)
		hbox.pack_start (self.status)
		
		self.vbox.pack_start (hbox, False, False, 0)

		self.add (self.vbox)
		self.show_all ()

		self.image.hide ()
		self.timeoutid = None

		self.connect ('delete-event', self.on_delete_event)
	
	def on_delete_event (self, widget, event):
		if self.timeoutid != None:
			gobject.source_remove (self.timeoutid)
	
	def float_func (self, col, cell, model, iter, id):
		value = model.get_value (iter, id)
		cell.set_property ("text", "%.2f" % value)
	
	def data_func (self, col, cell, model, iter, id):
		value = model.get_value (iter, id)
		cell.set_property ("text", value)
	
	def update_status (self, type, string):
		self.image.show ()

		if type == NotifyType.SAVE:
			self.image.set_from_stock (gtk.STOCK_SAVE, gtk.ICON_SIZE_MENU)
		if type == NotifyType.ADD:
			self.image.set_from_stock (gtk.STOCK_ADD, gtk.ICON_SIZE_MENU)
		if type == NotifyType.DEL:
			self.image.set_from_stock (gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)
	
		if self.timeoutid != None:
			gobject.source_remove(self.timeoutid)
			self.status.pop(0)

		self.status.push(0, string)

		self.timeoutid = gobject.timeout_add(2000, self.callback)

	def callback(self):
		self.image.hide()
		self.status.pop(0)

		self.timeoutid = None
		
		return False
	
	def on_selection_changed (self, treeselection):
		mod, it = treeselection.get_selected ()

		if it == None: return

		x = 0

		for i in self.vars:
			if self.store.get_column_type (self.vars.index (i) + 1).pytype == gtk.gdk.Pixbuf:
				#print "image is %s" % mod.get_value (it, self.last + x)
				i.set_text( mod.get_value (it, self.last + x))
				x += 1
			else:
				i.set_text( mod.get_value (it, self.vars.index (i) + 1))

		self.after_selection_changed (mod, it)
	
	def after_selection_changed (self, mod, it):
		pass

	def on_row_activated (self, tree, path, col):
		pass
	
	def on_add (self, widget):
		mod = self.store
		it = mod.get_iter_first ()
		id = 0

		while it != None:
			tmp = int (self.store.get_value (it, 0))

			if tmp > id: id = tmp

			it = mod.iter_next (it)

		id += 1
		it = self.store.append ()

		# Settiamo il campo ID e gli altri campi
		self.store.set_value (it, 0, id)
		x = 0
		
		for tmp in self.vars:
			if self.store.get_column_type (self.vars.index (tmp) + 1).pytype == gtk.gdk.Pixbuf:

				#print "col n %d => %s" % (self.last + x, tmp)
				
				self.store.set_value (it, self.last + x, tmp.get_text ())

				self.store.set_value (it, self.vars.index (tmp) + 1, utils.make_image (tmp.get_text ()))

				x += 1
			else:
				self.store.set_value (it, self.vars.index (tmp) + 1, tmp.get_text ())

		self.add_entry (it)
	
	def add_entry (self, it):
		# Aggiunge la entry nel database
		pass

	def on_refresh (self, widget):
		
		# Prendiamo l'iter e il modello dalla selezione		
		mod, it = self.view.get_selection ().get_selected ()
		
		# Se esiste una selezione aggiorniamo la row
		# in base al contenuto delle entry
		
		if it != None:
			#id = int (self.store.get_value (it, 0))
			x = 0

			for tmp in self.vars:
				if self.store.get_column_type (self.vars.index (tmp) + 1).pytype == gtk.gdk.Pixbuf:
					
					self.store.set_value (it, x + self.last, tmp.get_text ())
					
					self.store.set_value (it, self.vars.index (tmp) + 1, utils.make_image (tmp.get_text ()))
					
					x += 1
				else:
					self.store.set_value (it, self.vars.index (tmp) + 1, tmp.get_text ())

			self.after_refresh (it)
	
	def after_refresh (self, it):
		# Implementata dalla sovraclasse
		pass
			
	def on_remove (self, widget):
		
		# Prendiamo l'iter selezionato ed elimianiamolo dalla store
		mod, it = self.view.get_selection ().get_selected ()

		if it != None:
			# Questo e' il valore da confrontare
			value = int (self.store.get_value (it, 0))

			# Rimuoviamo dal database
			self.remove_id (value)

			# Rimuoviamo la riga selezionata
			self.store.remove (it)

			# Iteriamo tutte le righe per trovarne una con campo id
			# maggiore di value e modifichiamolo
			it = mod.get_iter_first ()

			while it != None:
				tmp = int (self.store.get_value (it, 0))

				if value < tmp:
					self.store.set_value (it, 0, tmp-1)
					self.decrement_id (tmp)
				
				it = mod.iter_next (it)
	
	def remove_id (self, id):
		# Passa l'id da rimuovere nel database
		pass
	def decrement_id (self, id):
		# cur.execute("update vasca set id=%d where id=%d" % (id-1, id))
		pass
	
	def pack_before_button_box (self, hb):
		pass
	
	def custom_page (self, edt_frame):
		return False

class Test(DBWindow):
	def __init__(self):
		# Per immagini prima le pixbuf e le stringhe alla fine
		lst = gtk.ListStore(int, str, str, gtk.gdk.Pixbuf, str)
		
		lst.append([1, "Francesco", "stringa",
				utils.make_image("prova.png"), "prova.png"])

		DBWindow.__init__(self, 2, 2, ["ID", "Nome", "Stringa", "Immagine"],
				[gtk.Entry(), gtk.Entry(), utils.ImgEntry()], lst)

	def remove_id (self, id):
		self.update_status(NotifyType.SAVE, "Immagine Rimossa! :)")

if __name__ == "__main__":
	Test()
	gtk.main ()
