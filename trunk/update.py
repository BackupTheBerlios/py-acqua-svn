import pysvn
import os
import pygtk
import sys
pygtk.require('2.0')
import gtk

class Update(gtk.Window):	
	def __init__(self):
		gtk.Window.__init__(self)
		self.set_title(_("Update"))
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		self.set_resizable(False)
		self.set_size_request(350, 500)
		
		vbox = gtk.VBox()
		
		self.textview = gtk.TextView()
		self.textview.set_wrap_mode(gtk.WRAP_WORD) ###
		self.textbuffer = self.textview.get_buffer()
		
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN) ###
		sw.add(self.textview)
		
		self.bar = gtk.Statusbar()
		
		vbox.pack_start(sw)
		vbox.pack_start(self.bar, False, False, 0)
		
		
		self.add(vbox)
		self.show_all()
		
		#Funzioni e variabili varie
		set_up = "Avvio update py-Acqua in corso..."
		self.set_svn = "Controllo la presenza di .svn... %s"
		self.errore = "Errore durante l'update: %s"
		self.textbuffer.set_text(set_up)
		self.on_update()

	def on_update(self):
		
		client = pysvn.Client()
		cwdir = os.getcwd()
		svn = 'http://svn.berlios.de/svnroot/repos/py-acqua/trunk/'
		for dir in os.listdir(cwdir):
			if dir == ".svn":
				try:
					self.textbuffer.set_text(self.set_svn % "Ok")
					client.update(cwdir)
				except:
					self.textbuffer.set_text(self.errore % sys.exc_value)
			else:
				try:
					self.textbuffer.set_text(self.set_svn % "No")
					client.checkout(svn, cwdir)
				except:					
					self.textbuffer.set_text(self.errore % sys.exc_value)
