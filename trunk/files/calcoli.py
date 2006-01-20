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

class win2:
	#def delete_event(self, widget, event):
		#widget.hide()
	def __init__(self):
		
		self.win = finestre.win(600, 250, "Py-Acqua Calcoli", 5)
		
		self.fixed = gtk.Fixed()
		self.win.add(self.fixed)
		####
		#self.win.connect("delete_event", delete_event)
		
		self.win
		self.label1 = gtk.Label("Inserisci la larghezza in cm:")
		self.fixed.put(self.label1, 2, 2)
		self.label2 =  gtk.Label("Inserisci la lunghezza in cm:")
		self.fixed.put(self.label2, 200, 2)
		self.label3 = gtk.Label("Inserisci l'altezza in cm:")
		##
		self.fixed.put(self.label3, 400, 2)
		self.entry1 = gtk.Entry(30)
		self.fixed.put(self.entry1, 2, 30)
		self.entry2 = gtk.Entry(30)
		self.fixed.put(self.entry2, 200, 30)
		self.entry3 = gtk.Entry(30)
		self.fixed.put(self.entry3, 400, 30)
		####
		self.label4 = gtk.Label("Volume:")
		self.fixed.put(self.label4, 50, 80)
		self.label5 = gtk.Label("Piante inseribili:")
		self.fixed.put(self.label5, 230, 80)
		self.label6 = gtk.Label("Numero di pesci da 3-4 cm:")
		self.fixed.put(self.label6, 390, 80)
		##
		self.label7 = gtk.Label(0)
		self.fixed.put(self.label7, 70, 105)
		self.label8 = gtk.Label(0)
		self.fixed.put(self.label8, 270, 105)
		self.label9 = gtk.Label(0)
		self.fixed.put(self.label9, 470, 105)
		####
		self.label10 = gtk.Label("Numero pesci da 5-6 cm:")
		self.fixed.put(self.label10, 2, 140)
		self.label11 = gtk.Label("Watt per piante esigenti:")
		self.fixed.put(self.label11, 200, 140) 
		self.label12 = gtk.Label("Watt per piante poco esigenti:")
		self.fixed.put(self.label12, 388, 140)
		##
		self.label13 = gtk.Label(0)
		self.fixed.put(self.label13, 70, 165)
		self.label14 = gtk.Label(0)
		self.fixed.put(self.label14, 270, 165)
		self.label15 = gtk.Label(0)
		self.fixed.put(self.label15, 470, 165)
		####
		self.button1 = gtk.Button("Calcola")
		self.button1.connect("clicked", self.calcola)
		self.fixed.put(self.button1, 150, 210)
		self.button2 = gtk.Button("Pulisci")
		self.button2.connect("clicked", self.pulisci_calcoli)
		self.fixed.put(self.button2, 250, 210)
		self.button3 = gtk.Button("Chiudi")
		#self.button3.connect("clicked", gtk.main_quit)
		self.button3.connect_object("clicked", gtk.Widget.destroy, self.win)
		self.fixed.put(self.button3, 350, 210)
		self.win.show_all()
		
	def delete_event(self, widget, event, data=None):
		return True
	
	#Funzioni del file
	def calcola(self, obj):
		try:
			a = int(self.entry1.get_text())
			b = int(self.entry2.get_text())
			c = int(self.entry3.get_text())
			
			
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

		self.label7.set_text(str(e))
		self.label8.set_text(str(f))
		self.label9.set_text(str(g))
		self.label13.set_text(str(h))
		self.label14.set_text(str(i))
		self.label15.set_text(str(l))
	
	def pulisci_calcoli(self, obj):
		self.entry1.set_text("")
		self.entry2.set_text("")
		self.entry3.set_text("")
