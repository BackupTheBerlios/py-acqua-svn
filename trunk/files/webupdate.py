import gtk
import gobject
import httplib
import threading
import generate

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

		self.callback (self.data)
		
		gtk.gdk.threads_leave ()
		
		return False

class WebUpdate (gtk.Window):
	def __init__ (self):
		gtk.Window.__init__ (self)

		vbox = gtk.VBox (False, 2)

		self.store = gtk.ListStore (str, str, str, int)
		self.tree = gtk.TreeView (self.store)

		rend = gtk.CellRendererText (); id = 0
		for i in (_("File"), _("Bytes"), _("MD5")):
			col = gtk.TreeViewColumn (i, rend, text=id)
			self.tree.append_column (col)
			id += 1

		rend = gtk.CellRendererProgress ()
		col = gtk.TreeViewColumn (_("%"), rend, value=3)
		self.tree.append_column (col)

		sw = gtk.ScrolledWindow ()
		sw.add (self.tree)
		vbox.pack_start (sw)

		self.status = gtk.Statusbar ()
		vbox.pack_start (self.status, False, False, 0)

		self.add (vbox)
		self.show_all ()
		
		self.connect ('delete-event', self.exit)

		self.actual_data = generate.Generator.ParseDir (".")
		self.thread (self.populate_tree, "/update/list.txt")
	
	def thread (self, callback, url):
		f = Fetcher (callback, url)
		f.setDaemon (True)
		f.start ()

	def populate_tree (self, data):
		if data == None: return

		data = data.splitlines ()

		for i in zip (data, self.actual_data):
			if i[0] == i[1]:
				print "Same", i[0]
			else:
				temp = i[0].split ('|')
				self.store.append([temp[0], int (temp[1]), temp[2], 0])

	def exit (self, *w):
		self.hide ()
