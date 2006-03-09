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
import utils

class Calcoli(gtk.Window):
	def __init__(self): 
		gtk.Window.__init__(self)
		
		self.set_title(_("Calcoli"))
		self.set_resizable(False)
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		vbox = gtk.VBox()
		vbox.set_spacing(4)
		vbox.set_border_width(4)
		
		f1 = gtk.Frame(_('Valori')); f2 = gtk.Frame(_('Risultati'))
		
		vbox.pack_start(f1, False, False, 0)
		vbox.pack_start(f2, False, False, 0)
		
		tbl_valori = gtk.Table(3, 2)
		tbl_valori.set_border_width(4)
		tbl_valori.set_row_spacings(4)
		
		
		tbl_valori.attach(self.new_label(_("Vasca:")), 0, 1, 0, 1)
		tbl_valori.attach(self.new_label(_("Altezza in cm:")), 0, 1, 1, 2)
		tbl_valori.attach(self.new_label(_("Lunghezza in cm:")), 0, 1, 2, 3)
		tbl_valori.attach(self.new_label(_("Larghezza in cm:")), 0, 1, 3, 4)
		
		self.e_vasca = utils.Combo()

		self.e_vasca.append_text(_("Dolce"))
		self.e_vasca.append_text(_("Marino"))
		
		
		self.e_altezza, self.e_lunghezza, self.e_larghezza = gtk.Entry(), gtk.Entry(), gtk.Entry()
		
		tbl_valori.attach(self.e_vasca, 1, 2, 0, 1, yoptions=0)
		tbl_valori.attach(self.e_altezza, 1, 2, 1, 2, yoptions=0)
		tbl_valori.attach(self.e_lunghezza, 1, 2, 2, 3, yoptions=0)
		tbl_valori.attach(self.e_larghezza, 1, 2, 3, 4, yoptions=0)
		
		tbl = gtk.Table(6, 2)
		tbl.set_border_width(4)
		tbl.set_row_spacings(4)
		
		idea = self.e_vasca.get_active_text()
		#print idea
		#if idea == 'Dolce':
		
		#	tbl.attach(self.new_label(_("Volume:")), 0, 1, 2, 3)
		#	tbl.attach(self.new_label(_("Piante Inseribili:")), 0, 1, 3, 4)
		#	tbl.attach(self.new_label(_("Numero di pesci 3-4 cm:")), 0 ,1, 4, 5)
		#else:
		#	tbl.attach(self.new_label(_("Volume:")), 0, 1, 2, 3)
			
		self.volume = self.new_label('0', False)
		self.piante_inseribili = self.new_label('0', False)
		self.num_pesci_3_4 = self.new_label('0', False)
		
		tbl.attach(self.volume, 1, 2, 2, 3)
		tbl.attach(self.piante_inseribili, 1, 2, 3, 4)
		tbl.attach(self.num_pesci_3_4, 1, 2, 4, 5)
		
		tbl.attach(self.new_label(_("Numero di pesci 5-6 cm:")), 0, 1, 5, 6)
		tbl.attach(self.new_label(_("Watt per piante esigenti:")), 0, 1, 6, 7)
		tbl.attach(self.new_label(_("Watt per piante poco esigenti:")), 0, 1, 8, 9)
		
		self.num_pesci_5_6 = self.new_label('0', False)
		self.watt_esigenti = self.new_label('0', False)
		self.watt_poco_esigenti = self.new_label('0', False)
		
		tbl.attach(self.num_pesci_5_6, 1, 2, 5, 6)
		tbl.attach(self.watt_esigenti, 1, 2, 6, 7)
		tbl.attach(self.watt_poco_esigenti, 1, 2, 8, 9)

		f1.add(tbl_valori); f2.add(tbl)
		
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		
		btn = gtk.Button(stock=gtk.STOCK_REFRESH)
		btn.connect('clicked', self.on_refresh)
		bb.pack_start(btn)
		
		btn = gtk.Button(stock=gtk.STOCK_ADD)
		btn.connect('clicked', self.on_aggiorna)
		bb.pack_start(btn)
		
		vbox.pack_start(bb, False, False, 0)
		
		self.add(vbox)
		
		self.show_all()
		
	def on_refresh(self, widget):
		try:
			a = int(self.e_larghezza.get_text())
			b = int(self.e_lunghezza.get_text())
			c = int(self.e_altezza.get_text())
			
		except ValueError:
			a = 0
			b = 0
			c = 0
			#Finestra dialog con errore
		
		e = a*b*c/1000
		f = b*a/50
		g = e/(1.5*4)
		h = e / (3*6)
		i = e*0.5
		l = e*0.35

		self.volume.set_text(str(e))
		self.piante_inseribili.set_text(str(f))
		self.num_pesci_3_4.set_text(str(g))
		self.num_pesci_5_6.set_text(str(h))
		self.watt_esigenti.set_text(str(i))
		self.watt_poco_esigenti.set_text(str(l))
	
	def pulisci_calcoli(self, obj):
		self.entry1.set_text("")
		self.entry2.set_text("")
		self.entry3.set_text("")
		
		
	def on_aggiorna(self, widget):
		tbl = gtk.Table(6, 2)
		tbl.set_border_width(4)
		tbl.set_row_spacings(4)
		idea = self.e_vasca.get_active_text()
		print idea
		if idea == 'Dolce':
		
			tbl.attach(self.new_label(_("Volume:")), 0, 1, 2, 3)
			tbl.attach(self.new_label(_("Piante Inseribili:")), 0, 1, 3, 4)
			tbl.attach(self.new_label(_("Numero di pesci 3-4 cm:")), 0 ,1, 4, 5)
		else:
			tbl.attach(self.new_label(_("Volume:")), 0, 1, 2, 3)
		
	def new_label(self, txt, bold=True):
		lbl = gtk.Label()
		lbl.set_use_markup(True)
		
		if bold:
			lbl.set_label('<b>' + txt + '</b>')
		else:
			lbl.set_label(txt)
		
		lbl.set_alignment(0.0, 0.5)
		
		return lbl
