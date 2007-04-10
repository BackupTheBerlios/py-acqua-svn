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

import gtk
import gobject
import httplib
import threading
import generate
import app
import utils
import os.path
import sys

#REPOSITORY_ADDRESS = "http://pyacqua.altervista.org/"
#BASE_DIR = "/update/source/"
#LIST_FILE = "/update/list.txt"

REPOSITORY_ADDRESS = r"localhost"
BASE_DIR = r"/~stack/update/source/"
LIST_FILE = r"/~stack/update/list.txt"

class Fetcher(threading.Thread):
	def __init__ (self, callback, url):
		self.data = None
		self.callback = callback
		self.url = url
		threading.Thread.__init__ (self, name="Fetcher")

	def run (self):
		try:
			self.response = None; self.data = None
			try:
				conn = httplib.HTTPConnection (REPOSITORY_ADDRESS)
				conn.request ("GET", self.url)
				self.response = conn.getresponse ()
				self.data = self.response.read ()
			except:
				print _("!! Errore mentre scaricavo da %s") % self.url
		finally:
			gobject.idle_add (self._on_data)

	def _on_data (self):
		gtk.gdk.threads_enter ()
		
		try:
			self.callback (self.data, self.response)
		finally:
			gtk.gdk.threads_leave ()
		
		return False

