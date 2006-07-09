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

import gtk
from pysqlite2 import dbapi2 as sqlite

class dbupdate:
	def updatedb (self):
		connessione=sqlite.connect ("Data/db")
		cursore=connessione.cursor ()

		def check (query):
			try:
				cursore.execute (query)
			except:
				print "Errore nella query (%s)" % query

		###################################
		# Versione 0.7
		
		check ("create table spese(id integer, date DATE, vasca FLOAT, tipologia TEXT, quantita NUMERIC, nome TEXT,soldi TEXT, img TEXT)")
		check ("create table invertebrati(id integer, date DATE, vasca FLOAT, quantita NUMERIC, nome TEXT, img TEXT)")
		check ("alter table vasca add reattore TEXT")
		check ("alter table vasca add schiumatoio TEXT")
		check ("alter table vasca add riscaldamento TEXT")
		check ("alter table vasca add note VARCHAR(500)")
		check ("alter table test add vasca FLOAT")
		check ("alter table test add calcio FLOAT")
		check ("alter table test add magnesio FLOAT")
		check ("alter table test add densita FLOAT")
		
		###################################
		# Versione 1.0

		check ("alter table vasca add note VARCHAR(500)")
		check ("alter table pesci add note VARCHAR(500)")
		check ("alter table piante add note VARCHAR(500)")
		check ("alter table invertebrati add note VARCHAR(500)")
		check ("alter table fertilizzante add note VARCHAR(500)")
		check ("alter table spese add note VARCHAR(500)")
		check ("alter table filtro add note VARCHAR(500)")

		connessione.commit ()
