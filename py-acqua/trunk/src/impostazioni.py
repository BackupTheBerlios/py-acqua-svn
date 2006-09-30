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

import os, os.path
import sys
import utils
from xml.dom.minidom import parse, getDOMImplementation

# Valori per il tipo dolce
dolce_values = {
	'ph' :	[6, 8, None],
	'kh' :	[3, 8, None],
	'gh' :	[7, 20, None],
	'no2' :	[0, 0.7, None],
	'no3' :	[20, 100, None],
	'con' :	[100, 1500, None],
	'am' :	[0, 0.5, None],
	'fe' :	[3, 6, None],
	'ra' :	[0, 0.3, None],
	'fo' :	[0, 3, None],
	
	# Questi tre nn vengono utilizzati attualmente
	
	'cal' :	[None, None, None],	# valore marino (inutilizzato qui)
	'mag' :	[None, None, None],	# idem
	'den' :	[None, None, None]	# lo stesso
}

# Valori per il tipo marino
marino_values = {
	'ph' :	[7.7, 8.5, None],
	'kh' :	[4, 11, None],
	'gh' :	[None, None, None],	# inutilizzato.. valore troppo alto
	'no2' :	[0, 0.5, None],		# 0 valore ideale
	'no3' :	[0, 50,	None],		# idem
	'con' :	[None, None, None],	# inutilizzato
	'am' :	[0, 0.5, None],
	'fe' :	[0, 3, None],
	'ra' :	[0, 0.5, None],
	'fo' :	[0, 0.7, None],
	
	# Non vengono utilizzati
	
	'cal' :	[300, 500, None],
	'mag' :	[1100, 1500, None],
	'den' :	[1020, 1028, None]
}

gui_values = {
	'show_tips' :	True,
	'skin' :	'default',
	'lang' :	'it'
}

