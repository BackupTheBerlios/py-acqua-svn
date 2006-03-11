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

class Test(gtk.Window):
	PyChart = True
	def __init__(self): 
		gtk.Window.__init__(self)
		
		self.set_title(_("Test"))
		self.set_size_request(600, 400)
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		box = gtk.VBox()
		# id integer, date DATE, vasca FLOAT, ph FLOAT, kh FLOAT, gh
		# NUMERIC, no NUMERIC, noo NUMERIC, con NUMERIC, amm NUMERIC, fe
		# NUMERIC, ra NUMERIC, fo NUMERIC
		self.test_store = gtk.ListStore(
			int,	# ID
			str,	# DATA
			str,	# VASCA
			float,	# PH
			float,	# KH
			float,	# GH
			float,	# NO
			float,	# NO2
			float,	# COND
			float,	# AMMO
			float,	# FERRO
			float,	# RAME
			float,	# FOSFATI
			float,	#calcio
			float,	#magnesio
			float)	#densita
		
		
		self.view = view = gtk.TreeView(self.test_store)
		
		lst = [_('Id'), _('Data'), _('Vasca')]
		renderer = gtk.CellRendererText()
		
		for i in lst:
			id = lst.index(i)
			col = gtk.TreeViewColumn(i, renderer, text=id)
			col.set_sort_column_id(id)
			col.set_clickable(True)
			col.set_resizable(True)
			view.append_column(col)
		
		lst = [_('Ph'), _('Kh'), _('Gh'), _('No'), _('No2'),
			_('Conducibilita\''), _('Ammoniaca'), _('Ferro'), _('Rame'), _('Fosfati'), _('Calcio'), _('Magnesio'), _('Densità')]
			
		for i in lst:
			id = lst.index(i)
			view.insert_column_with_data_func(-1, i, renderer, self.row_func, id+3)
		
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
			y[5], y[6], y[7], y[8], y[9], y[10], y[11], y[12], y[13], y[14], y[15]])
		
		
		frm = gtk.Frame(_("Editing:"))
		
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

		btn = gtk.Button(_('Grafico'))
		btn.connect('clicked', self.on_draw_graph)
		bb.pack_start(btn)
		
		box.pack_start(bb, False, False, 0)
		box.pack_start(frm, False, False, 0)
		
		# Creiamo la table che verra contenuta nel frame
		tbl = gtk.Table(6, 4)
		tbl.set_col_spacings(4)
		
		tbl.attach(self.new_label(_("Data:")), 0, 1, 0, 1)
		tbl.attach(self.new_label(_("Vasca:")), 0, 1, 1, 2)
		tbl.attach(self.new_label(_("Ph:")), 0, 1, 2, 3)
		tbl.attach(self.new_label(_("Kh:")), 0, 1, 3, 4)
		tbl.attach(self.new_label(_("Gh:")), 0, 1, 4, 5)
		tbl.attach(self.new_label(_("No:")), 0, 1, 5, 6)
		tbl.attach(self.new_label(_("Calcio")), 0, 1, 6, 7)
		
		tbl.attach(self.new_label(_("No2:")), 2, 3, 0, 1)
		tbl.attach(self.new_label(_("Conducibilita':")), 2, 3, 1, 2)
		tbl.attach(self.new_label(_("Ammoniaca:")), 2, 3, 2, 3)
		tbl.attach(self.new_label(_("Ferro")), 2, 3, 3, 4)
		tbl.attach(self.new_label(_("Rame")), 2, 3, 4, 5)
		tbl.attach(self.new_label(_("Fosfati")), 2, 3, 5, 6)
		tbl.attach(self.new_label(_("Magnesio")), 2, 3, 6, 7)
		tbl.attach(self.new_label(_("Densità")), 2, 3, 7, 8)

		def make_inst(num):
			a = list()
			for i in range(num):
				a.append(utils.FloatEntry())
			return a

		self.e_data = utils.DataButton()
		self.e_vasca = utils.Combo()
		
		connessione=sqlite.connect(os.path.join('Data', 'db'))
		cursore=connessione.cursor()
		cursore.execute("select * from vasca")
		
		for v in cursore.fetchall():
			self.e_vasca.append_text(v[3])

		self.e_ph, self.e_kh = make_inst(2)
		self.e_gh, self.e_no, self.e_no2, self.e_cond = make_inst(4)
		self.e_ammo, self.e_ferro, self.e_rame, self.e_fosfati = make_inst(4)
		self.e_calcio, self.e_magnesio, self.e_densita = make_inst(3)
		
		attach = lambda x, y, z: tbl.attach(x, 1, 2, y, z)

		attach(self.e_data, 0, 1)
		attach(self.e_vasca, 1, 2)
		attach(self.e_ph, 2, 3)
		attach(self.e_kh, 3, 4)
		attach(self.e_gh, 4, 5)
		attach(self.e_no, 5, 6)
		attach(self.e_calcio, 6, 7)
		
		attach = lambda x, y, z: tbl.attach(x, 3, 4, y, z)
		
		attach(self.e_no2, 0, 1)
		attach(self.e_cond, 1, 2)
		attach(self.e_ammo, 2, 3)
		attach(self.e_ferro, 3, 4)
		attach(self.e_rame, 4, 5)
		attach(self.e_fosfati, 5, 6)
		attach(self.e_magnesio, 6, 7)
		attach(self.e_densita, 7, 8)

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
		
	def row_func(self, col, cell, model, iter, id):
		value = model.get_value(iter, id)
		cell.set_property("text", "%.2f" % value)

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
			calcio = self.e_calcio.get_text()
			magnesio = self.e_magnesio.get_text()
			densita = self.e_densita.get_text()
			
			
			
			conn = sqlite.connect(os.path.join('Data', 'db'))
			cur = conn.cursor()

			cur.execute("update test set date='%(data)s', vasca='%(vasca)s', ph='%(ph)s', kh='%(kh)s', gh='%(gh)s', no='%(no)s', noo='%(no2)s', con='%(cond)s', amm='%(ammo)s', fe='%(ferro)s', ra='%(rame)s', fo='%(fosfati)s', calcio='%(calcio)s', magnesio='%(magnesio)s', densita='%(densita)' where id=%(id)s" %vars())
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
			self.test_store.set_value(it, 13, calcio)
			self.test_store.set_value(it, 14, magnesio)
			self.test_store.set_value(it, 15, densita)
			
			
			
			self.update_status(0, _("Row aggiornata (ID: %d)") % id)

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
		calcio = self.e_calcio.get_text()
		magnesio = self.e_magnesio.get_text()
		densita = self.e_densita.get_text()
		
		
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
		self.test_store.set_value(it, 13, calcio)
		self.test_store.set_value(it, 14, magnesio)
		self.test_store.set_value(it, 15, densita)
		
		conn = sqlite.connect(os.path.join('Data', 'db'))
		cur = conn.cursor()

		cur.execute('insert into test values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
			(id, data, vasca, ph, kh, gh, no, no2, cond, ammo, ferro, rame, fosfati, calcio, magnesio, densita))
		conn.commit()

		self.update_status(1, _("Row aggiunta (ID: %d)") % id)
		
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

			self.update_status(2, _("Row eliminata (ID: %d)") % value)

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
			self.e_calcio.set_text(mod.get_value(it, 13))
			self.e_magnesio.set_text(mod.get_value(it, 14))
			self.e_densita.set_text(mod.get_value(it, 15))
	
	def on_draw_graph(self, widget):
		if not Test.PyChart:
			dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL,
				gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
				_("PyChart non installato.\nScaricalo da http://home.gna.org/pychart/"))
			
			dialog.run()
			dialog.hide()
			dialog.destroy()
			
		else:
			date = self.e_data.get_text()
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
			calcio = self.e_calcio.get_text()
			magnesio = self.e_magnesio.get_text()
			densita = self.e_densita.get_text()
			
			
			can = canvas.init(os.path.join('Immagini', 'grafico.png'))
			
			theme.use_color = 2
			theme.reinitialize()
			
			data = [
				[_('Ph'), ph], [_('Kh'), kh],
				[_('Gh'), gh], [_('No'), no],
				[_('No2'), no2], [_('Cond.'), cond],
				[_('Ammon.'), ammo], [_('Ferro'), ferro],
				[_('Rame'), rame], [_('Fosf.'), fosfati],
				[_('Calcio'), calcio], [_('Magnes.'), magnesio],
				[_('Densità'), densita]
				]
			ar = area.T(x_coord = category_coord.T(data, 0),
				y_range = (0, None),
				size = (400, 250),

				x_axis = axis.X(label=_('Test')),
				y_axis = axis.Y(label=_('Valori')))
			ar.add_plot(bar_plot.T(data = data, label = _("Legenda")))
			ar.draw(can)
			can.close()

			# InfoDialog
			d = gtk.MessageDialog(self, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK)
			d.set_markup(_("<span size=\"large\"><b>PyAcqua Graph</b></span>\n\n<b>Tipo Vasca:</b> %s\n<b>Data:</b> %s") % (vasca, date))
			
			img = gtk.Image(); img.set_from_file(os.path.join('Immagini', 'grafico.png'))
			
			sw = gtk.ScrolledWindow()
			sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			#sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
			
			sw.add_with_viewport(img)
			
			d.vbox.pack_start(sw)
			d.vbox.show_all()
			d.set_border_width(4)
			
			d.set_size_request(600, 450)
			
			d.run()
			d.hide(); d.destroy()
			
			if os.path.isfile(os.path.join('Immagini', 'grafico.png')):
				os.remove(os.path.join('Immagini', 'grafico.png'))

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
try:
	from pychart import *
except:
	Test.PyChart = False
