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

#REPOSITORY_ADDRESS = "http://www.pyacqua.net"
#BASE_DIR = "/update/source/"
#LIST_FILE = "/update/list.xml"

REPOSITORY_ADDRESS = r"localhost"
BASE_DIR = r"/~stack/update/source/"
LIST_FILE = r"/~stack/update/list.xml"

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

		self.store = gtk.ListStore (
			gtk.gdk.Pixbuf, # icona
			str, # nome file
			int, # new_revision
			int, # bytes
			str, # md5
			int, # old_revision
			int, # old bytes
			str, # old_md5
			int, # percentuale scaricamento
			bool) #il bool finale: to_add?
		
		self.tree = gtk.TreeView (self.store)
		
		self.tree.append_column (gtk.TreeViewColumn ("", gtk.CellRendererPixbuf(), pixbuf=0))

		rend = gtk.CellRendererText (); id = 1
		for i in (_("File"), _("Rev"), _("Bytes"), _("MD5"), _("oldRev"), _("oldBytes"), _("oldMD5")):
			col = gtk.TreeViewColumn (i, rend, text=id)
			self.tree.append_column (col)
			id += 1

		rend = gtk.CellRendererProgress ()
		col = gtk.TreeViewColumn (_("%"), rend, value=8)
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
		self.xml_util = generate.UpdateXML ()
		
		self.icon_add = gtk.gdk.pixbuf_new_from_file (os.path.join (utils.DPIXM_DIR, "add.png"))
		self.icon_del = gtk.gdk.pixbuf_new_from_file (os.path.join (utils.DPIXM_DIR, "del.png"))

	def _on_get_list (self, widget):
		widget.set_sensitive (False)
		self.store.clear ()
		self._thread (self._populate_tree, LIST_FILE)
	
	def _thread (self, callback, url):
		print _(">> Creo un thread per %s") % url
		f = Fetcher (callback, url)
		f.setDaemon (True)
		f.start ()

	def _populate_tree (self, data, response):
		self.get_btn.set_sensitive (True)

		if data == None:
			self.status.push (0, _("Impossibile recuperare la lista dei file dal server."))
			return

		if response.status != 200:
			self.status.push (0, _("Errore durante lo scaricamento della lista dei file (HTTP %d)") % response.status)
			return

		#data = self._convert_to_dict (data)
		new_dict_object = self.xml_util.create_dict_from_string (data)
		current_dict_object = self.xml_util.create_dict_from_file ("/home/stack/py-acqua/py-acqua/trunk/list.xml") # FIXME: Fixami
		
		diff_object = self.xml_util.make_diff (new_dict_object, current_dict_object)
		
		for root in diff_object:
			for node in diff_object[root]:
				tmp = diff_object[root][node]
				
				if node == ".": continue
				if root[0:2] == "$$" and root[-2:] == "$$":
					
					self.store.append ([self.icon_add, os.path.join (root[2:-2], node),
						0, 0, "0",
						tmp[0], int (tmp[1]), tmp[2], 0, True])
				else:
					self.store.append ([self.icon_del, os.path.join (root, node),
						tmp[0], int (tmp[1]), tmp[2],
						tmp[3], int (tmp[4]), tmp[5], 0, False])
		
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
