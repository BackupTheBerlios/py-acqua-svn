#!/usr/bin/env python
# -*- coding: iso-8859-15 -*- 
#Copyright (C) 2005, 2007 Py-Acqua
#http://www.pyacqua.net
#email: info@pyacqua.net  
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
from os.path import join, getsize
import md5

class Generator (object):
	"""
	Questa classe serve a generare una lista di checksum data una dir o
	semplicemente a generare un checksum di un determinato file.
	"""
	
	def checksum (path):
		"""
		Genera un checksum MD5 a partire dal percorso del file stesso.
		
		Esempio:
			>> print Generator.checksum ("/home/foo/file.zip")
			850359fd43501306f912380273aca66e
		"""
		
		fobj = file (path, 'rb')
		m = md5.new()

		while True:
			d = fobj.read(8096)
			if not d:
				break
			m.update(d)
		
		return m.hexdigest()

	def ParseDir (dir):
		"""
		Genera i checksum MD5 di tutti i file presenti in una dir.
		NB: Analizza i file che si trovano nelle sottodirectory mentre non scanna
		i file all'interno di cartelle di nome ".svn"
		
		Il risultato e' un dizionario del tipo:
		dict ["percorso_file_relativo"] = "md5_come_hex_string"
		"""
		
		stack = [dir]
		data = {}

		while stack:
			dir = stack.pop ()
			for file in os.listdir (dir):
				fullname = os.path.join (dir, file)
				if not os.path.isdir (fullname):
					data[fullname[2:]] = str (getsize (fullname)) + "|" + str (Generator.checksum (fullname))
				elif not os.path.islink (fullname):
					if file != ".svn":
						stack.append (fullname)
		return data
	
	# Dichiariamoli statici
	checksum = staticmethod (checksum)
	ParseDir = staticmethod (ParseDir)

# Testing
if __name__ == "__main__":
	data = Generator.ParseDir (".")
	for i in data:
		print "%s|%s" % (i, data[i])
