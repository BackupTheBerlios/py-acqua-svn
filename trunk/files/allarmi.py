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
import os
import impostazioni

from inserisci import *
from pysqlite2 import dbapi2 as sqlite

class Allarmi(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		
		self.set_title('Allarmi')

		vbox = gtk.VBox()

		nb = gtk.Notebook()

		# Aggiungiamo i tab
		self.ph = self.gh = self.no2 = self.no3 = self.cond = None
		self.ammoniaca = self.ferro = self.rame = self.fosfati = None

		nb.append_page(self.make_test_page(), gtk.Label('Test'))
		nb.append_page(self.make_fert_page(), gtk.Label('Fertilizzante'))
		nb.append_page(self.make_filt_page(), gtk.Label('Filtro'))
		
		vbox.pack_start(nb)

		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)

		btn = gtk.Button(stock=gtk.STOCK_CLOSE)
		btn.connect('clicked', self.exit)

		bb.pack_start(btn)

		btn = gtk.Button(stock=gtk.STOCK_REFRESH)
		btn.connect('clicked', self.refresh)
		
		bb.pack_start(btn)

		vbox.pack_start(bb, False, False, 0)
		
		self.add(vbox)
		self.show_all()

		self.set_size_request(400, 300)
		self.refresh(None)
		
	def refresh(self, widget):
		
		impostazioni.refresh()
		
		con = sqlite.connect(os.path.join('Data', 'db'))
		cur = con.cursor()
		cur.execute('select * from test')
		
		for x in cur.fetchall():
			if x[1] < float(impostazioni.minph): self.ph.set_label('Ph basso')
			if x[1] > float(impostazioni.maxph): self.ph.set_label('Ph alto')
			else: self.ph.set_label('Ph ok')

			if x[1] < float(impostazioni.minkh): self.kh.set_label('Kh basso')
			if x[1] > float(impostazioni.maxkh): self.kh.set_label('Kh alto')
			else: self.kh.set_label('Kh ok')

			if x[1] < float(impostazioni.mingh): self.gh.set_label('Gh basso')
			if x[1] > float(impostazioni.maxgh): self.gh.set_label('Gh alto')
			else: self.gh.set_label('Gh ok')

			if x[1] < float(impostazioni.minno2): self.no2.set_label('No2 bassi')
			if x[1] > float(impostazioni.maxno2): self.no2.set_label('No2 alti')
			else: self.no2.set_label('No2 ok')

			if x[1] < float(impostazioni.minno3): self.no3.set_label('No3 bassi')
			if x[1] > float(impostazioni.maxno3): self.no3.set_label('No3 alti')
			else: self.no3.set_label('No3 ok')

			if x[1] < float(impostazioni.mincon): self.cond.set_label('Conducibilita\' bassa')
			if x[1] > float(impostazioni.maxcon): self.cond.set_label('Conducibilita\' alta')
			else: self.cond.set_label('Conducibilita\' ok')

			if x[1] < float(impostazioni.minam):	self.ammoniaca.set_label('Ammoniaca bassa')
			if x[1] > float(impostazioni.maxam): self.ammoniaca.set_label('Ammoniaca alta')
			else: self.ammoniaca.set_label('Ammoniaca ok')

			if x[1] < float(impostazioni.minfe): self.ferro.set_label('Ferro basso')
			if x[1] > float(impostazioni.maxfe): self.ferro.set_label('Ferro alto')
			else: self.ferro.set_label('Ferro ok')

			if x[1] < float(impostazioni.minra): self.rame.set_label('Rame basso')
			if x[1] > float(impostazioni.maxra): self.rame.set_label('Rame alto')
			else: self.rame.set_label('Rame ok')

			if x[1] < float(impostazioni.minfo): self.fosfati.set_label('Fosfati bassi')
			if x[1] > float(impostazioni.maxfo): self.fosfati.set_label('Fosfati alti')
			else: self.fosfati.set_label('Fosfati ok')
		
		# Popoliamo i fertilizzanti
		cur.execute('select * from fertilizzante')

		for i in cur.fetchall():
			self.fert_store.append([i[0], i[1], i[2], i[3], i[4]])

		# Popoliamo i filtri
		cur.execute('select * from filtro')

		for i in cur.fetchall():
			self.filt_store.append([i[0], i[1], i[2]])

	def make_filt_page(self):
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)

		self.filt_store = gtk.ListStore(int, str, str, float, str)
		view = gtk.TreeView(self.filt_store)
		
		lst = ['Id', 'Data', 'Prossima volta']
		renderer = gtk.CellRendererText()

		for i in lst:
			id = lst.index(i)
			col = gtk.TreeViewColumn(i, renderer, text=id)
			col.set_sort_column_id(id+1)
			col.set_clickable(True)
			col.set_resizable(True)
			view.append_column(col)

		sw.add(view)

		return sw
		
	def make_fert_page(self):
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)

		self.fert_store = gtk.ListStore(int, str, str, float, str)
		view = gtk.TreeView(self.fert_store)
		
		lst = ['Id', 'Data', 'Nome', 'Quantita\'', 'Prossima volta']
		renderer = gtk.CellRendererText()

		for i in lst:
			id = lst.index(i)
			col = gtk.TreeViewColumn(i, renderer, text=id)
			col.set_sort_column_id(id+1)
			col.set_clickable(True)
			col.set_resizable(True)
			view.append_column(col)

		sw.add(view)

		return sw
		
	def make_test_page(self):
		# Pagina Test
		tbl = gtk.Table(10, 2)
		tbl.set_border_width(5)
		
		tbl.attach(self.new_label('Ph'), 0, 1, 0, 1)
		tbl.attach(self.new_label('Kh'), 0, 1, 1, 2)
		tbl.attach(self.new_label('Gh'), 0, 1, 2, 3)
		tbl.attach(self.new_label('No2'), 0, 1, 3, 4)
		tbl.attach(self.new_label('No3'), 0, 1, 4, 5)
		tbl.attach(self.new_label('Conducibilità'), 0, 1, 5, 6)
		tbl.attach(self.new_label('Ammoniaca'), 0, 1, 6, 7)
		tbl.attach(self.new_label('Ferro'), 0, 1, 7, 8)
		tbl.attach(self.new_label('Rame'), 0, 1, 8, 9)
		tbl.attach(self.new_label('Fosfati'), 0, 1, 9, 10)
		
		self.ph = self.new_label('0', False); self.kh = self.new_label('0', False)
		self.gh = self.new_label('0', False); self.no2 = self.new_label('0', False)
		self.no3 = self.new_label('0', False); self.cond = self.new_label('0', False)
		self.rame = self.new_label('0', False); self.fosfati = self.new_label('0', False)
		self.ammoniaca = self.new_label('0', False); self.ferro = self.new_label('0', False)

		tbl.attach(self.ph, 1, 2, 0, 1)
		tbl.attach(self.kh, 1, 2, 1, 2)
		tbl.attach(self.gh, 1, 2, 2, 3)
		tbl.attach(self.no2, 1, 2, 3, 4)
		tbl.attach(self.no3, 1, 2, 4, 5)
		tbl.attach(self.cond, 1, 2, 5, 6)
		tbl.attach(self.ammoniaca, 1, 2, 6, 7)
		tbl.attach(self.ferro, 1, 2, 7, 8)
		tbl.attach(self.rame, 1, 2, 8, 9)
		tbl.attach(self.fosfati, 1, 2, 9, 10)

		return tbl
		
	def new_label(self, txt, bold=True):
		lbl = gtk.Label()
		if bold:
			lbl.set_use_markup(True)
			lbl.set_label('<b>' + txt + '</b>')
			lbl.set_alignment(0, 0.5)
		else:
			lbl.set_label(txt)
			lbl.set_alignment(0.5, 0)
		
		return lbl
		
	def exit(self, *w):
		self.hide()
