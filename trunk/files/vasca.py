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

class Vasca(gtk.Window):
	def __init__(self): 
		gtk.Window.__init__(self)
		
		self.set_title(_("Vasche"))
		self.set_size_request(600, 400)
		
		box = gtk.VBox()
		
		self.vasca_store = gtk.ListStore(int, str, str, str, str, str, str, str, str, gtk.gdk.Pixbuf, str)
		
		self.view = view = gtk.TreeView(self.vasca_store)
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		
		lst = [_('Id'), _('Vasca'), _('Data'), _('Nome'), _('Litri'),
			_('Tipo Acquario'), _('Tipo Filtro'),
			_('Impianto Co2'), _('Illuminazione')]
			
		renderer = gtk.CellRendererText()
		
		for i in lst:
			id = lst.index(i)
			col = gtk.TreeViewColumn(i, renderer, text=id)
			col.set_sort_column_id(id)
			col.set_clickable(True)
			col.set_resizable(True)
			view.append_column(col)
		
		# Aggiungiamo la colonna per le immagini della vasca
		col = gtk.TreeViewColumn(_("Immagine"), gtk.CellRendererPixbuf(), pixbuf=8)
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
		
		connessione=sqlite.connect(os.path.join('Data', 'db'))
		cursore=connessione.cursor()
		cursore.execute("select * from vasca")

		# Costruisci l'immagine..
		for y in cursore.fetchall():
			self.vasca_store.append([y[0], y[1], y[2], y[3], y[4],
			y[5], y[6], y[7], y[8], self.make_image(y[9]), y[9]])
		
		
		frm = gtk.Frame(_("Vasca:")); frm1 = gtk.Frame(_("Editing:"))
		
		# Pacchiamoli...
		box.pack_start(frm, False, False, 0)
		box.pack_start(frm1, False, False, 0)

		
		
		
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
		tbl_1 = gtk.Table(8, 2)
		
		tbl_1.attach(self.new_label(_("Vasca:")), 0, 1, 0, 1)
		
		#combo per i tipi di vasche
		self.e_vasca = utils.Combo()
		
		self.e_vasca.append_text(_("Dolce"))
		self.e_vasca.append_text(_("Dolce Tropicale"))
		self.e_vasca.append_text(_("Marino"))
		self.e_vasca.append_text(_("Marino Mediterraneo"))
		self.e_vasca.append_text(_("Paludario"))
		self.e_vasca.append_text(_("Salmastro"))
		self.e_vasca.set_active(0)
		
		
		tbl_1.attach(self.e_vasca, 1, 2, 0, 1)
		
		# Quando si sceglie il tipo di vasca invochiamo aggiorna()
		self.e_vasca.connect('changed', self.aggiorna)
		
		
		# Creiamo un notebook di due schede contenenti le diverse
		# tabelle (per dolce e marino)
		self.notebook = gtk.Notebook()
		self.notebook.set_show_tabs(False)
		self.notebook.set_show_border(False)
		
		#creiamo la tabella per il dolce
		tbl = gtk.Table(8, 2)
		tbl.set_border_width(4)
		tbl.set_row_spacings(4)
		
		tbl.attach(self.new_label(_("Data:")), 0, 1, 1, 2)
		tbl.attach(self.new_label(_("Nome:")), 0, 1, 2, 3)
		tbl.attach(self.new_label(_("Litri:")), 0, 1, 3, 4)
		tbl.attach(self.new_label(_("Tipo Acquario:")), 0, 1, 4, 5)
		tbl.attach(self.new_label(_("Tipo Filtro:")), 0, 1, 5, 6)
		tbl.attach(self.new_label(_("Impianto Co2:")), 0, 1, 6, 7)
		tbl.attach(self.new_label(_("Illuminazione:")), 0, 1, 7, 8)
		tbl.attach(self.new_label(_("Immagine:")), 0, 1, 8, 9)
		
		#combo per i tipi di vasche
		#self.e_vasca = utils.Combo()

		#self.e_vasca.append_text(_("Dolce"))
		#self.e_vasca.append_text(_("Dolce Tropicale"))
		#self.e_vasca.append_text(_("Marino"))
		#self.e_vasca.append_text(_("Marino Mediterraneo"))
		#self.e_vasca.append_text(_("Paludario"))
		#self.e_vasca.append_text(_("Salmastro"))
		
		
		
		self.e_data, self.e_nome = utils.DataButton(), gtk.Entry()
		self.e_litri, self.e_tipo, self.e_filtro = gtk.Entry(), gtk.Entry(), gtk.Entry()
		self.e_co2, self.e_il = gtk.Entry(), gtk.Entry()
		self.e_path = gtk.Entry()

		self.e_path.set_property('editable', False)
		
		#tbl.attach(self.e_vasca, 1, 2, 0, 1)
		tbl.attach(self.e_data, 1, 2, 1, 2)
		tbl.attach(self.e_nome, 1, 2, 2, 3)
		tbl.attach(self.e_litri, 1, 2, 3, 4)
		tbl.attach(self.e_tipo, 1, 2, 4, 5)
		tbl.attach(self.e_filtro, 1, 2, 5, 6)
		tbl.attach(self.e_co2, 1, 2, 6, 7)
		tbl.attach(self.e_il, 1, 2, 7, 8)
		
		
		
		#per l immagine
		hbox = gtk.HBox()

		btn = gtk.Button(stock=gtk.STOCK_OPEN)
		btn.set_relief(gtk.RELIEF_NONE)
		btn.connect('clicked', self.on_browse)
		
		hbox.pack_start(self.e_path)
		hbox.pack_start(btn, False, False, 0)
		
		tbl.attach(hbox, 1, 2, 8, 9)

		tbl.set_border_width(10)
		
		# Aggiungiamo la table per il tipo dolce alla notebook
		self.notebook.append_page(tbl, None)
		
		
		# Creiamo la table per il tipo marino
		tbl = gtk.Table(8, 2)
		tbl.set_border_width(4)
		tbl.set_row_spacings(4)
		
		
		tbl.attach(self.new_label(_("Data:")), 0, 1, 1, 2)
		tbl.attach(self.new_label(_("Nome:")), 0, 1, 2, 3)
		tbl.attach(self.new_label(_("Litri:")), 0, 1, 3, 4)
		tbl.attach(self.new_label(_("Tipo Acquario:")), 0, 1, 4, 5)
		tbl.attach(self.new_label(_("Tipo Filtro:")), 0, 1, 5, 6)
		tbl.attach(self.new_label(_("Impianto Co2:")), 0, 1, 6, 7)
		tbl.attach(self.new_label(_("Illuminazione:")), 0, 1, 7, 8)
		tbl.attach(self.new_label(_("Immagine:")), 0, 1, 8, 9)
		
		self.e_data, self.e_nome = utils.DataButton(), gtk.Entry()
		self.e_litri, self.e_tipo, self.e_filtro = gtk.Entry(), gtk.Entry(), gtk.Entry()
		self.e_co2, self.e_il = gtk.Entry(), gtk.Entry()
		self.e_path = gtk.Entry()

		self.e_path.set_property('editable', False)
		
		tbl.attach(self.e_data, 1, 2, 1, 2)
		tbl.attach(self.e_nome, 1, 2, 2, 3)
		tbl.attach(self.e_litri, 1, 2, 3, 4)
		tbl.attach(self.e_tipo, 1, 2, 4, 5)
		tbl.attach(self.e_filtro, 1, 2, 5, 6)
		tbl.attach(self.e_co2, 1, 2, 6, 7)
		tbl.attach(self.e_il, 1, 2, 7, 8)
		
		# Aggiungiamo la table per il tipo marino alla notebook
		self.notebook.append_page(tbl, None)
		
		
		
		
		
		

		hbox = gtk.HBox()

		btn = gtk.Button(stock=gtk.STOCK_OPEN)
		btn.set_relief(gtk.RELIEF_NONE)
		btn.connect('clicked', self.on_browse)
		
		hbox.pack_start(self.e_path)
		hbox.pack_start(btn, False, False, 0)
		
		tbl.attach(hbox, 1, 2, 8, 9)

		tbl.set_border_width(10)
		
		
		
		frm.add(tbl_1)
		
		#aggiungiamo la notebook
		frm1.add(self.notebook)
		
		
		
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
		
		
	def aggiorna(self, widget):
		self.notebook.set_current_page(self.e_vasca.get_active())

	def on_refresh(self, widget):
		
		# Prendiamo l'iter e il modello dalla selezione
		
		mod, it = self.view.get_selection().get_selected()
		
		# Se esiste una selezione aggiorniamo la row
		# in base al contenuto delle entry
		
		if it != None:
			id = int(self.vasca_store.get_value(it, 0))
			
			text = self.e_vasca.get_text()
			date = self.e_data.get_text()
			name = self.e_nome.get_text()
			litri = self.e_litri.get_text()
			tacq = self.e_tipo.get_text()
			tflt = self.e_filtro.get_text()
			ico2 = self.e_co2.get_text()
			illu = self.e_il.get_text()
			img = self.e_path.get_text()
			
			conn = sqlite.connect(os.path.join('Data', 'db'))
			cur = conn.cursor()

			cur.execute("update vasca set vasca='%(text)s', date='%(date)s', nome='%(name)s', litri='%(litri)s', tipo='%(tacq)s', filtro='%(tflt)s', co='%(ico2)s', illuminazione='%(illu)s', img='%(img)s' where id = %(id)s" %vars())
			conn.commit()
			
			self.vasca_store.set_value(it, 1, text)
			self.vasca_store.set_value(it, 2, date)
			self.vasca_store.set_value(it, 3, name)
			self.vasca_store.set_value(it, 4, litri)
			self.vasca_store.set_value(it, 5, tacq)
			self.vasca_store.set_value(it, 6, tflt)
			self.vasca_store.set_value(it, 7, ico2)
			self.vasca_store.set_value(it, 8, illu)
			self.vasca_store.set_value(it, 9, self.make_image(img))
			self.vasca_store.set_value(it, 10, img)

			self.update_status(0, _("Row aggiornata (ID: %d)") % id)

	def on_add(self, widget):
		# Aggiungiamo dei valori casuali che andranno subito ad essere modificati
		# dall'utente
		mod = self.view.get_model()
		it = mod.get_iter_first()
		id = 0
		
		while it != None:
			tmp = int(self.vasca_store.get_value(it, 0))
			
			if tmp > id: id = tmp

			it = mod.iter_next(it)
		
		id += 1		
		it = self.vasca_store.append()

		# Settiamo il campo ID
		self.vasca_store.set_value(it, 0, id)

		text = self.e_vasca.get_text()
		date = self.e_data.get_text()
		name = self.e_nome.get_text()
		litri = self.e_litri.get_text()
		tacq = self.e_tipo.get_text()
		tflt = self.e_filtro.get_text()
		ico2 = self.e_co2.get_text()
		illu = self.e_il.get_text()
		img = self.e_path.get_text()
		
		self.vasca_store.set_value(it, 1, text)
		self.vasca_store.set_value(it, 2, date)
		self.vasca_store.set_value(it, 3, name)
		self.vasca_store.set_value(it, 4, litri)
		self.vasca_store.set_value(it, 5, tacq)
		self.vasca_store.set_value(it, 6, tflt)
		self.vasca_store.set_value(it, 7, ico2)
		self.vasca_store.set_value(it, 8, illu)
		self.vasca_store.set_value(it, 9, self.make_image(img))
		self.vasca_store.set_value(it, 10, img)
		
		conn = sqlite.connect(os.path.join('Data', 'db'))
		cur = conn.cursor()

		cur.execute('insert into vasca values(?,?,?,?,?,?,?,?,?,?)',
			(id, text, date, name, litri, tacq, tflt, ico2, illu, img))
		conn.commit()

		self.update_status(1, _("Row aggiunta (ID: %d)") % id)
		
	def on_del(self, widget): 
		# prendiamo l'iter selezionato e elimianiamolo dalla store
		mod, it = self.view.get_selection().get_selected()

		if it != None:
			# Questo e' il valore da confrontare
			value = int(self.vasca_store.get_value(it, 0))

			# Rimuoviamo dal database
			conn = sqlite.connect(os.path.join('Data', 'db'))
			cur = conn.cursor()

			cur.execute('delete from vasca where id=%d' % value)
			conn.commit()

			# Rimuoviamo la riga selezionata
			self.vasca_store.remove(it)

			# Iteriamo tutte le righe per trovarne una con campo id
			# maggiore di value e modifichiamolo
			it = mod.get_iter_first()

			while it != None:
				tmp = int(self.vasca_store.get_value(it, 0))

				if value < tmp:
					self.vasca_store.set_value(it, 0, tmp-1)
					cur.execute("update vasca set id=%d where id=%d" % (tmp-1, tmp))
					conn.commit()
				it = mod.iter_next(it)

			self.update_status(2, _("Row eliminata (ID: %d)") % value)

	def on_selection_changed(self, sel):
		# Aggiorniamo il contenuto delle entry in base alla selezione
		mod, it = sel.get_selected()
		
		if it != None:
			self.e_vasca.set_text(mod.get_value(it, 1))
			self.e_data.set_text(mod.get_value(it, 2))
			self.e_nome.set_text(mod.get_value(it, 3))
			self.e_litri.set_text(mod.get_value(it, 4))
			self.e_tipo.set_text(mod.get_value(it, 5))
			self.e_filtro.set_text(mod.get_value(it, 6))
			self.e_co2.set_text(mod.get_value(it, 7))
			self.e_il.set_text(mod.get_value(it, 8))
			self.e_path.set_text(mod.get_value(it, 10))
			
	def on_row_activated(self, tree, path, col):
		mod = self.view.get_model()
		it = mod.get_iter_from_string(str(path[0]))

		InfoDialog(self, mod, it)
	
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
	
	def on_delete_event(self, widget, event):
		if self.timeoutid != None:
			gobject.source_remove(self.timeoutid)
	
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

