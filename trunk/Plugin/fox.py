import app
import gtk
import files.utils
import files.dbwindow

class fox(gtk.Window):
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
		
		f1 = gtk.Frame(_('Sonde')); f2 = gtk.Frame(_('Uscite')); f3 = gtk.Frame(_('Alba e Tramonto'))
		
		box.pack_start(f1, False, False, 0)
		box.pack_start(f2, False, False, 0)
		box.pack_start(f3, False, False, 0)
		
		tbl_sonde = gtk.Table(11, 3)
		tbl_sonde.set_border_width(5)
		
		
		tbl_sonde.attach(self.new_label(_('Ph')), 0, 1, 0, 1, yoptions=gtk.SHRINK)
		tbl_sonde.attach(self.new_label(_('Temperatura')), 0, 1, 1, 2, yoptions=gtk.SHRINK)
		
		
		
		
		
		tbl = gtk.Table(11, 3)
		tbl.set_border_width(5)
		
		
		labels = ('1', '2', '3', '4')
		for i in labels:
			widget = gtk.CheckButton(i)
		
		tbl.attach(self.new_label(_('Uscita 1')), 0, 1, 0, 1, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Uscita 2')), 0, 1, 1, 2, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Uscita 3')), 0, 1, 2, 3, yoptions=gtk.SHRINK)
		tbl.attach(self.new_label(_('Uscita 4')), 0, 1, 3, 4, yoptions=gtk.SHRINK)
		
		
		tbl.attach(widget, 1, 2, 0, 1)
		
		
		tbl_alba = gtk.Table(11, 3)
		tbl_alba.set_border_width(5)
		
		tbl_alba.attach(self.new_label(_('Alba')), 0, 1, 0, 1, yoptions=gtk.SHRINK)
		tbl_alba.attach(self.new_label(_('Tramonto')), 0, 1, 1, 2, yoptions=gtk.SHRINK)
		
		#qui pero e da modificare invece che scegliere la data bisogna far scegliere
		# l ora dell alba e del tramonto.
		
		self.alba = files.utils.DataButton ()
		self.tramonto = files.utils.DataButton ()
		
		tbl_alba.attach(self.alba, 1, 2, 0, 1, yoptions=0)
		tbl_alba.attach(self.tramonto, 1, 2, 1, 2, yoptions=0)
		
		
		f1.add(tbl_sonde)
		f2.add(tbl)
		f3.add(tbl_alba)
		
		self.add(box)
		self.show_all ()
			
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
