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

class Importa (gtk.Window):
	def __init__ (self):
		gtk.Window.__init__ (self)
		
	

		self.set_title (_("Importa"))
		self.set_size_request (400, 200)
		self.set_icon_from_file ("pixmaps/logopyacqua.jpg")
		self.connect ('delete-event', self.exit)
	
		vbox = gtk.VBox()
		vbox.set_spacing(4)
		vbox.set_border_width(4)
		
		tbl = gtk.Table(3, 2)
		tbl.set_border_width(4)
		tbl.set_row_spacings(4)
		
		self.ver_sette = sette = gtk.RadioButton (None, _("Versione 0.7"))
		self.ver_otto = otto = gtk.RadioButton (sette, _("Versione 0.8"))
		
		tbl.attach(utils.new_label(_("Importa:")), 1, 2, 0, 1)
		tbl.attach(utils.new_label(_("Esporta:")), 1, 2, 1, 2)
		
		self.importa_db = utils.ImgEntry ()
		self.esporta_db = utils.ImgEntry ()
		
		tbl.attach(self.importa_db, 2, 3, 0, 1)
		tbl.attach(self.esporta_db, 2, 3, 1, 2)
		
		self.ver_sette = sette = gtk.RadioButton (None, _("Versione 0.7"))
		self.ver_otto = otto = gtk.RadioButton (sette, _("Versione 0.8"))
		
		box = gtk.VBox()
		box.pack_start(tbl, False, False, 0)
		box.pack_start (sette)
		box.pack_start (otto)
		self.add (box)
		self.show_all ()
	
	def exit (self, *w):
		self.hide ()
