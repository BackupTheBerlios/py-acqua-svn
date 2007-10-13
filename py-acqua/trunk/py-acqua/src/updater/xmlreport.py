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

"""
Update staff.

$Id$
"""

__author__    = "Francesco Piccinno <stack.box@gmail.com>"
__version__   = "$Revision$"
__copyright__ = "Copyright (c) 2007 Francesco Piccinno"

import sys
import base64
import ConfigParser

from optparse import OptionParser
from database import DatabaseWrapper
from xml.dom.minidom import parse, parseString, getDOMImplementation

class ProgramInterface(object):
	
	def __init__(self, name):
		self.name = name

		self.options = {
			'%s.uselast'           % self.name : True,
			'%s.mainversion'       % self.name : 0,
			'%s.secondversion'     % self.name : 0,
			'%s.revision'          % self.name : 0,
			'%s.changelog'         % self.name : '',
			'%s.database'          % self.name : '',
			'%s.message'           % self.name : '',

			'%s.message-pre'       % self.name : '',
			'%s.message-post'      % self.name : '',

			'%s.mirrors'           % self.name : [],

			'%s.downloads-windows' % self.name : [],
			'%s.downloads-tarball' % self.name : [],
			'%s.downloads-svn'     % self.name : [],

			'%s.actions-pre'       % self.name : [],
			'%s.actions-post'      % self.name : [],

		}
	
	def get(self, option):
		return self.options['%s.%s' % (self.name, option)]
	
	def check(self, option):
		return "%s.%s" % (self.name, option) in self.options

	def set(self, option, value):
		self.options['%s.%s' % (self.name, option)] = value

class ListCreator(object):
	def __init__(self, database, info):
		self.db = DatabaseWrapper(database)

		self.info = info
		self.programs = {}

		self.readInfoFile()
	
	def readVersionFromDatabase(self, name):
		try:
			program = self.programs[name]

			t = map(
				int, self.db.select("SELECT mainversion, version, revision FROM program WHERE name=\"%s\"" % self.db.sanitize(name))[0]
			)
     
			program.set("mainversion", t[0])
			program.set("secondversion", t[1])
			program.set("revision", t[2])
		except:
			print "Cannot get the versions for program %s." % name
			sys.exit(-1)
	
	def readInfoFile(self):
		parser = ConfigParser.ConfigParser()
		parser.read(self.info)

		# First load the programs name
		for sec in parser.sections():
			if '.' not in sec:
				self.programs[sec] = ProgramInterface(sec)

		for sec in parser.sections():
			for opt in parser.options(sec):
				self.handleOption(sec.lower(), opt.lower(), parser.get(sec, opt))
		
		for k in self.programs:
			program = self.programs[k]
			if program.get("uselast"):
				self.readVersionFromDatabase(program.name)
	
	def handleOption(self, sec, opt, value):
		
		if '.' not in sec:
			program = self.programs[sec]
		else:
			program = self.programs[sec.split(".")[0]]
			sec = sec.split(".", 1)[1]

		if program.check(sec):
			# Mirrors or lists to handle

			# TODO: evalutate numbers

			check = lambda x, y: x[:len(y)] == y and ((len(x[len(y):]) > 0 and x[len(y):].isdigit()) or (len(x[len(y):]) == 0))

			if check(opt, "mirror"):
				program.get("mirrors").append(value)

			elif check(opt, "svn"):
				program.get("downloads-svn").append(value)
			elif check(opt, "tarball"):
				program.get("downloads-tarball").append(value)
			elif check(opt, "windows"):
				program.get("downloads-windows").append(value)

			elif check(opt, "pre"):
				program.get("actions-pre").append(value)
			elif check(opt, "post"):
				program.get("actions-post").append(value)
		else:
			# type checking
			
			if not program.check(opt):
				print "%s not used." % opt
				return

			converter = type(program.get(opt))
			
			# Necessary ugly code :D

			def strict_bool(x):
				if x == "1" or x.lower() == "true":
					return True
				elif x == "0" or x.lower() == "false":
					return False
				else:
					raise

			if converter == bool:
				converter = strict_bool

			try:
				if value != "":
					program.set(opt, converter(value))
			except:
				print "Type error detected:"
				print "%s must be of %s not %s" % (full, (converter == strict_bool) and (bool) or (converter), type(value))
				
				sys.exit(-1)
	
	def create(self):
		for i in self.programs:
			self.createXmlForProgram(i)

	def createXmlForProgram(self, name):
		
		program = self.programs[name]

		doc = getDOMImplementation().createDocument(None, "%s-update" % name, None)
		
		element = doc.createElement("update")
		doc.documentElement.appendChild(element)

		def temp(x):
			try:
				f = open(x, 'r')
				t = base64.b64encode(f.read())
				f.close()
				return t
			except:
				return ""

		values = [
			# optionname category howto dump
			['mainversion', 	'info', 	str],
			['secondversion',	'info', 	str],
			['revision', 		'info', 	str],
			['message', 		'info', 	str],

			['changelog', 		'changelog',	temp],
			
			['database', 		None, 		str],

			['message-pre', 	'info',	str],
			['message-post',	'info',	str],

			['mirrors',		'mirrors',	None,	'url'],

			['actions-pre',		'actions',	None,	'pre'],
			['actions-post',	'actions',	None,	'post'],

			['downloads-svn',	'downloads',	None,	'svn'],
			['downloads-tarball',	'downloads',	None,	'tarball'],
			['downloads-windows',	'downloads',	None,	'windows']

		]

		self.categories = {}

		for option in values:
			if len(option) == 4:
				if not option[1] in self.categories:
					t = self.categories[option[1]] = doc.createElement(option[1])
					element.appendChild(t)
				
				t = self.categories[option[1]]
				
				for i in program.get(option[0]):
					x = doc.createElement(option[3])
					x.appendChild(doc.createTextNode(i))
					t.appendChild(x)
			else:
				if option[1] == None:
					t = doc.createElement(option[0])
					t.appendChild(doc.createTextNode(str(program.get(option[0]))))
					element.appendChild(t)
				else:
					if not option[1] in self.categories:
						t = self.categories[option[1]] = doc.createElement(option[1])
						element.appendChild(t)
					
					t = self.categories[option[1]]
					x = doc.createElement(option[0])
					
					x.appendChild(doc.createTextNode(option[2](program.get(option[0]))))
					t.appendChild(x)
		try:
			f = open("%s-update.xml" % name, "w")
			doc.writexml (f, "", "", "")
			f.close()
			
			print "%s-update.xml written." % name
		except:
			print "Cannot write to %s-update.xml ... ignoring." % name
