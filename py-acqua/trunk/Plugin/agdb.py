import app
import gtk
import impostazioni

class dummy:
	__name__ = "AgDB"
	__desc__ = "Aggiornamento database"
	__ver__ = "0.0.1"
	__author__ = "PyAcqua team"
	__preferences__ = {
		'dummy_nervose_mode' : False
	}

	def start (self):
		print ">> Starting", self.__name__
		
		print ">> AgDB.. showtips :", impostazioni.get("show_tips")
		
		if impostazioni.get("dummy_nervose_mode"):
			print prova
		
		menu = app.App.get_plugin_menu ()

		self.item = gtk.MenuItem ("AgDB Plugin")
		self.item.connect ('activate', self.on_activated)
		self.item.show ()

		menu.append (self.item)

	def stop (self):
		print "** Stopping", self.__name__

		self.item.hide ()
		self.item.destroy ()
	
	def on_activated(self, widget):
		print "clicked"
