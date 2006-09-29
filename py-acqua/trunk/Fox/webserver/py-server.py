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
import cgi
import BaseHTTPServer
import CGIHTTPServer
import Cookie
from SimpleHTTPServer import SimpleHTTPRequestHandler

class CustomHandler(BaseHTTPServer.BaseHTTPRequestHandler, CGIHTTPServer.CGIHTTPRequestHandler): 
	def do_GET(self):
	
		
		self.handle_data()
		
		
	def handle_data(self):
		self.resp_headers = {"Content-type":'text/html'} 
		self.cookie=Cookie.SimpleCookie()
		if self.headers.has_key('cookie'):
			self.cookie=Cookie.SimpleCookie(self.headers.getheader("cookie"))
		
		path = self.get_file() 
		if os.path.isdir(path):
		
			pass
			
			
		
		else:
		
			ctype = self.guess_type(path)
			if ctype.startswith('text/'):
				mode = 'r'
			else:
				mode = 'rb'
			try:
				f = open(path,mode)
				self.resp_headers['Content-type'] = ctype
				self.resp_headers['Content-length'] = str(os.fstat(f.fileno())[6])
				self.done(200,f)
			except IOError:
				self.send_error(404, "File not found")
	def get_file(self):
		path = self.path
		print path
		if path.find('?')>1:
		
			path = path.split('?',1)[0]
		path = self.translate_path(path)
		print path
		if os.path.isdir(path):
			for index in "index.html", "index.htm":
				index = os.path.join(path, index)
				print index
				if os.path.exists(index):
					path = index
					break
		return path	
		
	def done(self, code, infile):

		self.send_response(code)
		for morsel in self.cookie.values():
			self.send_header('Set-Cookie', morsel.output(header='').lstrip())
		for (k,v) in self.resp_headers.items():
			self.send_header(k,v)
		self.end_headers()
		infile.seek(0)
		self.copyfile(infile, self.wfile)


### qua la docroot poi bisogna settarla per Fox
docroot="/usr/home/luca/Documenti/Programmi/py-acqua/svn/trunk/Fox/webserver/html"
os.chdir(docroot)
port = 8000
server = BaseHTTPServer.HTTPServer(('', port), SimpleHTTPRequestHandler)# fare il bind sulla 88 da problemi se nn sei r00t :P
print "ScriptServer running on port %s" %port
server.serve_forever()
