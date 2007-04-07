#!/usr/bin/env python
# -*- coding: iso-8859-15 -*- 
#Copyright (C) 2005, 2007 Luca Sanna - Italy
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

try:
	import pygtk
	pygtk.require ('2.0')
except:
	print "!! PyGtk Not present"

import os
os.environ['PATH'] += r";lib;etc;bin"

if os.environ.has_key ('PYTHONPATH'):
	os.environ['PYTHONPATH'] += r";eggmini"
else:
	os.environ['PYTHONPATH'] = r";eggmini"

import locale
import gettext

try:
	# Richiediamo gtk2
	import gtk
	import gobject
except:
	print _("You need to install GTKv2")

try:
	#import pysqlite2 as sqlite
	from pysqlite2 import dbapi2 as sqlite
except:
	print _("You need to install pysqlite")

def main ():
	
	APP = 'acqua'
	DIR = os.path.join (utils.DHOME_DIR, "locale")
	
	try:
		if impostazioni.get ("lang").lower () == "en":
			en = gettext.translation (APP, DIR, ["en"])
			en.install ()
			try:
				os.environ['LANG'] = "en_US"
				locale.setlocale (locale.LC_MESSAGES, "en_US")
			except: pass
		else:
			os.environ['LANG'] = "it_IT"
			it = gettext.translation (APP, DIR, [])
			it.install ()
	except (IOError, locale.Error), e:
		print "(%s): WARNING **: %s" % (APP, e)
		__builtins__.__dict__["_"] = gettext.gettext
	
	path = os.path.join (utils.DATA_DIR, "db")
	db = backend.get_backend_class ()(path)
	
	if not db.get_schema_presents ():
		t = backend.ColumnType
		
		db.create_table (
			"vasca",
			[
				"id", "vasca", "date", "nome", "litri", "tipo", "filtro", "co",
				"illuminazione", "reattore", "schiumatoio", "riscaldamento", "note", "img"
			],
			[
				t.INTEGER, t.TEXT, t.DATE, t.TEXT, t.FLOAT, t.TEXT, t.TEXT, t.TEXT,
				t.TEXT, t.TEXT, t.TEXT, t.TEXT, t.VARCHAR + 500, t.TEXT
			]
		)
		
		db.create_table (
			"test",
			[
				"id", "date", "vasca", "ph", "kh", "gh", "no", "noo", "con",
				"amm", "fe", "ra", "fo", "calcio", "magnesio", "densita", "limiti"
			],
			[
				t.INTEGER, t.DATE, t.TEXT, t.FLOAT, t.FLOAT, t.FLOAT, t.FLOAT,
				t.FLOAT, t.FLOAT, t.FLOAT, t.FLOAT, t.FLOAT, t.FLOAT, t.FLOAT,
				t.FLOAT, t.FLOAT, t.TEXT
			]
		)
		
		db.create_table (
			"pesci",
			[
				"id", "date", "vasca", "quantita", "nome", "note", "img"
			],
			[
				t.INTEGER, t.DATE, t.FLOAT, t.NUMERIC, t.TEXT, t.VARCHAR + 500, t.TEXT
			]
		)
		
		db.create_table (
			"invertebrati",
			[
				"id", "date", "vasca", "quantita", "nome", "note", "img"
			],
			[
				t.INTEGER, t.DATE, t.FLOAT, t.NUMERIC, t.TEXT, t.VARCHAR + 500, t.TEXT
			]
		)
		
		db.create_table (
			"piante",
			[
				"id", "date", "vasca", "quantita", "nome", "note", "img"
			],
			[
				t.INTEGER, t.DATE, t.FLOAT, t.NUMERIC, t.TEXT, t.VARCHAR + 500, t.TEXT
			]
		)
		
		db.create_table (
			"fertilizzante",
			[
				"id", "date", "nome", "quantita", "giorni", "note"
			],
			[
				t.INTEGER, t.DATE, t.TEXT, t.FLOAT, t.NUMERIC, t.VARCHAR + 500
			]
		)
		
		db.create_table (
			"spesa",
			[
				"id", "vasca", "data", "tipologia", "nome", "quantita", "soldi",
				"note", "img"
			],
			[
				t.INTEGER, t.TEXT, t.DATE, t.TEXT, t.TEXT, t.NUMERIC, t.TEXT,
				t.VARCHAR + 500, t.TEXT 
			]
		)
		
		db.create_table (
			"filtro",
			[
				"id", "date", "giorni", "note"
			],
			[
				t.INTEGER, t.DATE, t.NUMERIC, t.VARCHAR + 500
			]
		)
		
		db.create_table (
			"manutenzione",
			[
				"id", "vasca", "data", "tipo", "nome", "quantita", "giorni", "note"
			],
			[
				t.INTEGER, t.TEXT, t.DATE, t.TEXT, t.TEXT, t.TEXT, t.DATE, t.VARCHAR + 500
			]
		)
		
		db.set_schema_presents (True)
	
	merger.check_for_updates () #Controlliamo se ci sono update da fare

	gobject.threads_init ()
	
	app.App = app.Gui()
	app.App.p_engine = engine.PluginEngine ()
	app.App.p_backend = db
	
	#per il momento finche non si sistema non si usa la tray
	#utils.tray_apri()
	
	gtk.gdk.threads_enter ()
	app.App.main()
	gtk.gdk.threads_leave ()
	
	
	print _(">> Salvo le impostazioni prima di uscire")
	impostazioni.save ()

if __name__ == "__main__":
	# Dobbiamo caricare i moduli come import pyacqua.ecc
	
	import pyacqua.utils as utils
	
	utils.prepare_enviroment ()
	
	import pyacqua.app as app
	import pyacqua.engine as engine
	import pyacqua.merger as merger
	import pyacqua.impostazioni as impostazioni
	import pyacqua.backend as backend
	
	main ()
	
	
else:
	
	import utils
	
	utils.prepare_enviroment ()
	
	import app
	import engine
	import merger
	import impostazioni
	import backend
	
	main ()
