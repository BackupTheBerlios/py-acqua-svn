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
from pysqlite2 import dbapi2 as sqlite

class Vasca(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		
		self.set_title('Vasche')
		
		vbox = gtk.VBox()
		
		nb = gtk.Notebook()
		
		nb.append_page(self.inserisci_vasche(), gtk.Label('Inserisci'))
		nb.append_page(self.visualizza_vasche(), gtk.Label('Visualizza'))
		nb.append_page(self.modifica_vasche(), gtk.Label('Modifica'))
		
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
		
	def refresh(self,widget):
		
		connessione=sqlite.connect(os.path.join('Data', 'db'))
		cursore=connessione.cursor()
		cursore.execute("select * from vasca")

		# Eliminiamo le vecchie righe
		self.vasca_store.clear()
		
		for y in cursore.fetchall():
			self.vasca_store.append([y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[8]])
		
		
	def inserisci_vasche(self):
		entry = gtk.Entry()
		tbl = gtk.Table(10, 2)
		tbl.set_border_width(5)
		
		tbl.attach(self.new_label('Vasca'), 0, 1, 0, 1)
		tbl.attach(self.new_label('Data di avvio'), 0, 1, 1, 2)
		tbl.attach(self.new_label('Nome'), 0, 1, 2, 3)
		tbl.attach(self.new_label('Tipo di acquario'), 0, 1, 3, 4)
		tbl.attach(self.new_label('Tipo di filtro'), 0, 1, 4, 5)
		tbl.attach(self.new_label('Impianto co2'), 0, 1, 5, 6)
		tbl.attach(self.new_label('Illuminazione'), 0, 1, 6, 7)
		tbl.attach(self.new_label('Foto'), 0, 1, 7, 8)
		
		tbl.attach(entry, 1, 2, 0, 1)
		
		return tbl
	def visualizza_vasche(self):
	
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)

		self.vasca_store = gtk.ListStore(int, str, str, str, str, str, str, str, str)
		view = gtk.TreeView(self.vasca_store)
		lst = ['Id', 'Vasca', 'Data', 'Nome', 'Tipo Acquario', 'Tipo Filtro', 'Impianto Co2', 'Illuminazione']
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
		
	def modifica_vasche(self):
		entry = gtk.Entry()
		tbl = gtk.Table(10, 2)
		tbl.set_border_width(5)
		
		tbl.attach(self.new_label('Vasca'), 0, 1, 0, 1)
		tbl.attach(self.new_label('Data di avvio'), 0, 1, 1, 2)
		tbl.attach(self.new_label('Nome'), 0, 1, 2, 3)
		tbl.attach(self.new_label('Tipo di acquario'), 0, 1, 3, 4)
		tbl.attach(self.new_label('Tipo di filtro'), 0, 1, 4, 5)
		tbl.attach(self.new_label('Impianto co2'), 0, 1, 5, 6)
		tbl.attach(self.new_label('Illuminazione'), 0, 1, 6, 7)
		tbl.attach(self.new_label('Foto'), 0, 1, 7, 8)
		
		tbl.attach(entry, 1, 2, 0, 1)
		
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
