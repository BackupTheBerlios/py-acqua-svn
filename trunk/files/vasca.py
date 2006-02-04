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
		self.set_title("Vasche")
		
		box = gtk.VBox()
		
		self.vasca_store = gtk.ListStore(int, str, str, str, str, str, str, str, str)
		
		self.view = view = gtk.TreeView(self.vasca_store)
		
		lst = ['Id', 'Vasca', 'Data', 'Nome', 'Tipo Acquario', 'Tipo Filtro', 'Impianto Co2', 'Illuminazione']
		renderer = gtk.CellRendererText()
		
		for i in lst:
			id = lst.index(i)
			col = gtk.TreeViewColumn(i, renderer, text=id)
			col.set_sort_column_id(id+1)
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
		cursore.execute("select * from vasca")

		for y in cursore.fetchall():
			self.vasca_store.append([y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[8]])
		
		
		# Usiamo un expander per rendere tutto piu' appetibile
		self.exp = exp = gtk.Expander("<b>Editing</b>")
		# Facciamo in modo che riconosca i tag di formattazione (<b>)
		exp.set_use_markup(True)
		
		# Creiamo una buttonbox per contenere i bottoni di modifica
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		
		btn = gtk.Button(stock=gtk.STOCK_ADD)
		btn.connect('clicked', self.on_add)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_REFRESH)
		btn.connect('clicked', self.on_refresh)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_SAVE)
		btn.connect('clicked', self.on_save)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_REMOVE)
		btn.connect('clicked', self.on_del)
		bb.pack_start(btn)
		
		# Attacchiamo alla box expander e buttonbox
		# in modo da non farli allargare durante il
		# ridimensionamento :)
		box.pack_start(bb, False, False, 0)
		box.pack_start(exp, False, False, 0)
		
		# Creiamo la table che verra contenuta nell'expander
		tbl = gtk.Table(7, 2)
		
		tbl.attach(gtk.Label("Vasca:"), 0, 1, 0, 1)
		tbl.attach(gtk.Label("Data:"), 0, 1, 1, 2)
		tbl.attach(gtk.Label("Nome:"), 0, 1, 2, 3)
		tbl.attach(gtk.Label("Tipo Acquario:"), 0, 1, 3, 4)
		tbl.attach(gtk.Label("Tipo Filtro:"), 0, 1, 4, 5)
		tbl.attach(gtk.Label("Impianto Co2:"), 0, 1, 5, 6)
		tbl.attach(gtk.Label("Illuminazione:"), 0, 1, 6, 7)
		
		self.e_vasca, self.e_data, self.e_nome = gtk.Entry(), gtk.Entry(), gtk.Entry()
		self.e_tipo, self.e_filtro = gtk.Entry(), gtk.Entry()
		self.e_co2, self.e_il = gtk.Entry(), gtk.Entry()
		
		tbl.attach(self.e_vasca, 1, 2, 0, 1)
		tbl.attach(self.e_data, 1, 2, 1, 2)
		tbl.attach(self.e_nome, 1, 2, 2, 3)
		tbl.attach(self.e_tipo, 1, 2, 3, 4)
		tbl.attach(self.e_filtro, 1, 2, 4, 5)
		tbl.attach(self.e_co2, 1, 2, 5, 6)
		tbl.attach(self.e_il, 1, 2, 6, 7)
		
		exp.add(tbl)
		
		self.add(box)
		self.show_all()

	def on_refresh(self, widget): 
		
		# Prendiamo l'iter e il modello dalla selezione
		
		mod, it = self.view.get_selection().get_selected()
		
		# Se esiste una selezione aggiorniamo la row
		# in base al contenuto delle entry
		
		if it != None:
			self.vasca_store.set_value(it, 1, self.e_vasca.get_text())
			self.vasca_store.set_value(it, 2, self.e_data.get_text())
			self.vasca_store.set_value(it, 3, self.e_nome.get_text())
			self.vasca_store.set_value(it, 4, self.e_tipo.get_text())
			self.vasca_store.set_value(it, 5, self.e_filtro.get_text())
			self.vasca_store.set_value(it, 6, self.e_co2.get_text())
			self.vasca_store.set_value(it, 7, self.e_il.get_text())

	def on_add(self, widget):
		# Aggiungiamo dei valori casuali che andranno subito ad essere modificati
		# dall'utente
		
		it = self.vasca_store.append()

		self.vasca_store.set_value(it, 1, "EDIT ME")
		self.vasca_store.set_value(it, 2, "EDIT ME")
		self.vasca_store.set_value(it, 3, "EDIT ME")
		self.vasca_store.set_value(it, 4, "EDIT ME")
		self.vasca_store.set_value(it, 5, "EDIT ME")
		self.vasca_store.set_value(it, 6, "EDIT ME")
		self.vasca_store.set_value(it, 7, "EDIT ME")
	def on_save(self, widget):
		#come fai a prelevare i dati dal row????
		
		connessione=sqlite.connect(os.path.join('Data', 'db'))
		cursore=connessione.cursor()
		cursore.execute("insert into vasca values (?,?,?,?,?,?,?,?,?)",(id, vasca, data, nome, tipo, filtro, co, illuminazione, immagine))
		connessione.commit()



	def on_del(self, widget): 
		# prendiamo l'iter selezionato e elimianiamolo dalla store
		mod, it = self.view.get_selection().get_selected()
		
		if it != None:
			self.vasca_store.remove(it)

	def on_selection_changed(self, sel):
		# Aggiorniamo il contenuto delle entry in base alla selezione
		mod, it = sel.get_selected()
		
		if it != None:
			self.e_vasca.set_text(mod.get_value(it, 1))
			self.e_data.set_text(mod.get_value(it, 2))
			self.e_nome.set_text(mod.get_value(it, 3))
			self.e_tipo.set_text(mod.get_value(it, 4))
			self.e_filtro.set_text(mod.get_value(it, 5))
			self.e_co2.set_text(mod.get_value(it, 6))
			self.e_il.set_text(mod.get_value(it, 7))
			
			self.exp.set_expanded(True)
		else:
			self.e_vasca.set_text('')
			self.e_data.set_text('')
			self.e_nome.set_text('')
			self.e_tipo.set_text('')
			self.e_filtro.set_text('')
			self.e_co2.set_text('')
			self.e_il.set_text('')

			self.exp.set_expanded(False)
