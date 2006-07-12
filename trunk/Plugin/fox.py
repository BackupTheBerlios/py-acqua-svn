import app
import gtk
import files.utils
import files.dbwindow

class fox:
	__name__ = "Fox"
	__desc__ = "Plugin per fox"
	__ver__ = "0.0.1"
	__author__ = "PyAcqua team"

	def start (self):
		print ">> Starting", self.__name__
		
		menu = app.App.get_plugin_menu ()

		self.item = gtk.MenuItem ("Fox Plugin")
		self.item.connect ('activate', self.on_activated)
		self.item.show ()

		menu.append (self.item)

	def stop (self):
		print "** Stopping", self.__name__

		self.item.hide ()
		self.item.destroy ()
	
	def on_activated(self, widget):
		print "clicked"
		
		
		box = gtk.VBox()
		box.set_spacing(4)
		box.set_border_width(4)
		
		tbl = gtk.Table(11, 3)
		tbl.set_border_width(5)
		
		tbl.attach(self.new_label(_('Sonde')), 1, 2, 0, 1, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Ph')), 2, 3, 0, 1, yoptions=gtk.SHRINK)
		
		box.pack_start(tbl)
		
		
		
		##### da finire perche da errori
		add (box)
		show_all ()
			
	def new_label(self, txt, bold=True):
		lbl = gtk.Label()
		if bold:
			lbl.set_use_markup(True)
			lbl.set_label('<b>' + txt + '</b>')
			lbl.set_alignment(0, 0.5)
		else:
			lbl.set_label(txt)
			lbl.set_alignment(0.5, 0.5)
		
		return lbl
		
	def exit(self, *w):
		self.hide()
