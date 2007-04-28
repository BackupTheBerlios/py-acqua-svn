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

import os.path
import utils
import generate
import shutil
from xml.dom.minidom import parse, getDOMImplementation

def fill_fs_structure (path):
	lst = path.split (os.path.sep); lst.pop () # Eliminiamo la parte del file

	current = utils.UPDT_DIR

	for i in lst:
		current = os.path.join (current, i)

		print _(">> Controllo"), current,
		
		if not os.path.exists (current):
			os.mkdir (current)
			print _("creato.")

def rmgeneric(path, __func__):
	try:
		__func__ (path)
		print _(">> Path Rimosso (%s)") % path
	except OSError, (errno, strerror):
		print _("!! Errore mentre rimuovevo %s (%s)") % (path, strerror)

def removeall (path):
	if not os.path.isdir (path):
		return
	files=os.listdir (path)
	
	for x in files:
		fullpath=os.path.join (path, x)
		if os.path.isfile (fullpath):
			f=os.remove
			rmgeneric (fullpath, f)
		elif os.path.isdir (fullpath):
			removeall (fullpath)
			f=os.rmdir
			rmgeneric (fullpath, f)

def update ():
	path = os.path.join (utils.UPDT_DIR, ".diff.xml")
	
	if not os.path.exists (path):
		return
	
	try:
		doc = parse (path)
	except:
		#eliminatutto 
		return
	
	if doc.documentElement.tagName == "pyacqua":
		for root in doc.documentElement.childNodes:
			if root.nodeName == "directory":
				directory = root.attributes["name"].nodeValue
				root_path = os.path.join (utils.UPDT_DIR, directory)
				
				if directory[0:2] == "$$" and directory[-2:] == "$$":
					# Fai un for e cancella tutti i file elencati
					# se la directory alla fine rimane vuota va cancellata
					
					for file_to_remove in root.childNodes:
						print ">> Removing file", os.path.join (root_path, file_to_remove.attributes["name"].nodeValue)
						os.remove (os.path.join (root_path, file_to_remove.attributes["name"].nodeValue))
					
					if os.path.isdir (root_path) and len (os.listdir (root_path)) == 0:
						print ">> Removing directory", root_path
						os.rmdir (root_path)
				else:
					# Controlla se esiste la directory altrimenti creala
					
					if not os.path.exists(root_path):
						print ">> Making directory", root_path
						os.mkdir (root_path)
					
					for node in root.childNodes:
						if node.nodeName == "file":
							tmp_path = os.path.join (root_path, node.attributes["name"].nodeValue)
							
							md5_v = generate.Generator.checksum (tmp_path)
							bytes_v = os.path.getsize (tmp_path)
							
							md5_n = node.attributes["md5"].nodeValue
							bytes_n = node.attributes["bytes"].nodeValue
							
							print "'%s' == '%s'" % (md5_n, md5_v)
							print "'%s' == '%s'" % (bytes_n, bytes_v)
							
							if str (md5_v) == str (md5_n) and int (bytes_v) == int (bytes_n):
								#/home/stack/.pyacqua/update/./pyacqua/src/generate.py
								print ">> File is ok. Moving"
								
								unz = os.path.join (
									root.attributes["name"].nodeValue,
									node.attributes["name"].nodeValue
								)
								
								# Bisogna ricreare le directory mancanti in PROG_DIR
								base = os.path.dirname (unz)
								
								# Facciamo un for
								i = utils.PROG_DIR
								for x in base.split (os.path.sep):
									if x != "" and not os.path.exists (os.path.join (i, x)):
										i = os.path.join (i, x)
										os.mkdir (i)
								
								unz = os.path.join (utils.PROG_DIR, unz)
								
								if os.path.exists (unz):
									os.remove (unz)
								
								shutil.move (tmp_path, os.path.join (utils.PROG_DIR, unz))
							else:
								print "!! MD5 or bytes wrong"
	
	print _(">> Pulisco la directory dell'Update")
	removeall (utils.UPDT_DIR)
	
	# Crea la nuova list.xml

def check_for_updates ():
	if os.path.exists (os.path.join (utils.UPDT_DIR, ".diff.xml")):
		print _(">> Aggiornamento disponibile. Procedo con il merging dei file")
		update ()
	else:
		print _(">> Nessun aggiornamento da concludere.")
