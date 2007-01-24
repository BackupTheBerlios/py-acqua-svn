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

class sqliteBE(BackendFE):
	"""
	An sqlite backend for pyacqua
	"""
	def __init__ (self, filename):
		BackendFE.__init__ (self, filename)
	
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
		
	def commit_request (self, req):
		print req

if __name__ == "__main__":
	a = sqliteBE ("/home/stack/unz")
	a.create_table ("unz", ["nome", "cognome"], [ColumnType.TEXT, ColumnType.VARCHAR + 500])
	a.select ("*", "unz")