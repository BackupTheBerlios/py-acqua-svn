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

class Filtro(gtk.Window):
	def __init__(self): 
		gtk.Window.__init__(self)
		
		self.set_title("Filtro")
		self.set_size_request(600, 400)
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		box = gtk.VBox()
		
		
		#sw = gtk.ScrolledWindow()
		#sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		#sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)

		self.fert_store = gtk.ListStore(int, str, str, float, str)
		self.view = view = gtk.TreeView(self.fert_store)
		
		self.filtro_store = gtk.ListStore(int, str, str)
		self.view = view = gtk.TreeView(self.filtro_store)
		
		lst = ['Id', 'Data', 'Prossima volta']
		renderer = gtk.CellRendererText()

		for i in lst:
			id = lst.index(i)
			col = gtk.TreeViewColumn(i, renderer, text=id)
			col.set_sort_column_id(id+1)
			col.set_clickable(True)
			col.set_resizable(True)
			view.append_column(col)

		
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		
		sw.add(view)
		
		box.pack_start(sw)
		
		connessione=sqlite.connect(os.path.join('Data', 'db'))
		cursore=connessione.cursor()
		cursore.execute("select * from filtro")

		# Costruisci l'immagine..
		for y in cursore.fetchall():
			self.filtro_store.append([y[0], y[1], y[2]])
			
		
		
		frm = gtk.Frame("Editing:")
		
		# Creiamo una buttonbox per contenere i bottoni di modifica
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		
		btn = gtk.Button(stock=gtk.STOCK_ADD)
		btn.connect('clicked', self.on_add)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_REFRESH)
		btn.connect('clicked', self.on_refresh)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_REMOVE)
		btn.connect('clicked', self.on_del)
		bb.pack_start(btn)
		
		box.pack_start(bb, False, False, 0)
		box.pack_start(frm, False, False, 0)
		
		# Creiamo la table che verra contenuta nel frame
		tbl = gtk.Table(2, 2)
		
		tbl.attach(self.new_label("Data:"), 0, 1, 0, 1)
		tbl.attach(self.new_label("Prossima volta:"), 0, 1, 1, 2)
		
		
		self.fi_data, self.fi_giorni = utils.DataButton(), utils.DataButton()
		
		tbl.attach(self.fi_data, 1, 2, 0, 1)
		tbl.attach(self.fi_giorni, 1, 2, 1, 2)
		
		frm.add(tbl)

		self.status = gtk.Statusbar()
		self.img = gtk.Image()
		
		hbox = gtk.HBox()
		hbox.pack_start(self.img, False, False, 0)
		hbox.pack_start(self.status)
		
		box.pack_start(hbox, False, False, 0)
		
		self.add(box)
		self.show_all()
		
		self.connect('delete-event', self.on_delete_event)

		self.img.hide()
		self.timeoutid = None

		box.set_border_width(4)

	def on_refresh(self, widget):
		
		# Prendiamo l'iter e il modello dalla selezione
		
		mod, it = self.view.get_selection().get_selected()
		
		# Se esiste una selezione aggiorniamo la row
		# in base al contenuto delle entry
		
		if it != None:
			id = int(self.filtro_store.get_value(it, 0))
			
			date = self.fi_data.get_text()
			giorni = self.fi_giorni.get_text()
			
			
			conn = sqlite.connect(os.path.join('Data', 'db'))
			cur = conn.cursor()

			cur.execute("update fertilizzante set date='%(date)s', giorni='%(giorni)s'" %vars())
			conn.commit()
			
			self.filtro_store.set_value(it, 1, date)
			self.filtro_store.set_value(it, 2, giorni)
			

			self.update_status(0, "Row aggiornata (ID: %d)" % id)

	def on_add(self, widget):
		# Aggiungiamo dei valori casuali che andranno subito ad essere modificati
		# dall'utente
		mod = self.view.get_model()
		it = mod.get_iter_first()
		id = 0
		
		while it != None:
			tmp = int(self.filtro_store.get_value(it, 0))
			
			if tmp > id: id = tmp

			it = mod.iter_next(it)
		
		id += 1		
		it = self.filtro_store.append()

		# Settiamo il campo ID
		self.filtro_store.set_value(it, 0, id)
		
		date = self.fi_data.get_text()
		giorni = self.fi_giorni.get_text()
		
		
		
		self.filtro_store.set_value(it, 1, date)
		self.filtro_store.set_value(it, 2, giorni)
		
		
		conn = sqlite.connect(os.path.join('Data', 'db'))
		cur = conn.cursor()

		cur.execute('insert into filtro values(?,?,?)',
			(id, date, giorni))
		conn.commit()

		self.update_status(1, "Row aggiunta (ID: %d)" % id)
		
	def on_del(self, widget): 
		# prendiamo l'iter selezionato e elimianiamolo dalla store
		mod, it = self.view.get_selection().get_selected()

		if it != None:
			# Questo Ã¨ il valore da confrontare
			value = int(self.filtro_store.get_value(it, 0))

			# Rimuoviamo dal database
			conn = sqlite.connect(os.path.join('Data', 'db'))
			cur = conn.cursor()

			cur.execute('delete from filtro where id=%d' % value)
			conn.commit()

			# Rimuoviamo la riga selezionata
			self.filtro_store.remove(it)

			# Iteriamo tutte le righe per trovarne una con campo id
			# maggiore di value e modifichiamolo
			it = mod.get_iter_first()

			while it != None:
				tmp = int(self.filtro_store.get_value(it, 0))

				if value < tmp:
					self.filtro_store.set_value(it, 0, tmp-1)
					cur.execute("update filtro set id=%d where id=%d" % (tmp-1, tmp))
					conn.commit()
				it = mod.iter_next(it)

			self.update_status(2, "Row eliminata (ID: %d)" % value)

	def on_selection_changed(self, sel):
		# Aggiorniamo il contenuto delle entry in base alla selezione
		mod, it = sel.get_selected()
		
		if it != None:
			
			self.fi_data.set_text(mod.get_value(it, 1))
			self.fi_giorni.set_text(mod.get_value(it, 2))
			
			
	def on_row_activated(self, tree, path, col):
		mod = self.view.get_model()
		it = mod.get_iter_from_string(str(path[0]))

		InfoDialog(self, mod, it)
	

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
	
	def on_delete_event(self, widget, event):
		if self.timeoutid != None:
			gobject.source_remove(self.timeoutid)
	
	def new_label(self, txt):
		lbl = gtk.Label()
		lbl.set_use_markup(True)
		lbl.set_label('<b>' + txt + '</b>')
		lbl.set_alignment(0.0, 0.5)
		
		return lbl
		
	
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

