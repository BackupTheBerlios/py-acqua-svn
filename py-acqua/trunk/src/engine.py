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
import glob
import sys
import impostazioni
import utils

class Plugin:
	__name__ = ""
	__desc__ = ""
	__ver__ = ""
	__author__ = ""
	__preferences__ = {}
	
	def start (self):
		pass
	def stop (self):
		pass 

class PluginEngine:
	def __init__ (self):
		self.array = list () # Lista per contenere l'elenco di tutti i plugin
		self.load_defaults ()
	
	def load_defaults (self):
		# Carichiamo tutti i plugin presenti in Plugin/
		
		path = os.path.join(utils.DHOME_DIR, 'Plugin')

		for i in glob.glob(path + "/*.py"):
			if os.path.isfile(os.path.join(path, i)):
				file = os.path.join (path, i)
				base = os.path.basename(file)
				
				if base != "__init__.py":
					print _("Carico <%s>") % base[:-3]
					#if self.load ("Plugin." + base[:-3], base[:-3]) == False:
					if not self.load (path, base[:-3], base[:-3]):
						print _("Errori... Ignoro")
		
	def load (self, path, name, klass):
		# Aggiungiamo la path
			old = sys.path
			sys.path.append (path)
		
			print "Carico il modulo senza try/except.. fixami prima della revisione finale"
		#try:
			module = __import__ (name)#, globals (), locals (), [klass])
			instance = vars(module)[klass]

			for i in self.array:
				if i.__class__ == instance:
					return False
			
			plugin = instance ()
			
			# Roba di preferenze... raccomandati di merda -.- gh
			
			for i in plugin.__preferences__:
				ret = impostazioni.get (i)
				
				if ret == None:
					impostazioni.set (i, plugin.__preferences__[i])
				else:
					if type (ret) == type (plugin.__preferences__[i]):
						plugin.__preferences__[i] = ret
			
			plugin.start ()
			
			self.array.append (plugin)
			
			print ">> Restoring path"
			sys.path = old

			return True
		#except:
		#	print ">> Restoring path"
		#	sys.path = old

		#	print "!! %s::%s (%s)" % (klass, sys.exc_value, sys.exc_type)
		#	return False
