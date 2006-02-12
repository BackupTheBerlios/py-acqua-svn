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
#import finestre
from pysqlite2 import dbapi2 as sqlite


class Calendario:
	
	def calendar_set_flags(self):
		options = 0
		for i in range(3):
			if self.settings[i]:
				options = options + (1<<i)
		if self.window:
			self.window.display_options(options)
			
	def calendar_toggle_flag(self, toggle):
		j = 0
		for i in range(3):
			if self.flag_checkboxes[i] == toggle:
				j = i
				
		self.settings[j] = not self.settings[j]
		self.calendar_set_flags()
		
	def __init__(self):
		connessione=sqlite.connect("Data/db")
		cursore=connessione.cursor()
		cursore.execute("select * from fertilizzante")		
		
		flags = [
			"Mostra il mese/anno",
			"Mostra i giorni"
			]
		self.window = None
		self.flag_checkboxes = 5*[None]
		self.settings = 5*[0]
		self.marked_date = 31*[0]
		
		window = finestre.win(272, 280, "py-Acqua Calendario", 5)
		
		calendar = gtk.Calendar()
		self.window = calendar
		self.calendar_set_flags()
		fixed = gtk.Fixed()
		vbox = gtk.VBox()
		window.add(fixed)
		
		fixed.put(calendar, 1, 1)
		fixed.put(vbox, 5, 220)
		
		for x in cursore.fetchall():
			day = x[4]
			self.calendar.mark_day(day)
		
		for i in range(len(flags)):
			toggle = gtk.CheckButton(flags[i])
			toggle.connect("toggled", self.calendar_toggle_flag)
			vbox.pack_start(toggle)
			self.flag_checkboxes[i] = toggle
			
		window.show_all()