class InfoDialog(gtk.Dialog):
	def __init__(self, parent, mod, it):
		gtk.Dialog.__init__(self, "Riepilogo", parent,
			gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_OK))

		self.set_size_request(400, 300)
		self.vbox.set_border_width(10)

		self.set_has_separator(False)
		
		tbl = gtk.Table(7, 2)
		tbl.set_border_width(4)
		
		img = gtk.Image();
		
		try:
			img.set_from_file(os.path.join('Immagini',
				str(mod.get_value(it, 9))))
		except:
			img.set_from_stock(gtk.STOCK_IMAGE_MISSING,
				gtk.ICON_SIZE_DIALOG)
		
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

		sw.add_with_viewport(img)

		self.vbox.pack_start(sw)
		
		tbl.attach(self.new_label("Vasca:"), 0, 1, 0, 1)
		tbl.attach(self.new_label("Data:"), 0, 1, 1, 2)
		tbl.attach(self.new_label("Nome:"), 0, 1, 2, 3)
		tbl.attach(self.new_label("Tipo Acquario:"), 0, 1, 3, 4)
		tbl.attach(self.new_label("Tipo Filtro:"), 0, 1, 4, 5)
		tbl.attach(self.new_label("Impianto Co2:"), 0, 1, 5, 6)
		tbl.attach(self.new_label("Illuminazione:"), 0, 1, 6, 7)

		attach = lambda t, x, y: tbl.attach(gtk.Label(str(x)), 1, 2, x, y)
		
		attach(mod.get_value(it, 1), 0, 1)
		attach(mod.get_value(it, 2), 1, 2)
		attach(mod.get_value(it, 3), 2, 3)
		attach(mod.get_value(it, 4), 3, 4)
		attach(mod.get_value(it, 5), 4, 5)
		attach(mod.get_value(it, 6), 5, 6)
		attach(mod.get_value(it, 7), 6, 7)
		
		self.vbox.pack_start(tbl, False, False, 0)
		self.show_all()

		self.connect('response', self.on_response)
	
	def new_label(self, txt):
		lbl = gtk.Label()
		lbl.set_use_markup(True)
		lbl.set_label('<b>' + txt + '</b>')
		lbl.set_alignment(0.0, 0.5)
		
		return lbl
		
	def on_response(self, dial, id):
		if id == gtk.RESPONSE_OK:
			self.hide()
			self.destroy()

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