class WebUpdate (gtk.Window):
	def __init__ (self):
		gtk.Window.__init__ (self)

		vbox = gtk.VBox (False, 2)

		self.store = gtk.ListStore (str, str, int, str, int, bool) #il bool finale: to_add?
		self.tree = gtk.TreeView (self.store)

		rend = gtk.CellRendererText (); id = 0
		for i in (_("File"), _("Azione"), _("Bytes"), _("MD5")):
			col = gtk.TreeViewColumn (i, rend, text=id)
			self.tree.append_column (col)
			id += 1

		rend = gtk.CellRendererProgress ()
		col = gtk.TreeViewColumn (_("%"), rend, value=4)
		self.tree.append_column (col)

		sw = gtk.ScrolledWindow ()
		sw.add (self.tree)
		vbox.pack_start (sw)
		
		bb = gtk.HButtonBox ()
		bb.set_layout (gtk.BUTTONBOX_END)
		
		self.update_btn = btn = utils.new_button (_("Aggiorna"), gtk.STOCK_REFRESH)
		btn.connect ('clicked', self._on_start_update)
		bb.pack_start (btn)

		btn.set_sensitive (False)

		self.get_btn = btn = utils.new_button (_("Controlla Aggiornamenti"), gtk.STOCK_APPLY)
		btn.connect ('clicked', self._on_get_list)
		bb.pack_start (btn)
		
		vbox.pack_start (bb, False, False, 0)

		self.status = gtk.Statusbar ()
		vbox.pack_start (self.status, False, False, 0)

		self.add (vbox)
		self.show_all ()
		
		self.connect ('delete-event', self._on_delete_event)
		
		self.file = None
		self.it = None
		self.checklist = []
		
		self.actual_data = generate.Generator.ParseDir (utils.HOME_DIR)

	def _on_get_list (self, widget):
		widget.set_sensitive (False)
		self.store.clear ()
		self._thread (self._populate_tree, LIST_FILE)
	
	def _thread (self, callback, url):
		print _(">> Creo un thread per %s") % url
		f = Fetcher (callback, url)
		f.setDaemon (True)
		f.start ()
	
	def _convert_to_dict(self, data):
		data = data.splitlines()
		dict = {}
		
		for i in data:
			name, bytes, sum = i.split("|")
			dict[name] = bytes + "|" + sum
		
		return dict

	def _populate_tree (self, data, response):
		self.get_btn.set_sensitive (True)

		if data == None:
			self.status.push (0, _("Impossibile recuperare la lista dei file dal server."))
			return

		if response.status != 200:
			self.status.push (0, _("Errore durante lo scaricamento della lista dei file (HTTP %d)") % response.status)
			return

		data = self._convert_to_dict (data)
		
		precheck = len (data) - len (self.actual_data)
		
		if precheck > 0:
			print _(">> Nuovi file aggiunti dall'ultimo update.")
		elif precheck < 0:
			print _(">> Qualche file e' stato zappato dall'ultimo update.")
		
		for i in self.actual_data:
			n_bytes, n_sum = "0", "0"
			o_bytes, o_sum = self.actual_data[i].split("|")
			
			to_add = False
			
			if data.has_key (i):
				n_bytes, n_sum = data[i].split("|")
				
				if n_sum != o_sum:
					print _(">> Il checksum e' differente. Aggiungo il file %s") % i
					to_add = True
				else:
					if n_bytes == o_bytes:
						print _(">> Bene! Tutto questo lavoro per niente!")
					else:
						print _(">> U0z! Collisione di MD5 per il file %s") % i
						print _(">> Comunque il file deve essere aggiunto -_-")
						to_add = True
				data.pop (i)
			else:
				print _(">> Questo file deve essere cancellato %s") % i
				self.store.append ([i, _("Elimina"), int (o_bytes), o_sum, 0, False])
				
			if to_add:
				self.store.append ([i, _("Scarica"), int (n_bytes), n_sum, 0, True])
		
		for i in data:
			n_bytes, n_sum = data[i].split("|")
			print _(">> Questo file deve essere aggiunto %s") % i
			self.store.append ([i, _("Scarica"), int (n_bytes), n_sum, 0, True])
		
		self.update_btn.set_sensitive (True)
	
	def _on_start_update (self, widget):
		self.it = self.tree.get_model ().get_iter_first ()
		self._update_from_iter ()
		
	def _update_file (self, data, response):
		# Dovremmo semplicemente salvare in una directory temporanea
		# del tipo ~/.pyacqua/.update o .update nella directory corrente
		# insieme ad una lista di file|bytes|checksum per il controllo sull'update
		# Al riavvio il programma dovrebbe controllare che in .update ci siano file
		# e aggiornare di conseguenza
		
		# TODO: da finire
		
		if not data:
			print _(">> Nessun file da ricevere")
		if response.status != 200:
			print _("!! Errori. Il sospetto e' %s (response: %d)") % (self.file, response.status)
		
		# Creiamo le subdirectory necessarie
		dirs = self.file.split (os.path.sep); dirs.pop ()
		path = utils.UPDT_DIR
		
		#print "!! Aggiungi check prima della versione finale webupdate.py:164"
		#try:
		for i in dirs:
			path = os.path.join (path, i)
			if not os.path.exists (path):
				os.mkdir (path)
	
		print _(">> File ricevuto %s") % self.file
	
		f = open (os.path.join (utils.UPDT_DIR, self.file), 'w')
		f.write (data)
		f.close ()
		
		self._update_check_list ()
		self._update_percentage ()
		self._go_with_next_iter ()
		#except:
		#	print "Error while updating (%s %s)" % (sys.exc_value, sys.exc_type)
	
	def _update_percentage (self):
		self.tree.get_model ().set_value (self.it, 4, 100)

	def _update_check_list (self):
		bytes = self.tree.get_model ().get_value (self.it, 2)
		sum = self.tree.get_model ().get_value (self.it, 3)
		
		self.checklist.append ("%s|%d|%s" % (self.file, bytes, sum))
		
	def _go_with_next_iter (self):
		self.it = self.tree.get_model ().iter_next (self.it)
		self._update_from_iter ()
		
	def _update_from_iter (self):
		if self.it != None:
			self.file = self.tree.get_model ().get_value (self.it, 0)
			
			if self.tree.get_model ().get_value (self.it, 5):
				self._thread (self._update_file, utils.url_encode (BASE_DIR + self.file))
			else:
				print _(">> Questo file deve essere aggiunto (setto 0 come checksum)")
				self.checklist.append ("%s|0|0" % self.file)
				self._update_percentage ()
				self._go_with_next_iter ()
		else:
			# Probabilmente abbiamo finito.. controlliamo la checklist e via
			if len (self.checklist) > 0:
					print "!! Aggiungi check prima della versione finale webupdate.py:199"
				#try:
					f = open (os.path.join (utils.UPDT_DIR, ".checklist"), "w")
					for i in self.checklist:
						f.write (i + "\n")
					f.close ()

					utils.info (_("Riavvia per procedere all'aggiornamento di PyAcqua"))
				#except:
				#	print "Error while writing the checklist"
		
	def _on_delete_event (self, *w):
		app.App.p_window["update"] = None
