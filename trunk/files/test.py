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
from pysqlite2 import dbapi2 as sqlite

class Test(gtk.Window):
	def __init__(self): 
		gtk.Window.__init__(self)
		
		self.set_title("Vasche")
		self.set_size_request(600, 400)
		
		box = gtk.VBox()
		# id integer, date DATE, vasca FLOAT, ph FLOAT, kh FLOAT, gh
		# NUMERIC, no NUMERIC, noo NUMERIC, con NUMERIC, amm NUMERIC, fe
		# NUMERIC, ra NUMERIC, fo NUMERIC
		self.test_store = gtk.ListStore(int, str, str, str, str, str, str, str, str, str, str, str, str)
		
		self.view = view = gtk.TreeView(self.test_store)
		
		lst = ['Id', 'Data', 'Vasca', 'Ph', 'Kh', 'Gh', 'No', 'No2',
		'Conducibilita\'', 'Ammoniaca', 'Ferro', 'Rame', 'Fosfati']
		renderer = gtk.CellRendererText()
		
		for i in lst:
			id = lst.index(i)
			col = gtk.TreeViewColumn(i, renderer, text=id)
			col.set_sort_column_id(id)
			col.set_clickable(True)
			col.set_resizable(True)
			view.append_column(col)
		
		view.get_selection().connect('changed', self.on_selection_changed)
		
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		
		sw.add(view)
		
		box.pack_start(sw)
		
		connessione=sqlite.connect(os.path.join('Data', 'db'))
		cursore=connessione.cursor()
		cursore.execute("select * from test")

		# Costruisci l'immagine..
		for y in cursore.fetchall():
			self.test_store.append([y[0], y[1], y[2], y[3], y[4],
			y[5], y[6], y[7], y[8], y[9], y[10], y[11], y[12]])
		
		
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
		tbl = gtk.Table(6, 4)
		tbl.set_col_spacings(4)
		
		tbl.attach(self.new_label("Data:"), 0, 1, 0, 1)
		tbl.attach(self.new_label("Vasca:"), 0, 1, 1, 2)
		tbl.attach(self.new_label("Ph:"), 0, 1, 2, 3)
		tbl.attach(self.new_label("Kh:"), 0, 1, 3, 4)
		tbl.attach(self.new_label("Gh:"), 0, 1, 4, 5)
		tbl.attach(self.new_label("No:"), 0, 1, 5, 6)
		
		tbl.attach(self.new_label("No2:"), 2, 3, 0, 1)
		tbl.attach(self.new_label("Conducibilita':"), 2, 3, 1, 2)
		tbl.attach(self.new_label("Ammoniaca:"), 2, 3, 2, 3)
		tbl.attach(self.new_label("Ferro"), 2, 3, 3, 4)
		tbl.attach(self.new_label("Rame"), 2, 3, 4, 5)
		tbl.attach(self.new_label("Fosfati"), 2, 3, 5, 6)

		def make_inst(num):
			a = list()
			for i in range(num):
				a.append(gtk.Entry())
			return a

		self.e_data, self.e_vasca, self.e_ph, self.e_kh = make_inst(4)
		self.e_gh, self.e_no, self.e_no2, self.e_cond = make_inst(4)
		self.e_ammo, self.e_ferro, self.e_rame, self.e_fosfati = make_inst(4)

		attach = lambda x, y, z: tbl.attach(x, 1, 2, y, z)

		attach(self.e_data, 0, 1)
		attach(self.e_vasca, 1, 2)
		attach(self.e_ph, 2, 3)
		attach(self.e_kh, 3, 4)
		attach(self.e_gh, 4, 5)
		attach(self.e_no, 5, 6)
		
		attach = lambda x, y, z: tbl.attach(x, 3, 4, y, z)
		
		attach(self.e_no2, 0, 1)
		attach(self.e_cond, 1, 2)
		attach(self.e_ammo, 2, 3)
		attach(self.e_ferro, 3, 4)
		attach(self.e_rame, 4, 5)
		attach(self.e_fosfati, 5, 6)

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
			id = int(self.test_store.get_value(it, 0))
			
			data = self.e_data.get_text()
			vasca = self.e_vasca.get_text()
			ph = self.e_ph.get_text()
			kh = self.e_kh.get_text()
			gh = self.e_gh.get_text()
			no = self.e_no.get_text()
			no2 = self.e_no2.get_text()
			cond = self.e_cond.get_text()
			ammo = self.e_ammo.get_text()
			ferro = self.e_ferro.get_text()
			rame = self.e_rame.get_text()
			fosfati = self.e_fosfati.get_text()
			
			conn = sqlite.connect(os.path.join('Data', 'db'))
			cur = conn.cursor()

		# id integer, date DATE, vasca FLOAT, ph FLOAT, kh FLOAT, gh
		# NUMERIC, no NUMERIC, noo NUMERIC, con NUMERIC, amm NUMERIC, fe
		# NUMERIC, ra NUMERIC, fo NUMERIC
			cur.execute("update test set date='%(data)s', vasca='%(vasca)s', ph='%(ph)s', kh='%(kh)s', gh='%(gh)s', no='%(no)s', noo='%(no2)s', con='%(cond)s', amm='%(ammo)s', fe='%(ferro)s', ra='%(rame)s', fo='%(fosfati)s' where id=%(id)s" %vars())
			conn.commit()

			self.test_store.set_value(it, 1, data)
			self.test_store.set_value(it, 2, vasca)
			self.test_store.set_value(it, 3, ph)
			self.test_store.set_value(it, 4, kh)
			self.test_store.set_value(it, 5, gh)
			self.test_store.set_value(it, 6, no)
			self.test_store.set_value(it, 7, no2)
			self.test_store.set_value(it, 8, cond)
			self.test_store.set_value(it, 9, ammo)
			self.test_store.set_value(it, 10, ferro)
			self.test_store.set_value(it, 11, rame)
			self.test_store.set_value(it, 12, fosfati)
			
			self.update_status(0, "Row aggiornata (ID: %d)" % id)

	def on_add(self, widget):
		mod = self.view.get_model()
		it = mod.get_iter_first()
		id = 0
		
		while it != None:
			tmp = int(self.test_store.get_value(it, 0))
			
			if tmp > id: id = tmp

			it = mod.iter_next(it)
		
		id += 1		
		it = self.test_store.append()

		# Settiamo il campo ID
		self.test_store.set_value(it, 0, id)

		data = self.e_data.get_text()
		vasca = self.e_vasca.get_text()
		ph = self.e_ph.get_text()
		kh = self.e_kh.get_text()
		gh = self.e_gh.get_text()
		no = self.e_no.get_text()
		no2 = self.e_no2.get_text()
		cond = self.e_cond.get_text()
		ammo = self.e_ammo.get_text()
		ferro = self.e_ferro.get_text()
		rame = self.e_rame.get_text()
		fosfati = self.e_fosfati.get_text()
		
		self.test_store.set_value(it, 1, data)
		self.test_store.set_value(it, 2, vasca)
		self.test_store.set_value(it, 3, ph)
		self.test_store.set_value(it, 4, kh)
		self.test_store.set_value(it, 5, gh)
		self.test_store.set_value(it, 6, no)
		self.test_store.set_value(it, 7, no2)
		self.test_store.set_value(it, 8, cond)
		self.test_store.set_value(it, 9, ammo)
		self.test_store.set_value(it, 10, ferro)
		self.test_store.set_value(it, 11, rame)
		self.test_store.set_value(it, 12, fosfati)
		
		conn = sqlite.connect(os.path.join('Data', 'db'))
		cur = conn.cursor()

		cur.execute('insert into test values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
			(id, data, vasca, ph, kh, gh, no, no2, cond, ammo, ferro, rame, fosfati))
		conn.commit()

		self.update_status(1, "Row aggiunta (ID: %d)" % id)
		
	def on_del(self, widget): 
		# prendiamo l'iter selezionato e elimianiamolo dalla store
		mod, it = self.view.get_selection().get_selected()

		if it != None:
			# Questo Ã¨ il valore da confrontare
			value = int(self.test_store.get_value(it, 0))

			# Rimuoviamo dal database
			conn = sqlite.connect(os.path.join('Data', 'db'))
			cur = conn.cursor()

			cur.execute('delete from test where id=%d' % value)
			conn.commit()

			# Rimuoviamo la riga selezionata
			self.test_store.remove(it)

			# Iteriamo tutte le righe per trovarne una con campo id
			# maggiore di value e modifichiamolo
			it = mod.get_iter_first()

			while it != None:
				tmp = int(self.test_store.get_value(it, 0))

				if value < tmp:
					self.test_store.set_value(it, 0, tmp-1)
					cur.execute("update test set id=%d where id=%d" % (tmp-1, tmp))
					conn.commit()
				it = mod.iter_next(it)

			self.update_status(2, "Row eliminata (ID: %d)" % value)

	def on_selection_changed(self, sel):
		# Aggiorniamo il contenuto delle entry in base alla selezione
		mod, it = sel.get_selected()
		
		if it != None:
			self.e_data.set_text(mod.get_value(it, 1))
			self.e_vasca.set_text(mod.get_value(it, 2))
			self.e_ph.set_text(mod.get_value(it, 3))
			self.e_kh.set_text(mod.get_value(it, 4))
			self.e_gh.set_text(mod.get_value(it, 5))
			self.e_no.set_text(mod.get_value(it, 6))
			self.e_no2.set_text(mod.get_value(it, 7))
			self.e_cond.set_text(mod.get_value(it, 8))
			self.e_ammo.set_text(mod.get_value(it, 9))
			self.e_ferro.set_text(mod.get_value(it, 10))
			self.e_rame.set_text(mod.get_value(it, 11))
			self.e_fosfati.set_text(mod.get_value(it, 12))
			
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