class Prefs(object):
	def __init__ (self):
		self.values = gui_values
		self.collection = {"dolce" : dolce_values, "marino" : marino_values}
	def Dump (self):
		print self.values
		print self.collection
	def Load (self):
		try:
			doc = parse (os.path.join (utils.HOME_DIR, "pyacqua.xml"))
		except:
			print "pyacqua.xml not found.. using default values"
			return
		
		if doc.documentElement.tagName == "pyacqua": # Seems valid
			
			for node in doc.documentElement.childNodes:
				
				if node.nodeName == "values":
					self.parseValues (node)
					
				if node.nodeName == "preferences":
					self.parsePreferences (node)
	
	def parseValues (self, node):
		for i in node.childNodes:
			if i.nodeName == "collection":
				self.parseCollection (i.attributes ["name"].nodeValue, i)
	
	def parseCollection (self, name, node):
		dict = {}
		for i in node.childNodes:
			if i.nodeName == "value":
				try:
					id = i.attributes ["id"].nodeValue
					min, max, ide = None, None, None
					
					if i.attributes.has_key ("min"):
						min = float (i.attributes ["min"].nodeValue)
					if i.attributes.has_key ("max"):
						max = float (i.attributes ["max"].nodeValue)
					if i.attributes.has_key ("ideal"):
						ide = float (i.attributes ["ideal"].nodeValue)
					
					dict [id] = (min, max, ide)
				except:
					print "Float error in", id
		
		if len (dict) > 0:
			self.collection [name] = dict
	
	def parsePreferences (self, node):
		for i in node.childNodes:
			if i.nodeName == "bool": self.parseWithConverter (i, bool)
			if i.nodeName == "string": self.parseWithConverter (i, str)
			if i.nodeName == "float": self.parseWithConverter (i, float)
			if i.nodeName == "int": self.parseWithConverter (i, int)
	
	def parseWithConverter (self, node, converter):
		id = node.attributes ["id"].nodeValue
		val = node.attributes ["value"].nodeValue
		
		try:
			if converter == bool:
				if val.lower () == "true":
					val = True
				else:
					val = False #diamo maggior priorita' al false
			else:
				val = converter (val)
			
			old = None
			
			if self.values.has_key(id):
				old = self.values [id]
			
			if old != None:
				if type (old) == type (val):
					print "Same type.. nice"
					self.values [id] = val
				else:
					print "Type mismatch in", id
					print "Ignoring the new value", val, "old =", old
			else:
				self.values[id] = val
		except:
			print "Error while converting", id, "to", converter
	
	def get (self, me):
		your_girlfriend = self.values
		if me in your_girlfriend:
			return your_girlfriend [me]
		else:
			return None
		
	def set (self, name, val):
		self.values [name] = val
	
	def save (self):
		doc = getDOMImplementation ().createDocument (None, "pyacqua", None)
		
		values = doc.createElement ("values")
		prefs  = doc.createElement ("preferences")
		
		root = doc.documentElement
		root.appendChild (values); root.appendChild (prefs)
		
		self.dump_collections (values, doc)
		self.dump_preferences (prefs, doc)
		
		try:
			writer = open (os.path.join (utils.HOME_DIR, "pyacqua.xml"), "w")
			doc.writexml (writer, '\t', '\t', '\n')
			writer.close ()
		except:
			print "Error while saving pyacqua.xml"
	
	def dump_collections (self, node, doc):
		element = None
		
		for i in self.collection:
			element = doc.createElement ("collection"); element.setAttribute ("name", i)
			node.appendChild (element)
			
			for x in self.collection[i]:
				tup = self.collection[i][x]
				
				if tup != (None, None, None):
					current = doc.createElement ("value")
					current.setAttribute ("id", x)
					
					if tup [0]:
						current.setAttribute ("min", str (tup[0]))
					if tup [1]:
						current.setAttribute ("max", str (tup[1]))
					if tup [2]:
						current.setAttribute ("ideal", str (tup[2]))
					
					element.appendChild (current)
	
	def dump_preferences (self, node, doc):
		element = None
		
		for i in self.values:
			if type (self.values[i]) == bool:
				element = doc.createElement ("bool")
			elif type (self.values[i]) == str:
				element = doc.createElement ("string")
			elif type (self.values[i]) == int:
				element = doc.createElement ("int")
			elif type (self.values[i]) == float:
				element = doc.createElement ("float")
			
			if element != None:
				element.setAttribute ("id", i)
				element.setAttribute ("value", str (self.values[i]))
				node.appendChild (element)
	
	def get_collection (self, name):
		if self.collection.has_key (name):
			return self.collection[name]
		else:
			return None
	
	def get_names_of_collections (self):
		lst = []
		
		for i in self.collection:
			lst.append (i)
		
		return lst
	
	def delete_collection (self, name):
		if self.collection.has_key (name):
			del self.collection[name]
	
	def add_collection (self, name, collection):
		self.collection [name] = collection

# Magari sarebbe stato meglio un approccio singletons?
m_pref = None

def check_instance ():
	global m_pref
	
	if not m_pref:
		m_pref = Prefs ()
		m_pref.Load ()

def get (name):
	global m_pref
	
	check_instance ()
	return m_pref.get (name)

def set (name, val):
	global m_pref
	
	check_instance ()
	ret = m_pref.get (name)
	
	if ret == None or (type (ret) == type (val)):
		m_pref.set (name, val)

def get_collection (name):
	global m_pref
	
	check_instance ()
	return m_pref.get_collection (name)

def get_names_of_collections ():
	global m_pref
	
	check_instance ()
	return m_pref.get_names_of_collections ()

def delete_collection (name):
	global m_pref
	
	check_instance ()
	m_pref.delete_collection (name)

def add_collection (name, collection):
	global m_pref
	
	check_instance ()
	m_pref.add_collection (name, collection)

def save ():
	global m_pref
	
	check_instance ()
	m_pref.save ()