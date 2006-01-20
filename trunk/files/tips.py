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
import random
import string
import os
import sys
class win7:
	def __init__(self):
		self.win = finestre.win(370, 180, "Py-Acqua Tips Tricks", 5)
		
		
		self.textview = gtk.TextView()
		self.textview.set_wrap_mode(gtk.WRAP_WORD)
		self.textbuffer = self.textview.get_buffer()
		self.win.add(self.textview)
		self.win.show_all()
	#def tip():
	
		tip_file = open("files/tip_of_the_day.txt","r")
	
		testo = tip_file.read()
		tip_file.close()
		lista_tips = []
		lista_tips = string.split(testo,"&")
		lunghezza_lista = len(lista_tips)
		x = random.randint(0,lunghezza_lista-1)
		lista = gtk.TextBuffer()
		lista.set_text(lista_tips[x])
		lista.set_text(lista_tips[x] + "\n\n" + "Dalle FAQ di it.hobby.acquari http://www.maughe.it/faq/faq.htm" )	
		
		self.textbuffer.set_text(testo)
