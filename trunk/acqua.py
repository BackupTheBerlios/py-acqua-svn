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

import os
__builtins__.__dict__["_"] = lambda x : x
os.environ['PATH'] += r";lib;etc;bin"

if os.environ.has_key ('PYTHONPATH'):
	os.environ['PYTHONPATH'] += r";eggmini"
else:
	os.environ['PYTHONPATH'] = r";eggmini"

import locale
import gettext

import files.utils as utils

utils.prepare_enviroment ()

import files.impostazioni

APP = 'acqua'
DIR = 'locale'

try:
	if files.impostazioni.get ("lang").lower () == "en":
		en = gettext.translation (APP, DIR, ["en"])
		en.install ()
		try:
			os.environ['LANG'] = "en_US"
			__builtins__.__dict__.delete("_")
			locale.setlocale (locale.LC_MESSAGES, "en_US")
		except: pass
	else:
		os.environ['LANG'] = "it_IT"
		__builtins__.__dict__["_"] = lambda x : x

except (IOError, locale.Error), e:
	print "(%s): WARNING **: %s" % (APP, e)
	__builtins__.__dict__["_"] = lambda x : x
	__builtins__.__dict__["ngettext"] = gettext.ngettext

try:
	# Richiediamo gtk2
	import pygtk
	pygtk.require('2.0')
except:
	# Gtk2 assente proviamo lo stesso con gtk
	pass

try:
	import gtk
	import gobject
except:
	print _("You need to install pyGTK or GTKv2")

try:
	#import pysqlite2 as sqlite
	from pysqlite2 import dbapi2 as sqlite
except:
	print _("You need to install pysqlite")

import app
import files.engine
import merger

path = os.path.join (utils.DATA_DIR, "db")
if not os.path.exists (path):
	connessione=sqlite.connect (os.path.join (utils.DATA_DIR, "db")) # Smazza altrimenti.. se nn c'e' lo crea
	cursore=connessione.cursor()
	cursore.execute("create table vasca(id integer, vasca TEXT, date DATE, nome TEXT, litri FLOAT, tipo TEXT, filtro TEXT, co TEXT, illuminazione TEXT, reattore TEXT, schiumatoio TEXT, riscaldamento TEXT, note VARCHAR(500), img TEXT)")
	cursore.execute("create table test(id integer, date DATE, vasca TEXT, ph FLOAT, kh FLOAT, gh FLOAT, no FLOAT, noo FLOAT, con FLOAT, amm FLOAT, fe FLOAT, ra FLOAT, fo FLOAT, calcio FLOAT, magnesio FLOAT, densita FLOAT, limiti TEXT)")
	cursore.execute("create table pesci(id integer, date DATE, vasca FLOAT, quantita NUMERIC, nome TEXT, note VARCHAR(500), img TEXT)")
	cursore.execute("create table invertebrati(id integer, date DATE, vasca FLOAT, quantita NUMERIC, nome TEXT, note VARCHAR(500), img TEXT)")
	cursore.execute("create table piante(id integer, date DATE, vasca FLOAT, quantita NUMERIC, nome TEXT, note VARCHAR(500), img TEXT)")
	cursore.execute("create table fertilizzante (id integer,date DATE, nome TEXT, quantita FLOAT, giorni NUMERIC, note VARCHAR(500))")
	cursore.execute("create table spese(id integer, date DATE, vasca FLOAT, tipologia TEXT, quantita NUMERIC, nome TEXT,soldi TEXT, note VARCHAR(500), img TEXT)")
	cursore.execute("create table filtro(id integer,date DATE, giorni NUMERIC, note VARCHAR(500))")
	connessione.commit()

if __name__ == "__main__":
	merger.check_for_updates () #Controlliamo se ci sono update da fare

	gobject.threads_init ()
	
	app.App = app.Gui()
	app.App.p_engine = files.engine.PluginEngine ()
	
	utils.tray_apri()
	
	gtk.gdk.threads_enter ()
	app.App.main()
	gtk.gdk.threads_leave ()
	
	
	print "Saving preferences before exiting..."
	files.impostazioni.save ()
