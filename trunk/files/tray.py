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
import pygtk
import gtk
import egg.trayicon

def Tray():
	
	t = egg.trayicon.TrayIcon("Pyacqua")
	image = gtk.Image()
	image.set_from_file('/home/luca/.pyacqua/pixmaps/tray.gif')
	#self.but_on.connect("toggled", self.on_toggled)
	#button = gtk.Button()
	button = gtk.ToggleButton ()
	button.set_relief (gtk.RELIEF_NONE)
	button.add(image)
	t.add(button)
	#button.connect('clicked', apri)
	button.connect("toggled", apri_2)
	
	t.show_all()
	gtk.main()
	
#def apri(self):
	#if app.App.active_toggle == False:
	#app.App.show()
	#return True
	#self.tray = True
	#print "if"
	#else:
	#	app.App.hide()
	#	print "else"
def apri_2(widget):
	if widget.get_active():
		app.App.show()
		return True
		print "active"
		#self.po = True
	else:
		#widget.set_label("Offline")
		app.App.hide()
		print "deactive"
