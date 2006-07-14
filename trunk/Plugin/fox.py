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



import app
import gtk
import files.utils as utils

class fox(gtk.Window):
	__name__ = "Fox"
	__desc__ = "Plugin per fox"
	__ver__ = "0.0.1"
	__author__ = "PyAcqua team"

	def __init__(self):
		gtk.Window.__init__ (self)
		self.create_gui ()

	def start (self):
		print ">> Starting", self.__name__
		
		menu = app.App.get_plugin_menu ()

		self.item = gtk.MenuItem ("Fox Plugin")
		self.item.connect ('activate', self.on_activated)
		self.item.show ()

		menu.append (self.item)
	
	def create_gui (self):
		# Qui viene costruita la gui

		box = gtk.VBox()
		box.set_spacing(4)
		box.set_border_width(4)
		
		f1 = gtk.Frame(_('Sonde')); f2 = gtk.Frame(_('Uscite'))#; f3 = gtk.Frame(_('Alba e Tramonto'))

		box.pack_start (f1, False, False, 0)
		box.pack_start (f2, False, False, 0)
		#box.pack_start (f3, False, False, 0)
		
		fbox = gtk.VBox ()
		f1_checks = list ()

		for i in (_("pH1"), _("pH2"), _("Temperatura"), _("Redox")):
			tmp = gtk.CheckButton (i)
			f1_checks.append (tmp)
			fbox.pack_start (tmp, False, False, 0)


		f1.add (fbox)

		# Aggiungi il resto
		
		tbl = gtk.Table(4, 2)
		tbl.set_border_width(5)
		
		x = 0; labels = ('1', '2', '3', '4'); f2_checks = list ()
		for i in labels:
			widget = gtk.CheckButton(_("Uscita ") + i)
			f2_checks.append (widget)
			tbl.attach (widget, x, x+1, 0, 1, yoptions=gtk.SHRINK); x += 1
		
		
		
		self.uscita1 = utils.Combo ()
		self.uscita1.append_text(_("Filtro"))
		self.uscita1.append_text(_("Co2"))
		self.uscita1.append_text(_("Pompa di movimento"))
		self.uscita1.append_text(_("Neon 1"))
		self.uscita1.append_text(_("Neon 2"))
		self.uscita1.append_text(_("Neon 3"))
		self.uscita1.append_text(_("Neon 4"))
		
		

		self.uscita2 = utils.Combo ()
		self.uscita3 = utils.Combo ()
		self.uscita4 = utils.Combo ()
		
		tbl.attach(self.uscita1, 0, 1, 1, 2, yoptions=0)
		tbl.attach(self.uscita2, 1, 2, 1, 2, yoptions=0)
		tbl.attach(self.uscita3, 2, 3, 1, 2, yoptions=0)
		tbl.attach(self.uscita4, 3, 4, 1, 2, yoptions=0)
		
		tbl.attach(utils.new_label(_('Accensione')), 0, 1, 2, 3, yoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Accensione')), 1, 2, 2, 3, yoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Accensione')), 2, 3, 2, 3, yoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Accensione')), 3, 4, 2, 3, yoptions=gtk.SHRINK)
		
		self.usc_1 = utils.DataButton ()
		self.usc_2 = utils.DataButton ()
		self.usc_3 = utils.DataButton ()
		self.usc_4 = utils.DataButton ()
		
		tbl.attach(self.usc_1, 0, 1, 3, 4, yoptions=0)
		tbl.attach(self.usc_2, 1, 2, 3, 4, yoptions=0)
		tbl.attach(self.usc_3, 2, 3, 3, 4, yoptions=0)
		tbl.attach(self.usc_4, 3, 4, 3, 4, yoptions=0)
		
		tbl.attach(utils.new_label(_('Spegnimento')), 0, 1, 4, 5, yoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Spegnimento')), 1, 2, 4, 5, yoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Spegnimento')), 2, 3, 4, 5, yoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Spegnimento')), 3, 4, 4, 5, yoptions=gtk.SHRINK)
		
		self.usc_5 = utils.DataButton ()
		self.usc_6 = utils.DataButton ()
		self.usc_7 = utils.DataButton ()
		self.usc_8 = utils.DataButton ()
		
		tbl.attach(self.usc_5, 0, 1, 5, 6, yoptions=0)
		tbl.attach(self.usc_6, 1, 2, 5, 6, yoptions=0)
		tbl.attach(self.usc_7, 2, 3, 5, 6, yoptions=0)
		tbl.attach(self.usc_8, 3, 4, 5, 6, yoptions=0)
		
		self.co1 = gtk.CheckButton ("Co2 Permanente")
		tbl.attach(self.co1, 0, 1, 6, 7, yoptions=0)
		
		self.co2 = gtk.CheckButton ("Co2 Regolata dal timer della luce")
		tbl.attach(self.co2, 0, 1, 7, 8, yoptions=0)
		
		self.co3 = gtk.CheckButton ("Co2 Regolata dal pH")
		tbl.attach(self.co3, 0, 1, 8, 9, yoptions=0)
		
		
		#tbl_alba = gtk.Table(2, 2)
		#tbl_alba.set_border_width(5)
		
		#tbl_alba.attach(utils.new_label(_('Alba')), 0, 1, 0, 1, yoptions=gtk.SHRINK)
		#tbl_alba.attach(utils.new_label(_('Tramonto')), 0, 1, 1, 2, yoptions=gtk.SHRINK)
		
		#qui e da modificare! invece che scegliere la data bisogna far scegliere
		# l ora dell alba e del tramonto.
		
		#self.alba = utils.DataButton ()
		#self.tramonto = utils.DataButton ()
		
		#tbl_alba.attach(self.alba, 1, 2, 0, 1, yoptions=0)
		#tbl_alba.attach(self.tramonto, 1, 2, 1, 2, yoptions=0)
		
		f2.add(tbl)
		#f3.add(tbl_alba)
		
		self.add(box)
		self.connect ('delete_event', self.exit)

	def stop (self):
		print "** Stopping", self.__name__

		self.item.hide ()
		self.item.destroy ()
	
	def on_activated(self, widget):
		self.show_all()
		
	def exit(self, *w):
		self.hide()
		return True # Per non distruggere il contenuto
