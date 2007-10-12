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

class ListCreator(object):
	def __init__(self, program, database, info, output):
		self.db = DatabaseWrapper(database)

		self.info = info
		self.output = output
		self.program = program

		self.options = {
			'%s.uselast'           % self.program : True,
			'%s.mainversion'       % self.program : 0,
			'%s.secondversion'     % self.program : 0,
			'%s.revision'          % self.program : 0,
			'%s.changelog'         % self.program : '',
			'%s.database'          % self.program : '',
			'%s.message'           % self.program : '',

			'%s.message-pre'       % self.program : '',
			'%s.message-post'      % self.program : '',

			'%s.mirrors'           % self.program : [],

			'%s.downloads-windows' % self.program : [],
			'%s.downloads-tarball' % self.program : [],
			'%s.downloads-svn'     % self.program : [],

			'%s.actions-pre'       % self.program : [],
			'%s.actions-post'      % self.program : [],

		}

		self.readInfoFile()

		if self.options['%s.uselast' % self.program]:
			self.readVersionFromDatabase()
	
	def readVersionFromDatabase(self):
		try:
			self.options['%s.mainversion' % self.program], self.options['%s.secondversion' % self.program], self.options['%s.revision' % self.program] = map(
				int, self.db.select("SELECT mainversion, version, revision FROM program WHERE name=\"%s\"" % self.db.sanitize(self.program))[0]
			)
		except:
			print "Cannot get the versions for program %s." % self.program
			sys.exit(-1)
	
	def readInfoFile(self):
		parser = ConfigParser.ConfigParser()
		parser.read(self.info)

		for sec in parser.sections():
			for opt in parser.options(sec):
				self.handleOption(sec.lower(), opt.lower(), parser.get(sec, opt))
	
	def handleOption(self, sec, opt, value):
		if sec in self.options:
			# Mirrors or lists to handle

			# TODO: evalutate numbers

			check = lambda x, y: x[:len(y)] == y and ((len(x[len(y):]) > 0 and x[len(y):].isdigit()) or (len(x[len(y):]) == 0))

			if check(opt, "mirror"):
				self.options["%s.mirrors" % self.program].append(value)

			elif check(opt, "svn"):
				self.options["%s.downloads-svn" % self.program].append(value)
			elif check(opt, "tarball"):
				self.options["%s.downloads-tarball" % self.program].append(value)
			elif check(opt, "windows"):
				self.options["%s.downloads-windows" % self.program].append(value)

			elif check(opt, "pre"):
				self.options["%s.actions-pre" % self.program].append(value)
			elif check(opt, "post"):
				self.options["%s.actions-post" % self.program].append(value)
		else:
			# type checking

			full = ".".join((sec, opt))
			
			if full not in self.options:
				print "%s not used." % full
				return

			converter = type(self.options[full])
			
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
					self.options[full] = converter(value)
			except:
				print "Type error detected:"
				print "%s must be of %s not %s" % (full, (converter == strict_bool) and (bool) or (converter), type(value))
				
				sys.exit(-1)
	
	def create(self):
		doc = getDOMImplementation().createDocument(None, "%s-update" % self.program, None)
		
		element = doc.createElement("update")
		doc.documentElement.appendChild(element)

		def temp(x):
			f = open(x, 'r')
			t = base64.b64encode(f.read())
			f.close()
			return t

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
				
				for i in self.options["%s.%s" % (self.program, option[0])]:
					x = doc.createElement(option[3])
					x.appendChild(doc.createTextNode(i))
					t.appendChild(x)
			else:
				if option[1] == None:
					t = doc.createElement(option[0])
					t.appendChild(doc.createTextNode(str(self.options["%s.%s" % (self.program, option[0])])))
					element.appendChild(t)
				else:
					if not option[1] in self.categories:
						t = self.categories[option[1]] = doc.createElement(option[1])
						element.appendChild(t)
					
					t = self.categories[option[1]]
					x = doc.createElement(option[0])
					
					x.appendChild(doc.createTextNode(option[2](self.options["%s.%s" % (self.program, option[0])])))
					t.appendChild(x)

		doc.writexml (sys.stdout, "", "", "")
