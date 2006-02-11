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
import sys
import ConfigParser

#TODO: imposta i valori di default
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
show_tips = "1"

def save():
	print "Salvo le impostazioni..."
	
	try:
		par = open(os.path.join('files', 'config.cfg'), 'w')
		
		cfg = ConfigParser.ConfigParser()
		
		cfg.add_section("ph")
		cfg.add_section("kh")
		cfg.add_section("gh")
		cfg.add_section("no2")
		cfg.add_section("no3")
		cfg.add_section("conducibilita")
		cfg.add_section("ammoniaca")
		cfg.add_section("ferro")
		cfg.add_section("rame")
		cfg.add_section("fosfati")
		cfg.add_section("GUI")
		
		global show_tips
		global minph, maxph, minkh, maxkh
		global minam, maxam, minfe, maxfe
		global minra, maxra, minfo, maxfo
		global mingh, maxgh, minno2, maxno2
		global minno3, maxno3, mincom, maxcon
		
		cfg.set("ph", "min", minph)
		cfg.set("ph", "max", maxph)
		
		cfg.set("kh", "min", minkh)
		cfg.set("kh", "max", maxkh)
		
		cfg.set("gh", "min", mingh)
		cfg.set("gh", "max", maxgh)
		
		cfg.set("no2", "min", minno2)
		cfg.set("no2", "max", maxno2)
		
		cfg.set("no3", "min", minno3)
		cfg.set("no3", "max", maxno3)
		
		cfg.set("conducibilita", "min", mincon)
		cfg.set("conducibilita", "max", maxcon)
		
		cfg.set("ammoniaca", "min", minam)
		cfg.set("ammoniaca", "max", maxam)
		
		cfg.set("ferro", "min", minfe)
		cfg.set("ferro", "max", maxfe)
		
		cfg.set("rame", "min", minra)
		cfg.set("rame", "max", maxra)
		
		cfg.set("fosfati", "min", minfo)
		cfg.set("fosfati", "max", maxfo)
		
		cfg.set("GUI", "show_tips", show_tips)
		
		cfg.write(par)
		
		par.flush()
		par.close()
	except:
		print "Errore nel salvataggio del file di configurazione (%s)" % sys.exc_value
		
def refresh():
	par = os.path.join('files', 'config.cfg')
	
	cfg = ConfigParser.ConfigParser()
	
	if os.path.isfile(par):
		try:
			cfg.read(par)
			
			global show_tips
			global minph, maxph, minkh, maxkh
			global minam, maxam, minfe, maxfe
			global minra, maxra, minfo, maxfo
			global mingh, maxgh, minno2, maxno2
			global minno3, maxno3, mincom, maxcon

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
			show_tips = cfg.get("GUI", "show_tips")
		except:
			print "Errore nel caricamento dei valori.. uso quelli di default"
	else:
		print "File config.cfg non trovato.. salvo la configurazione di default"
		save()
refresh()
