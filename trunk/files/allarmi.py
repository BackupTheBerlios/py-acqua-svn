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
import utils
import impostazioni

from inserisci import *
from pysqlite2 import dbapi2 as sqlite

class Allarmi(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		
		self.set_title(_('Allarmi'))
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		
		vbox = gtk.VBox()
		vbox.set_spacing(4)
		vbox.set_border_width(4)
		
		# Pagina Test
		tbl = gtk.Table(10, 2)
		tbl.set_border_width(5)
		
		tbl.attach(utils.new_label(_('Ph')), 0, 1, 0, 1)
		tbl.attach(utils.new_label(_('Kh')), 0, 1, 1, 2)
		tbl.attach(utils.new_label(_('Gh')), 0, 1, 2, 3)
		tbl.attach(utils.new_label(_('No2')), 0, 1, 3, 4)
		tbl.attach(utils.new_label(_('No3')), 0, 1, 4, 5)
		tbl.attach(utils.new_label(_('Conducibilita\'')), 0, 1, 5, 6)
		tbl.attach(utils.new_label(_('Ammoniaca')), 0, 1, 6, 7)
		tbl.attach(utils.new_label(_('Ferro')), 0, 1, 7, 8)
		tbl.attach(utils.new_label(_('Rame')), 0, 1, 8, 9)
		tbl.attach(utils.new_label(_('Fosfati')), 0, 1, 9, 10)
		
		self.ph = utils.new_label('0', False); self.kh = utils.new_label('0', False)
		self.gh = utils.new_label('0', False); self.no2 = utils.new_label('0', False)
		self.no3 = utils.new_label('0', False); self.cond = utils.new_label('0', False)
		self.rame = utils.new_label('0', False); self.fosfati = utils.new_label('0', False)
		self.ammoniaca = utils.new_label('0', False); self.ferro = utils.new_label('0', False)

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
		
		vbox.pack_start(tbl)

		# creiamo la ButtonBox
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		bb.set_spacing(4)

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
		
		# Aggiorniamo le label
		self.refresh(None)
		
	def refresh(self, widget):
		
		impostazioni.refresh()

		con = sqlite.connect(os.path.join('Data', 'db'))
		cur = con.cursor()
		cur.execute('select * from test')
		
		for x in cur.fetchall():
			if x[1] < float(impostazioni.minph): self.ph.set_label(_('Ph basso'))
			if x[1] > float(impostazioni.maxph): self.ph.set_label(_('Ph alto'))
			else: self.ph.set_label(_('Ph ok'))

			if x[1] < float(impostazioni.minkh): self.kh.set_label(_('Kh basso'))
			if x[1] > float(impostazioni.maxkh): self.kh.set_label(_('Kh alto'))
			else: self.kh.set_label(_('Kh ok'))

			if x[1] < float(impostazioni.mingh): self.gh.set_label(_('Gh basso'))
			if x[1] > float(impostazioni.maxgh): self.gh.set_label(_('Gh alto'))
			else: self.gh.set_label(_('Gh ok'))

			if x[1] < float(impostazioni.minno2): self.no2.set_label(_('No2 bassi'))
			if x[1] > float(impostazioni.maxno2): self.no2.set_label(_('No2 alti'))
			else: self.no2.set_label(_('No2 ok'))

			if x[1] < float(impostazioni.minno3): self.no3.set_label(_('No3 bassi'))
			if x[1] > float(impostazioni.maxno3): self.no3.set_label(_('No3 alti'))
			else: self.no3.set_label(_('No3 ok'))

			if x[1] < float(impostazioni.mincon): self.cond.set_label(_('Conducibilita\' bassa'))
			if x[1] > float(impostazioni.maxcon): self.cond.set_label(_('Conducibilita\' alta'))
			else: self.cond.set_label(_('Conducibilita\' ok'))

			if x[1] < float(impostazioni.minam): self.ammoniaca.set_label(_('Ammoniaca bassa'))
			if x[1] > float(impostazioni.maxam): self.ammoniaca.set_label(_('Ammoniaca alta'))
			else: self.ammoniaca.set_label(_('Ammoniaca ok'))

			if x[1] < float(impostazioni.minfe): self.ferro.set_label(_('Ferro basso'))
			if x[1] > float(impostazioni.maxfe): self.ferro.set_label(_('Ferro alto'))
			else: self.ferro.set_label(_('Ferro ok'))

			if x[1] < float(impostazioni.minra): self.rame.set_label(_('Rame basso'))
			if x[1] > float(impostazioni.maxra): self.rame.set_label(_('Rame alto'))
			else: self.rame.set_label(_('Rame ok'))

			if x[1] < float(impostazioni.minfo): self.fosfati.set_label(_('Fosfati bassi'))
			if x[1] > float(impostazioni.maxfo): self.fosfati.set_label(_('Fosfati alti'))
			else: self.fosfati.set_label(_('Fosfati ok'))
		
	def make_test_page(self):
		
		# Pagina Test
		tbl = gtk.Table(10, 2)
		tbl.set_border_width(5)
		
		tbl.attach(utils.new_label(_('Ph')), 0, 1, 0, 1)
		tbl.attach(utils.new_label(_('Kh')), 0, 1, 1, 2)
		tbl.attach(utils.new_label(_('Gh')), 0, 1, 2, 3)
		tbl.attach(utils.new_label(_('No2')), 0, 1, 3, 4)
		tbl.attach(utils.new_label(_('No3')), 0, 1, 4, 5)
		tbl.attach(utils.new_label(_('Conducibilita\'')), 0, 1, 5, 6)
		tbl.attach(utils.new_label(_('Ammoniaca')), 0, 1, 6, 7)
		tbl.attach(utils.new_label(_('Ferro')), 0, 1, 7, 8)
		tbl.attach(utils.new_label(_('Rame')), 0, 1, 8, 9)
		tbl.attach(utils.new_label(_('Fosfati')), 0, 1, 9, 10)
		
		self.ph = utils.new_label('0', False); self.kh = utils.new_label('0', False)
		self.gh = utils.new_label('0', False); self.no2 = utils.new_label('0', False)
		self.no3 = utils.new_label('0', False); self.cond = utils.new_label('0', False)
		self.rame = utils.new_label('0', False); self.fosfati = utils.new_label('0', False)
		self.ammoniaca = utils.new_label('0', False); self.ferro = utils.new_label('0', False)

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
		
	def exit(self, *w):
		self.hide()
