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
import datetime
from pysqlite2 import dbapi2 as sqlite

class Fertilizzante(gtk.Window):
	def __init__(self): 
		gtk.Window.__init__(self)
		
		self.set_title("Fertilizzante")
		self.set_size_request(600, 400)
		
		box = gtk.VBox()

		# id integer,date DATE, nome TEXT, quantita FLOAT, giorni NUMERIC
		self.fert_store = gtk.ListStore(int, str, str, float, str)
		self.view = view = gtk.TreeView(self.fert_store)
		
		lst = ['Id', 'Data', 'Nome', 'Quantita\'', 'Prossima volta']
		renderer = gtk.CellRendererText()

		for i in lst:
			id = lst.index(i)
			
			if id == 3:
				view.insert_column_with_data_func(-1, i, renderer, self.row_func, id)
			else:
				col = gtk.TreeViewColumn(i, renderer, text=id)
				col.set_sort_column_id(id+1)
				col.set_clickable(True)
				col.set_resizable(True)
				view.append_column(col)
				
		self.view.get_selection().connect('changed', self.on_selection_changed)
		
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		
		sw.add(view)
		
		box.pack_start(sw)
		
		connessione=sqlite.connect(os.path.join('Data', 'db'))
		cursore=connessione.cursor()
		cursore.execute("select * from fertilizzante")

		# Costruisci l'immagine..
		for y in cursore.fetchall():
			self.fert_store.append([y[0], y[1], y[2], y[3], y[4]])
			
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
		tbl = gtk.Table(8, 2)
		
		tbl.attach(self.new_label("Data:"), 0, 1, 0, 1)
		tbl.attach(self.new_label("Nome:"), 0, 1, 1, 2)
		tbl.attach(self.new_label("Quantita:"), 0, 1, 2, 3)
		tbl.attach(self.new_label("Prossima volta:"), 0, 1, 3, 4)
		
		
		self.fe_data, self.fe_nome = utils.DataButton(), gtk.Entry()
		self.fe_quantita = utils.FloatEntry()
		self.fe_prossima = utils.DataButton()
		
		tbl.attach(self.fe_data, 1, 2, 0, 1)
		tbl.attach(self.fe_nome, 1, 2, 1, 2)
		tbl.attach(self.fe_quantita, 1, 2, 2, 3)
		tbl.attach(self.fe_prossima, 1, 2, 3, 4)
		
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
	
	def set_prossima(self, days):
		try:
			data = self.fe_data.get_date()
			data = datetime.datetime(data[0], data[1], data[2])
			data = data + datetime.timedelta(int(days))
			self.fe_prossima.set_label("%02d/%02d/%04d" % (data.day, data.month, data.year))
		except:
			pass
	
	def get_prossima(self):
		data_o = self.fe_data.get_date()
		data = self.fe_prossima.get_date()
		
		data_o = datetime.datetime(data_o[0], data_o[1], data_o[2])
		data = datetime.datetime(data[0], data[1], data[2])

		delta = data - data_o

		return delta.days
	
	def row_func(self, col, cell, model, iter, id):
		value = model.get_value(iter, id)
		cell.set_property("text", "%.2f" % value)

	def on_refresh(self, widget):
		
		# Prendiamo l'iter e il modello dalla selezione
		
		mod, it = self.view.get_selection().get_selected()
		
		# Se esiste una selezione aggiorniamo la row
		# in base al contenuto delle entry
		
		if it != None:
			id = int(self.fert_store.get_value(it, 0))
			
			date = self.fe_data.get_text()
			nome = self.fe_nome.get_text()
			quantita = self.fe_quantita.get_text()
			giorni = self.fe_prossima.get_text()
			
			
			conn = sqlite.connect(os.path.join('Data', 'db'))
			cur = conn.cursor()

			cur.execute("update fertilizzante set date='%(date)s', nome='%(nome)s', quantita='%(quantita)s', giorni='%(giorni)s' where id=%(id)s" %vars())
			conn.commit()
			
			self.fert_store.set_value(it, 1, date)
			self.fert_store.set_value(it, 2, nome)
			self.fert_store.set_value(it, 3, quantita)
			self.fert_store.set_value(it, 4, giorni)
			

			self.update_status(0, "Row aggiornata (ID: %d)" % id)

	def on_add(self, widget):
		# Aggiungiamo dei valori casuali che andranno subito ad essere modificati
		# dall'utente
		mod = self.view.get_model()
		it = mod.get_iter_first()
		id = 0
		
		while it != None:
			tmp = int(self.fert_store.get_value(it, 0))
			
			if tmp > id: id = tmp

			it = mod.iter_next(it)
		
		id += 1		
		it = self.fert_store.append()

		# Settiamo il campo ID
		self.fert_store.set_value(it, 0, id)
		
		date = self.fe_data.get_text()
		nome = self.fe_nome.get_text()
		quantita = self.fe_quantita.get_text()
		giorni = self.fe_prossima.get_text()

		
		
		self.fert_store.set_value(it, 1, date)
		self.fert_store.set_value(it, 2, nome)
		self.fert_store.set_value(it, 3, quantita)
		self.fert_store.set_value(it, 4, giorni)
		
		
		conn = sqlite.connect(os.path.join('Data', 'db'))
		cur = conn.cursor()

		cur.execute('insert into fertilizzante values(?,?,?,?,?)',
			(id, date, nome, quantita, giorni))
		conn.commit()

		self.update_status(1, "Row aggiunta (ID: %d)" % id)
		
	def on_del(self, widget): 
		# prendiamo l'iter selezionato e elimianiamolo dalla store
		mod, it = self.view.get_selection().get_selected()

		if it != None:
			# Questo Ã¨ il valore da confrontare
			value = int(self.fert_store.get_value(it, 0))

			# Rimuoviamo dal database
			conn = sqlite.connect(os.path.join('Data', 'db'))
			cur = conn.cursor()

			cur.execute('delete from fertilizzante where id=%d' % value)
			conn.commit()

			# Rimuoviamo la riga selezionata
			self.fert_store.remove(it)

			# Iteriamo tutte le righe per trovarne una con campo id
			# maggiore di value e modifichiamolo
			it = mod.get_iter_first()

			while it != None:
				tmp = int(self.fert_store.get_value(it, 0))

				if value < tmp:
					self.fert_store.set_value(it, 0, tmp-1)
					cur.execute("update fertilizzante set id=%d where id=%d" % (tmp-1, tmp))
					conn.commit()
				it = mod.iter_next(it)

			self.update_status(2, "Row eliminata (ID: %d)" % value)

	def on_selection_changed(self, sel):
		# Aggiorniamo il contenuto delle entry in base alla selezione
		mod, it = sel.get_selected()
		
		if it != None:
			
			self.fe_data.set_text(mod.get_value(it, 1))
			self.fe_nome.set_text(mod.get_value(it, 2))
			self.fe_quantita.set_text(mod.get_value(it, 3))
			self.fe_prossima.set_text(mod.get_value(it, 4))
			
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