class InfoDialog(gtk.Dialog):
	def __init__(self, parent, mod, it):
		gtk.Dialog.__init__(self, _("Riepilogo"), parent,
			gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_OK))

		self.set_size_request(400, 300)
		self.vbox.set_border_width(10)

		self.set_has_separator(False)
		
		tbl = gtk.Table(7, 2)
		tbl.set_border_width(4)
		
		img = gtk.Image();
		
		try:
			img.set_from_file(os.path.join('Immagini',
				str(mod.get_value(it, 10))))
		except:
			img.set_from_stock(gtk.STOCK_IMAGE_MISSING,
				gtk.ICON_SIZE_DIALOG)
		
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

		sw.add_with_viewport(img)

		self.vbox.pack_start(sw)
		
		tbl.attach(self.new_label(_("Vasca:")), 0, 1, 0, 1)
		tbl.attach(self.new_label(_("Data:")), 0, 1, 1, 2)
		tbl.attach(self.new_label(_("Nome:")), 0, 1, 2, 3)
		tbl.attach(self.new_label(_("Litri:")), 0, 1, 3, 4)
		tbl.attach(self.new_label(_("Tipo Acquario:")), 0, 1, 4, 5)
		tbl.attach(self.new_label(_("Tipo Filtro:")), 0, 1, 5, 6)
		tbl.attach(self.new_label(_("Impianto Co2:")), 0, 1, 6, 7)
		tbl.attach(self.new_label(_("Illuminazione:")), 0, 1, 7, 8)

		attach = lambda t, x, y: tbl.attach(gtk.Label(str(t)), 1, 2, x, y)
		
		attach(mod.get_value(it, 1), 0, 1)
		attach(mod.get_value(it, 2), 1, 2)
		attach(mod.get_value(it, 3), 2, 3)
		attach(mod.get_value(it, 4), 3, 4)
		attach(mod.get_value(it, 5), 4, 5)
		attach(mod.get_value(it, 6), 5, 6)
		attach(mod.get_value(it, 7), 6, 7)
		attach(mod.get_value(it, 8), 7, 8)
		
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
