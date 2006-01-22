#!/usr/bin/env python
# -*- coding: iso-8859-15 -*- 
#Copyright (C) 2005, 2006 Luca Sanna - Italy
#http://pyacqua.altervista.org
#email: pyacqua@gmail.com  
#
#Team Members: 
#
#	LUCA SANNA -  	Founder and lead developer - pyacqua@gmail.com 
#	ENRICO GIUBERTONI  - Web Site Manager - enrico.giubertoni@gmail.com 
#	FEDERICO DEGRANDIS - Package Manager - danger90@gmail.com 
#	MASSIMILIANO SIST - DB and Tips and Tricks Manager -  massimiliano.sist@gmail.com
#	PIETRO GRASSI - Release Tester - gnatophillum@gmail.com
#	PIERO MUSU	 - Graphic Designer - admin@irk.it
#	
#	
#Please Refer to AUTHORS file for more Information
#
#Py-Acqua refers to the following libraries under GPL or other Free Licenses:
#PYTHON (http://www.python.org/psf/license.html)
#PYGTK (http://www.pygtk.org/about.html),
#PYSQLITE2 (http://initd.org/pub/software/pysqlite/)
#GTK (http://gladewin32.sourceforge.net/) 
#PYCHART (http://home.gna.org/pychart/)
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
import ConfigParser

minph = maxph = 0
minkh = maxkh = 0
mingh = maxgh = 0
minno2 = maxno2 = 0
minno3 = maxno3 = 0
mincon = maxcon = 0
minam = maxam = 0
minfe = maxfe = 0
minra = maxra = 0
minfe = maxfe = 0
minfo = maxfo = 0

def refresh():
	par = os.path.join('files', 'config.cfg')
	
	cfg = ConfigParser.ConfigParser()
	
	if os.path.isfile(par):
		cfg.read(par)
		
		minph = cfg.get("ph","min")
		maxph = cfg.get("ph","max")
		minkh = cfg.get("kh","min")
		maxkh = cfg.get("kh","max")
		mingh = cfg.get("gh","min")
		maxgh = cfg.get("gh","max")
		minno2 = cfg.get("no2","min")
		maxno2 = cfg.get("no2","max")
		minno3 = cfg.get("no3","min")
		maxno3 = cfg.get("no3","max")
		mincon = cfg.get("conducibilita","min")
		maxcon = cfg.get("conducibilita","max")
		minam = cfg.get("ammoniaca","min")
		maxam = cfg.get("ammoniaca","max")
		minfe = cfg.get("ferro","min")
		maxfe = cfg.get("ferro","max")
		minra = cfg.get("rame","min")
		maxra = cfg.get("rame","max")
		minfo = cfg.get("fosfati","min")
		maxfo = cfg.get("fosfati","max")
	else: 
		print "Non esiste il file di configurazione (config.cfg) scaricalo da http://pyacqua.altervista.org"

refresh()
