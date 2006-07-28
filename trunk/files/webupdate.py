import gtk
import gobject
import httplib
import threading
import generate
import utils

class Fetcher(threading.Thread):
	def __init__ (self, callback, url):
		self.data = None
		self.callback = callback
		self.url = url
		threading.Thread.__init__ (self, name="Fetcher")

	def run (self):
		try:
			conn = httplib.HTTPConnection ("intifada.altervista.org")
			conn.request ("GET", self.url)
			self.data = conn.getresponse ().read ()
		finally:
			gobject.idle_add (self.on_data)

	def on_data (self):
		gtk.gdk.threads_enter ()
		
		try:
			self.callback (self.data)
		finally:
			gtk.gdk.threads_leave ()
		
		return False

class WebUpdate (gtk.Window):
	def __init__ (self):
		gtk.Window.__init__ (self)

		vbox = gtk.VBox (False, 2)

		self.store = gtk.ListStore (str, str, int, str, int)
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
		
		self.button = btn = utils.new_button (_("Aggiorna"), gtk.STOCK_REFRESH)
		btn.connect ('clicked', self.on_start_update)
		bb.pack_start (btn)
		
		btn.set_sensitive (False)
		
		vbox.pack_start (bb, False, False, 0)

		self.status = gtk.Statusbar ()
		vbox.pack_start (self.status, False, False, 0)

		self.add (vbox)
		self.show_all ()
		
		self.connect ('delete-event', self.exit)
		
		self.file = None
		self.it = None
		
		self.actual_data = generate.Generator.ParseDir (".")
		self.thread (self.populate_tree, "/update/list.txt")
	
	def thread (self, callback, url):
		f = Fetcher (callback, url)
		f.setDaemon (True)
		f.start ()
	
	def convert_to_dict(self, data):
		data = data.splitlines()
		dict = {}
		
		for i in data:
			name, bytes, sum = i.split("|")
			dict[name] = bytes + "|" + sum
		
		return dict

	def populate_tree (self, data):
		if data == None: return

		data = self.convert_to_dict (data)
		
		precheck = len (data) - len (self.actual_data)
		
		if precheck > 0:
			print "New Files added since last update"
		elif precheck < 0:
			print "Some Files zapped since last update"
		
		for i in self.actual_data:
			n_bytes, n_sum = "0", "0"
			o_bytes, o_sum = self.actual_data[i].split("|")
			
			to_add = False
			
			if data.has_key (i):
				n_bytes, n_sum = data[i].split("|")
				
				if n_sum != o_sum:
					print "unz", i
					to_add = True
				else:
					if n_bytes == o_bytes:
						print "Ohh great! -.- a lot of work for nothing!"
					else:
						print "Cool! MD5 collision detected for file", i
						print "However this file must be added -_-"
						to_add = True
				data.pop (i)
			else:
				print "uhm.. This file must be deleted... mumble mumble"
				self.store.append ([i, _("Elimina"), int (o_bytes), o_sum, 0])
				
			if to_add:
				self.store.append ([i, _("Scarica"), int (n_bytes), n_sum, 0])
		
		for i in data:
			n_bytes, n_sum = data[i].split("|")
			print "This file is recomended -.- so must be added by default", i
			self.store.append ([i, _("Scarica"), int (n_bytes), n_sum, 0])
		
		self.button.set_sensitive (True)
	
	def on_start_update (self, widget):
		self.it = self.tree.get_model ().get_iter_first ()
		self.update_from_iter ()
		
	def update_file (self, data):
		# Dovremmo semplicemente salvare in una directory temporanea
		# del tipo ~/.pyacqua/.update o .update nella directory corrente
		# insieme ad una lista di file|bytes|checksum per il controllo sull'update
		# Al riavvio il programma dovrebbe controllare che in .update ci siano file
		# e aggiornare di conseguenza
		
		# TODO: da finire
		
		print "File received", self.file
		print data
		
		self.go_with_next_iter ()
	
	def go_with_next_iter (self):
		self.it = self.tree.get_model ().iter_next (self.it)
		self.update_from_iter ()
		
	def update_from_iter (self):
		if self.it != None:
			self.file = self.tree.get_model ().get_value (self.it, 0)
			self.thread (self.update_file, "/souce/" + self.file)
		
	def exit (self, *w):
		self.hide ()
