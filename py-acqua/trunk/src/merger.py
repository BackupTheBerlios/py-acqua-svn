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
	path = os.path.join (utils.UPDT_DIR, ".checklist")
	
	if not os.path.exists (path):
		return
	
	file = open (path, 'r')
	list = file.readlines ()
	file.close ()

	for i in list:
		line = i[:-1]
		name, bytes, sum = line.split ("|")
		
		path = os.path.join (utils.UPDT_DIR, name)

		new_path = os.path.join (".", name)

		bytes = int (bytes)

		print _(">> File %s") % path

		if sum == '0':
			# Questo file deve essere zappato via.. via!
			print _(">> Elimino %s") % name, 

			if os.path.isfile (new_path):
				os.remove (new_path)
				print _("OK (file)")
			elif os.path.isdir (new_path):
				os.rmdir (new_path)
				print _("OK (dir)")
		else:
			# File da aggiornare.. controlla il checksum se corretto sposta
			new_sum = generate.Generator.checksum (path)

			if new_sum == sum:
				print _(">> Checksum corretto. Adesso sposto ;)"),
				if os.path.isfile (new_path):
					os.remove (new_path)
					print _("OK (file)")
				elif os.path.isdir (new_path):
					os.rmdir (new_path)
					print _("OK (dir)")

				fill_fs_structure (name)
				os.rename (path, new_path)			
			else:
				print _("!! Errore nel checksum")
	
	print _(">> Pulisco la directory dell'Update")
	removeall (utils.UPDT_DIR)

def check_for_updates ():
	if os.path.exists (os.path.join (utils.UPDT_DIR, ".checklist")):
		print _(">> Aggiornamento disponibile. Procedo con il merging dei file")
		update ()
	else:
		print _(">> Nessun aggiornamento da concludere.")
