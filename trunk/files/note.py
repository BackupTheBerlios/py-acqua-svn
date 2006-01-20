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

class prova:
	def get_main_menu(self, win):
		accel_group = gtk.AccelGroup()
		item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
		item_factory.create_items(self.menu_items)
		win.add_accel_group(accel_group)
		self.item_factory = item_factory
		return item_factory.get_widget("<main>")
	
	def __init__(self):
		
		self.menu_items = (
			( "/_File",         None,         None, 0, "<Branch>" ),
			( "/File/_Nuovo",     "<control>N", None, 0, None ),
			( "/File/_Apri",    "<control>O", None, 0, None ),
			( "/File/_Salva",    "<control>S", None, 0, None ),
			( "/File/_Salva come...", None,         None, 0, None ),
			( "/File/sep1",	None,	None,	0,	"<Separator>" ),
			( "/File/Quit",     "<control>Q", gtk.main_quit, 0, None ))
			
		win = finestre.win(400, 400, "py-Acqua Note", 0)
		
		table = gtk.Table(2, 2, False)
		table.set_border_width(0)
		win.add(table)
		
		scrolled_window = gtk.ScrolledWindow()
		scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		
		menubar = self.get_main_menu(win)
		table.attach(menubar, 0, 1, 0, 1)
		table.attach(scrolled_window,0, 1, 1, 101)
		menubar.show()
		table.show()
	
		textview = gtk.TextView()
		buffer = textview.get_buffer()
		textview.set_justification(gtk.JUSTIFY_LEFT)
		textview.set_editable(gtk.TRUE)
		scrolled_window.add_with_viewport(textview)
		win.show_all()
		

	def main(self):
		gtk.main()
		
if __name__ == "__main__":
	prova = prova()
	prova.main()
