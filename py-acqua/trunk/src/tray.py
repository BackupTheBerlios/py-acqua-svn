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
import os

if os.name != 'nt':
	try:
		import eggmini.trayicon as eggmini
	except:
		try:
			import egg.trayicon as eggmini
		except:
			print _("!! Errore: il modulo per la tray non puo' essere importato")
else:
	import win32api
	import win32gui
	import win32con
	import win32utils

import os.path
import utils

if os.name != 'nt':
	class TrayIcon (eggmini.TrayIcon):
		def __init__ (self):
			eggmini.TrayIcon.__init__ (self, "PyAcqua")
			
			image = gtk.Image ()
			image.set_from_file (os.path.join (utils.DPIXM_DIR, "logopyacqua.jpg"))
			
			eb = gtk.EventBox ()
			eb.add (image)
			
			self.add (eb)
			
			self.menu = gtk.Menu ()
			
			it = gtk.ImageMenuItem (gtk.STOCK_QUIT)
			it.connect ('activate', self.on_quit)
			
			self.menu.append (it)
			
			eb.connect ('button-press-event', self.on_button)
			
			self.show_all ()
			
		def on_button (self, widget, event):
			# se == 1 e' il sinistro -> mostra/nascondi
			# se == 3 e' il destro -> popup menu
			print "button", event.button

			if event.button == 1:
				if app.App.tray:
					app.App.hide ()
				else:
					app.App.show ()
					
				app.App.tray = not app.App.tray
			elif event.button == 3:
				self.menu.popup (None, None, None, event.button, event.time)
				self.menu.show_all ()
				
		def on_quit (self, item):
			gtk.main_quit ()
else:
	class TrayIcon (object):
		def __init__ (self):
			self.win32ext = win32utils.GTKWin32Ext (app.App)
			self.win32ext.add_notify_icon (win32gui.LoadIcon (win32api.GetModuleHandle(None), 1), "PyAcqua")

			self.menu = gtk.Menu ()
			
			it = gtk.ImageMenuItem (gtk.STOCK_QUIT)
			it.connect ('activate', self.on_quit)
			
			self.menu.append (it)
			self.menu.show_all ()

			self.win32ext.notify_icon.menu = self.menu
			self.win32ext.message_map ({
				win32utils.WM_TRAYMESSAGE: self.on_notifyicon_activity
				})
			self.win32ext.show_balloon_tooltip (_("PyAcqua"), _("PyAcqua avviato.\nPremi su questa icona per ridurlo a icona.\nRipremi su questa icona per ripristinare."), 5, win32gui.NIIF_INFO)

		def on_notifyicon_activity(self, hwnd, message, wparam, lparam):
			if lparam == win32con.WM_RBUTTONDOWN:
				self.win32ext.notify_icon.menu.popup(None, None, None, 3, 0)
			elif lparam == win32con.WM_LBUTTONUP:
				self.win32ext.notify_icon.menu.popdown()
			elif lparam == win32con.WM_LBUTTONDOWN:
				if app.App.tray:
					app.App.hide ()
				else:
					app.App.show ()
					
				app.App.tray = not app.App.tray

		def on_quit (self, item):
			gtk.main_quit ()