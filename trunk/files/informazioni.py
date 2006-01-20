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

import pygtk
pygtk.require('2.0')
import gtk
import finestre


class win8:
	def __init__(self):
		self.win = finestre.win(570, 250, "py-Acqua Informazioni", 0)
		self.table = gtk.Table(2, 2, gtk.FALSE)
		self.win.add(self.table)
		
		self.notebook = gtk.Notebook()
		self.notebook.set_tab_pos(gtk.POS_TOP)
		self.table.attach(self.notebook, 0, 2, 0, 1)
		self.notebook.show()
		
#########Pagina Licenza#########################################################
		self.label60 = gtk.Label("Licenza")
		self.fixed1 = gtk.Fixed()
		self.notebook.prepend_page(self.fixed1)
		text = """Py-Acqua is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software 
Foundation; either version 2 of the License, or (at your option) any later version. 
Py-Acqua is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.\n
You should have received a copy of the GNU General Public License along
with Py-Acqua; if not, write to the Free Software Foundation, Inc.,
51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA"""

		self.label61 = gtk.Label("py-Acqua")
		self.fixed1.put(self.label61, 230, 20)
		self.label62 = gtk.Label("py-Acqua è un programma\nper la gestione di un acquario")
		self.fixed1.put(self.label62, 160, 50)
		self.label63 = gtk.Label(text)	
		self.fixed1.put(self.label63, 10, 100)

################################################################################
########Pagina Scritto##########################################################		
		
		self.label64 = gtk.Label("Licenza")
		self.fixed2 = gtk.Fixed()
		self.notebook.prepend_page(self.fixed2)
		text1 = """LUCA SANNA - Founder and lead developer - pyacqua@gmail.com 
ENRICO GIUBERTONI - Web Site Manager - enrico.giubertoni@gmail.com 
FEDERICO DEGRANDIS - Package Manager - danger90@gmail.com 
MASSIMILIANO SIST - DB and Tips and Tricks Manager -  massimiliano.sist@gmail.com
PIETRO GRASSI - Release Tester - gnatophillum@gmail.com
PIERO MUSU - Graphic - admin@irk.it"""

		self.label65 = gtk.Label("Scritto da:")
		self.label66 = gtk.Label(text1)
		self.fixed2.put(self.label66, 2, 2)
################################################################################

		self.notebook.set_current_page(1)
		self.table.show()
		self.win.show_all()
