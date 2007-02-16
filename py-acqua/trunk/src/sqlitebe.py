# -*- coding: utf-8 -*-
# Copyright © 2005 Francesco Piccinno (stack.box@gmail.com)
#
# This file is part of PyAcqua.
#
# PyAcqua is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PyAcqua is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyAcqua; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  
# USA

from backend import *
from pysqlite2 import dbapi2 as sqlite

class sqliteBE(BackendFE):
	"""
	An sqlite backend for pyacqua
	"""
	def __init__ (self, filename):
		BackendFE.__init__ (self, filename)
		
		if self.check_database ():
			self.set_schema_presents (True)
		
		#if not self.check_database ():
		#	raise "Error in check_database ()"
		
		self.connection = sqlite.connect (self.filename)
		self.cursor = self.connection.cursor ()
	
	def create_table (self, name, columns, types):
		subreq = ""
		for i in zip (columns, types):
			subreq += "%s %s, " % (i[0], self.get_type (i[1]))
		
		subreq = subreq[:-2]
		
		req = "CREATE TABLE %s (%s)" % (name, subreq)
		
		self.commit_request (req)
	
	def select (self, what, table):
		req = "SELECT %s FROM %s" % (what, table)
		
		self.commit_request (req)
	
	def update (self, table, colums, values):
		subreq = ""
		for i in zip (colums[:-1], values[:-1]):
			if type (i[1]) == int or type (i[1]) == float:
				subreq += "%s=%d, " % (i[0], self.safe_value_convert (i[1]))
			elif type (i[1]) == str:
				subreq += "%s='%s', " % (i[0], self.safe_value_convert (i[1]))
			else:
				raise "Unknown type for SET statement"
		
		subreq = subreq[:-2]
		subreq += " WHERE %s=" % colums[-1:][0]
		
		if type (values[-1:][0]) == int or type (values[-1:][0]) == float:
			subreq += "%d" % values[-1:][0]
		elif type (values[-1:][0]) == str:
			subreq += "'%s'" % self.safe_value_convert (values[-1:][0])
		else:
			raise "Unknown type for WHERE statement"
		req = "UPDATE %s SET %s" % (table, subreq)
		
		self.commit_request (req)
	
	def insert (self, table, values):
		subreq = ""
		for i in values:
			if type (i) == str:
				subreq += "'%s', " % self.safe_value_convert (i)
			elif type (i) == int or type (i) == float:
				subreq += "%d, " % i
		
		subreq = subreq[:-2]
		req = "INSERT INTO %s VALUES (%s)" % (table, subreq)
		
		self.commit_request (req)
	
	def delete (self, table, column, value):
		if type (value) == int or type (value) == float:
			req = "DELETE FROM %s WHERE %s=%d" % (table, column, value)
		elif type (value) == str:
			req = "DELETE FROM %s WHERE %s='%s'" % (table, column, self.safe_value_convert (value))
		else:
			raise "Unknown type for DELETE statement"
		
		self.commit_request (req)
	
	def commit_request (self, req):
		print ">>", req
		self.cursor.execute (req)
		ret = self.cursor.fetchall ()
		
		if ret != []:
			print "sbrah =>", ret
		
		self.connection.commit ()

if __name__ == "__main__":
	# Il risultato dovrebbe essere simile al seguente:
	# stack@dannazione src $ rm ~/database_prova && python sqlitebe.py
	# Initing a backend DB
	# >> CREATE TABLE unz (id INTEGER, nome TEXT, cognome VARCHAR(500))
	# >> INSERT INTO unz VALUES (1, 'pinco', 'pallino')
	# >> SELECT * FROM unz
	# sbrah => [(1, u'pinco', u'pallino')]
	# >> UPDATE unz SET nome='gay' WHERE id=1
	# >> SELECT * FROM unz
	# sbrah => [(1, u'gay', u'pallino')]
	# >> DELETE FROM unz WHERE id=1
	# >> SELECT * FROM unz

	a = sqliteBE ("~/database_prova")
	a.create_table ("unz", ["id", "nome", "cognome"], [ColumnType.INTEGER, ColumnType.TEXT, ColumnType.VARCHAR + 500])
	a.insert ("unz", [1, "pinco", "pallino"])
	a.select ("*", "unz")
	
	a.update ("unz", ["nome", "id"], ["gay", 1])
	a.select ("*", "unz")
	
	a.delete ("unz", "id", 1)
	a.select ("*", "unz")