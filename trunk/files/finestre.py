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

class main(gtk.Window):
	def __init__(self, width, heigth, title, border):
		gtk.Window.__init__(self)
		self.set_title(title)
		self.set_size_request(width, heigth)
		self.set_border_width(border)
		self.set_resizable(gtk.FALSE)
		self.connect("destroy", gtk.main_quit)
class win(gtk.Window):
	def __init__(self, width, heigth, title, border):
		gtk.Window.__init__(self)
		self.set_title(title)
		self.set_size_request(width, heigth)
		self.set_border_width(border)
		self.set_resizable(gtk.FALSE)
		#self.connect("destroy", self.chiudi)#gtk.main_quit)
		self.connect("delete_event", self.delete_event)
		
	def delete_event(self, widget, event, data=None):
		widget.hide()
		#return gtk.FALSE
		
	def chiudi(self, widget, event):
		return gtk.main_quit()
		
#class dialog(gtk.Dialog):
	#def __init__(self, title, message_type, label, buttons=gtk.BUTTONS_CLOSE):
		#gtk.Dialog.__init__(title, gtk.DIALOG_MODAL, message_type, buttons, label)
		
class file(gtk.FileSelection):
	def __init__(self):
		gtk.FileSelection.__init__(self, "Apri...")
		self.cancel_button.connect_object("clicked", gtk.Widget.destroy, self)
		self.ok_button.connect("clicked", self.get_name)
		self.show()
	
	def delete_event(self, widget, event, data=None):
		widget.hide()
		
	def get_name(self, widget, data=None):
		filename = self.get_filename()
		#return self.delete_event()
