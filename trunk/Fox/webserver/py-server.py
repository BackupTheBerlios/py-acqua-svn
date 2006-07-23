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
import BaseHTTPServer
import CGIHTTPServer



class BaseHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler, CGIHTTPServer.CGIHTTPRequestHandler): 
	def do_GET(self):
		
		#html
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		html = open("html/index.html")
		self.wfile.write(html.read())
		#cgi
		self.cgi_directories = ["html/cgi-bin"]
		
		
		


server = BaseHTTPServer.HTTPServer(('', 88), BaseHTTPRequestHandler)# fare il bind sulla 80 da problemi se nn sei r00t :P
server.serve_forever()
