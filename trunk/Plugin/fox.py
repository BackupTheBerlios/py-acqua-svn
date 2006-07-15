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
		self.set_title(_("Fox Plugin"))
		self.set_size_request (600, 400)
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")

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
		
		sw = gtk.ScrolledWindow ()
		sw.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type (gtk.SHADOW_ETCHED_IN)
		#sw.add(box)
		sw.add_with_viewport (box)
		self.add(sw)
		
		f1 = gtk.Frame(_('Sonde')); f2 = gtk.Frame(_('Uscite')); f3 = gtk.Frame(_('Regolazione Co2'))

		box.pack_start (f1, False, False, 0)
		box.pack_start (f2, False, False, 0)
		box.pack_start (f3, False, False, 0)
		
		
		fbox = gtk.HBox ()
		f1_checks = list ()
		x = 1
		for i in (_("pH1"), _("pH2"), _("Temperatura"), _("Redox")):
			tmp = gtk.CheckButton (i)
			f1_checks.append (tmp)
			
			fbox.pack_start (tmp, False, False, 0)


		f1.add (fbox)

		# Aggiungi il resto
		
		tbl = gtk.Table(4, 2)
		tbl.set_border_width(5)
		
		x = 0; labels = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'); f2_checks = list ()
		for i in labels:
			widget = gtk.CheckButton(_("Uscita ") + i)
			f2_checks.append (widget)
			tbl.attach (widget, x, x+1, 0, 1, xoptions=gtk.SHRINK); x += 1
		
		lst = [_("Filtro"), _("Co2"), _("Pompa"), _("Neon 1"), _("Neon 2"), _("Neon 3"), _("Neon 4")]
		
		self.uscita1 = utils.Combo (lst)
		self.uscita2 = utils.Combo (lst)	
		self.uscita3 = utils.Combo (lst)	
		self.uscita4 = utils.Combo (lst)
		self.uscita5 = utils.Combo (lst)
		self.uscita6 = utils.Combo (lst)
		self.uscita7 = utils.Combo (lst)
		self.uscita8 = utils.Combo (lst)
		self.uscita9 = utils.Combo (lst)
		self.uscita10 = utils.Combo (lst)
		
		
		tbl.attach(self.uscita1, 0, 1, 1, 2, xoptions=0)
		tbl.attach(self.uscita2, 1, 2, 1, 2, xoptions=0)
		tbl.attach(self.uscita3, 2, 3, 1, 2, xoptions=0)
		tbl.attach(self.uscita4, 3, 4, 1, 2, xoptions=0)
		tbl.attach(self.uscita5, 4, 5, 1, 2, xoptions=0)
		tbl.attach(self.uscita6, 5, 6, 1, 2, xoptions=0)
		tbl.attach(self.uscita7, 6, 7, 1, 2, xoptions=0)
		tbl.attach(self.uscita8, 7, 8, 1, 2, xoptions=0)
		tbl.attach(self.uscita9, 8, 9, 1, 2, xoptions=0)
		tbl.attach(self.uscita10, 9, 10, 1, 2, xoptions=0)
		
		
		tbl.attach(utils.new_label(_('Accensione')), 0, 1, 2, 3, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Accensione')), 1, 2, 2, 3, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Accensione')), 2, 3, 2, 3, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Accensione')), 3, 4, 2, 3, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Accensione')), 4, 5, 2, 3, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Accensione')), 5, 6, 2, 3, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Accensione')), 6, 7, 2, 3, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Accensione')), 7, 8, 2, 3, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Accensione')), 8, 9, 2, 3, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Accensione')), 9, 10, 2, 3, xoptions=gtk.SHRINK)
		
		
		
		self.usc_1 = utils.TimeEntry ()
		self.usc_2 = utils.TimeEntry ()
		self.usc_3 = utils.TimeEntry ()
		self.usc_4 = utils.TimeEntry ()
		self.usc_5 = utils.TimeEntry ()
		self.usc_6 = utils.TimeEntry ()
		self.usc_7 = utils.TimeEntry ()
		self.usc_8 = utils.TimeEntry ()
		self.usc_9 = utils.TimeEntry ()
		self.usc_10 = utils.TimeEntry ()
		
		
		tbl.attach(self.usc_1, 0, 1, 3, 4, xoptions=0)
		tbl.attach(self.usc_2, 1, 2, 3, 4, xoptions=0)
		tbl.attach(self.usc_3, 2, 3, 3, 4, xoptions=0)
		tbl.attach(self.usc_4, 3, 4, 3, 4, xoptions=0)
		tbl.attach(self.usc_5, 4, 5, 3, 4, xoptions=0)
		tbl.attach(self.usc_6, 5, 6, 3, 4, xoptions=0)
		tbl.attach(self.usc_7, 6, 7, 3, 4, xoptions=0)
		tbl.attach(self.usc_8, 7, 8, 3, 4, xoptions=0)
		tbl.attach(self.usc_9, 8, 9, 3, 4, xoptions=0)
		tbl.attach(self.usc_10, 9, 10, 3, 4, xoptions=0)
		
		
		tbl.attach(utils.new_label(_('Spegnimento')), 0, 1, 4, 5, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Spegnimento')), 1, 2, 4, 5, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Spegnimento')), 2, 3, 4, 5, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Spegnimento')), 3, 4, 4, 5, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Spegnimento')), 4, 5, 4, 5, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Spegnimento')), 5, 6, 4, 5, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Spegnimento')), 6, 7, 4, 5, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Spegnimento')), 7, 8, 4, 5, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Spegnimento')), 8, 9, 4, 5, xoptions=gtk.SHRINK)
		tbl.attach(utils.new_label(_('Spegnimento')), 9, 10, 4, 5, xoptions=gtk.SHRINK)
		
		self.usc_11 = utils.TimeEntry ()
		self.usc_21 = utils.TimeEntry ()
		self.usc_31 = utils.TimeEntry ()
		self.usc_41 = utils.TimeEntry ()
		self.usc_51 = utils.TimeEntry ()
		self.usc_61 = utils.TimeEntry ()
		self.usc_71 = utils.TimeEntry ()
		self.usc_81 = utils.TimeEntry ()
		self.usc_91 = utils.TimeEntry ()
		self.usc_111 = utils.TimeEntry ()
		
		tbl.attach(self.usc_11, 0, 1, 5, 6, xoptions=0)
		tbl.attach(self.usc_21, 1, 2, 5, 6, xoptions=0)
		tbl.attach(self.usc_31, 2, 3, 5, 6, xoptions=0)
		tbl.attach(self.usc_41, 3, 4, 5, 6, xoptions=0)
		tbl.attach(self.usc_51, 4, 5, 5, 6, xoptions=0)
		tbl.attach(self.usc_61, 5, 6, 5, 6, xoptions=0)
		tbl.attach(self.usc_71, 6, 7, 5, 6, xoptions=0)
		tbl.attach(self.usc_81, 7, 8, 5, 6, xoptions=0)
		tbl.attach(self.usc_91, 8, 9, 5, 6, xoptions=0)
		tbl.attach(self.usc_111, 9, 10, 5, 6, xoptions=0)
		
		
		
		
		tbl_alba = gtk.Table(2, 2)
		tbl_alba.set_border_width(5)
		
		
		self.co1 = gtk.CheckButton ("Co2 Permanente")
		tbl_alba.attach(self.co1, 0, 1, 6, 7, xoptions=gtk.SHRINK)
		
		self.co2 = gtk.CheckButton ("Co2 Regolata dal timer della luce")
		tbl_alba.attach(self.co2, 0, 1, 7, 8, xoptions=gtk.SHRINK)
		
		self.co3 = gtk.CheckButton ("Co2 Regolata dal pH")
		tbl_alba.attach(self.co3, 0, 1, 8, 9, xoptions=gtk.SHRINK)
		
		tbl_alba.attach(utils.new_label(_('Valore di pH da mantenere')), 0, 1, 9, 10, xoptions=gtk.SHRINK)
		self.val_ph = utils.FloatEntry ()
		tbl_alba.attach(self.val_ph, 1, 2, 9, 10, xoptions=gtk.SHRINK)
		
		
		
		
		
		
		
		f2.add(tbl)
		f3.add(tbl_alba)
		
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
