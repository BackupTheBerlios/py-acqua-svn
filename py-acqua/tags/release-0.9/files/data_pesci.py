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
from pysqlite2 import dbapi2 as sqlite

class Data_Pesci(gtk.Window):
	def __init__(self): 
		gtk.Window.__init__(self)
		
		self.set_title(_("Database Pesci"))
		self.set_size_request(600, 400)
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		box = gtk.VBox()
		
		self.data_pesci_store = gtk.ListStore(int, str, str, str, gtk.gdk.Pixbuf)
		
		self.view = view = gtk.TreeView(self.data_pesci_store)
		
		lst = [_('Id'), _('Nome'), _('Famiglia'), _('Note')]
		renderer = gtk.CellRendererText()
		
		for i in lst:
			id = lst.index(i)
			col = gtk.TreeViewColumn(i, renderer, text=id)
			col.set_sort_column_id(id)
			col.set_clickable(True)
			col.set_resizable(True)
			view.append_column(col)
		
		# Aggiungiamo la colonna per le immagini della vasca
		col = gtk.TreeViewColumn(_("Immagine"), gtk.CellRendererPixbuf(), pixbuf=6)
		col.set_resizable(True)
		col.set_clickable(False)
		view.append_column(col)
		
		view.get_selection().connect('changed', self.on_selection_changed)
		view.connect('row-activated', self.on_row_activated)
		
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		
		sw.add(view)
		
		box.pack_start(sw)
		
		#connessione=sqlite.connect(os.path.join('Data', 'db'))
		#cursore=connessione.cursor()
		#cursore.execute("select * from data_pesci")

		# Costruisci l'immagine..
		#for y in cursore.fetchall():
		#	self.data_pesci_store.append([y[0], y[1], y[2], y[3],
		#	y[4], self.make_image(y[4])])
		
		
		frm = gtk.Frame(_("Editing:"))
		
		# Creiamo una buttonbox per contenere i bottoni di modifica
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		
		btn = gtk.Button(_('Cerca'))
		#btn.connect('clicked', self.on_cerca)
		bb.pack_start(btn)
		
		#btn = gtk.Button(stock=gtk.STOCK_REFRESH)
		#btn.connect('clicked', self.on_refresh)
		#bb.pack_start(btn)
		
		#btn = gtk.Button(stock=gtk.STOCK_REMOVE)
		#btn.connect('clicked', self.on_del)
		#bb.pack_start(btn)
		
		box.pack_start(bb, False, False, 0)
		box.pack_start(frm, False, False, 0)
		
		# Creiamo la table che verra contenuta nel frame
		tbl = gtk.Table(8, 2)
		
		tbl.attach(self.new_label(_("Nome:")), 0, 1, 0, 1)
		tbl.attach(self.new_label(_("Famiglia:")), 0, 1, 1, 2)
		#tbl.attach(self.new_label(_("Note:")), 0, 1, 2, 3)
		#tbl.attach(self.new_label(_("Immagine:")), 0, 1, 3, 4)
		
		self.e_nome = gtk.Entry()
		self.e_famiglia = gtk.Entry()
		#self.e_note = gtk.Entry()
		#self.e_path = gtk.Entry()

	#	self.e_path.set_property('editable', False)
		
		tbl.attach(self.e_nome, 1, 2, 0, 1)
		tbl.attach(self.e_famiglia, 1, 2, 1, 2)
		#tbl.attach(self.e_note, 1, 2, 2, 3)
		
		hbox = gtk.HBox()

	#	btn = gtk.Button(stock=gtk.STOCK_OPEN)
	#	btn.set_relief(gtk.RELIEF_NONE)
	#	btn.connect('clicked', self.on_browse)
		
	#	hbox.pack_start(self.e_path)
	#	hbox.pack_start(btn, False, False, 0)
		
		tbl.attach(hbox, 1, 2, 3, 4)

		tbl.set_border_width(10)
		
		frm.add(tbl)

		self.status = gtk.Statusbar()
		self.img = gtk.Image()
		
		hbox = gtk.HBox()
		hbox.pack_start(self.img, False, False, 0)
		hbox.pack_start(self.status)
		
		box.pack_start(hbox, False, False, 0)
		
		self.add(box)
		self.show_all()

		self.img.hide()
		self.timeoutid = None

		box.set_border_width(4)

	def on_refresh(self, widget):
		
		# Prendiamo l'iter e il modello dalla selezione
		
		mod, it = self.view.get_selection().get_selected()
		
		# Se esiste una selezione aggiorniamo la row
		# in base al contenuto delle entry
		
		if it != None:
			id = int(self.data_pesci_store.get_value(it, 0))
			
			nome = self.e_nome.get_text()
			famiglia = self.e_famiglia.get_text()
			note = self.e_note.get_text()
			img = self.e_path.get_text()
			
			conn = sqlite.connect(os.path.join('Data', 'db'))
			cur = conn.cursor()

			cur.execute("update data_pesci set nome='%(nome)s', famiglia='%(famiglia)s', note='%(note)s', img='%(img)s' where id = %(id)s" %vars())
			conn.commit()
			
			self.data_pesci_store.set_value(it, 1, nome)
			self.data_pesci_store.set_value(it, 2, famiglia)
			self.data_pesci_store.set_value(it, 3, note)
			self.data_pesci_store.set_value(it, 4, self.make_image(img))
			self.data_pesci_store.set_value(it, 5, img)

			self.update_status(0, _("Row aggiornata (ID: %d)") % id)

	def on_add(self, widget):
		mod = self.view.get_model()
		it = mod.get_iter_first()
		id = 0
		
		while it != None:
			tmp = int(self.data_pesci_store.get_value(it, 0))
			
			if tmp > id: id = tmp

			it = mod.iter_next(it)
		
		id += 1		
		it = self.data_pesci_store.append()

		# Settiamo il campo ID
		self.data_pesci_store.set_value(it, 0, id)

		nome = self.e_nome.get_text()
		famiglia = self.e_famiglia.get_text()
		note = self.e_note.get_text()
		img = self.e_path.get_text()
		
		self.data_pesci_store.set_value(it, 1, nome)
		self.data_pesci_store.set_value(it, 2, famiglia)
		self.data_pesci_store.set_value(it, 3, note)
		self.data_pesci_store.set_value(it, 4, img)
		self.data_pesci_store.set_value(it, 5, self.make_image(img))
		
		conn = sqlite.connect(os.path.join('Data', 'db'))
		cur = conn.cursor()

		cur.execute('insert into data_pesci values(?,?,?,?,?)',
			(id, nome, famiglia, note, img))
		conn.commit()

		self.update_status(1, _("Row aggiunta (ID: %d)") % id)
		
	def on_del(self, widget): 
		# prendiamo l'iter selezionato e elimianiamolo dalla store
		mod, it = self.view.get_selection().get_selected()

		if it != None:
			# Questo Ã¨ il valore da confrontare
			value = int(self.data_pesci_store.get_value(it, 0))

			# Rimuoviamo dal database
			conn = sqlite.connect(os.path.join('Data', 'db'))
			cur = conn.cursor()

			cur.execute('delete from data_pesci where id=%d' % value)
			conn.commit()

			# Rimuoviamo la riga selezionata
			self.data_pesci_store.remove(it)

			# Iteriamo tutte le righe per trovarne una con campo id
			# maggiore di value e modifichiamolo
			it = mod.get_iter_first()

			while it != None:
				tmp = int(self.data_pesci_store.get_value(it, 0))

				if value < tmp:
					self.data_pesci_store.set_value(it, 0, tmp-1)
				it = mod.iter_next(it)

			self.update_status(2, _("Row eliminata (ID: %d)") % value)

	def on_selection_changed(self, sel):
		# Aggiorniamo il contenuto delle entry in base alla selezione
		mod, it = sel.get_selected()
		
		if it != None:
			self.e_nome.set_text(mod.get_value(it, 1))
			self.e_famiglia.set_text(mod.get_value(it, 2))
			self.e_note.set_text(mod.get_value(it, 3))
			self.e_path.set_text(mod.get_value(it, 4))
			
	def on_row_activated(self, tree, path, col):
		mod = self.view.get_model()
		it = mod.get_iter_from_string(str(path[0]))

		#InfoDialog(self, mod, it)
	
	def on_browse(self, widget):
		dialog = gtk.FileChooserDialog(_("Aggiungi foto"), self,
			buttons=(gtk.STOCK_OK, gtk.RESPONSE_OK,
			gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
		dialog.set_use_preview_label(False)

		img = gtk.Image()
		
		dialog.set_preview_widget(img)
		dialog.set_size_request(128, -1)

		# Creiamo i filtri

		filter = gtk.FileFilter()
		filter.set_name(_("Immagini"))
		filter.add_mime_type("image/png")
		filter.add_mime_type("image/jpeg")
		filter.add_mime_type("image/gif")
		filter.add_pattern("*.png")
		filter.add_pattern("*.jpg")
		filter.add_pattern("*.gif")
		dialog.add_filter(filter)
		
		dialog.connect('update-preview', self.on_update_preview)

		id = dialog.run()

		dialog.hide()

		if id == gtk.RESPONSE_OK:
			name = dialog.get_filename()

			img_dir = os.path.join(os.path.abspath(os.getcwd()), "Immagini")
			img_dir = os.path.join(img_dir, os.path.basename(name))

			if img_dir != name:
				try:
					import shutil
					shutil.copy(name, 'Immagini/')
				except:
					print _("Errore mentre copiavo (%s)") % sys.exc_value
			self.e_path.set_text(os.path.basename(name))

		dialog.destroy()

	def on_update_preview(self, chooser):
		uri = chooser.get_uri()
		try:
			pixbuf = gtk.gdk.pixbuf_new_from_file(uri[7:])
			
			w, h = make_thumb(50, pixbuf.get_width(), pixbuf.get_height())
			pixbuf = pixbuf.scale_simple(w, h, gtk.gdk.INTERP_BILINEAR)
			
			chooser.get_preview_widget().set_from_pixbuf(pixbuf)
		except:
			chooser.get_preview_widget().set_from_stock(gtk.STOCK_DIALOG_QUESTION,
				gtk.ICON_SIZE_DIALOG)
		
		chooser.set_preview_widget_active(True)
	
	def new_label(self, txt):
		lbl = gtk.Label()
		lbl.set_use_markup(True)
		lbl.set_label('<b>' + txt + '</b>')
		lbl.set_alignment(0.0, 0.5)
		
		return lbl
		
	def make_image(self, name):
		try:
			pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join('Immagini', name))
			w, h = make_thumb(50, pixbuf.get_width(), pixbuf.get_height())
			return pixbuf.scale_simple(w, h, gtk.gdk.INTERP_HYPER)
		except:
			return None
	
	def update_status(self, type, txt):
		self.img.show()
		
		if type == 0:
			self.img.set_from_stock(gtk.STOCK_SAVE, gtk.ICON_SIZE_MENU)
		if type == 1:
			self.img.set_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_MENU)
		if type == 2:
			self.img.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)
		
		if self.timeoutid != None:
			gobject.source_remove(self.timeoutid)
			self.status.pop(0)

		self.status.push(0, txt)

		self.timeoutid = gobject.timeout_add(2000, self.callback)
	
	def callback(self):
		self.img.hide()
		self.status.pop(0)

		self.timeoutid = None
		
		return False
		
def make_thumb(twh, w, h):
	if w == h:
		return twh, twh
	if w < h:
		y = twh
		x = int(float(y*w)/float(h))
		return x, y
	if w > h:
		x = twh
		y = int(float(x*h)/float(w))
		return x, y
