import app
import gtk
import files.utils as utils

class fox(gtk.Window):
	__name__ = "Fox"
	__desc__ = "Plugin per fox"
	__ver__ = "0.0.1"
	__author__ = "PyAcqua team"

	def __init__(self):
		gtk.Window.__init__ (self)
		self.create_gui ()

	def start (self):
		print ">> Starting", self.__name__
		
		menu = app.App.get_plugin_menu ()

		self.item = gtk.MenuItem ("Fox Plugin")
		self.item.connect ('activate', self.on_activated)
		self.item.show ()

		menu.append (self.item)
	
	def create_gui (self):
		# Qui viene costruita la gui

		box = gtk.VBox()
		box.set_spacing(4)
		box.set_border_width(4)
		
		f1 = gtk.Frame(_('Sonde')); f2 = gtk.Frame(_('Uscite')); f3 = gtk.Frame(_('Alba e Tramonto'))

		box.pack_start (f1, False, False, 0)
		box.pack_start (f2, False, False, 0)
		box.pack_start (f3, False, False, 0)
		
		fbox = gtk.VBox ()
		f1_checks = list ()

		for i in (_("pH1"), _("pH2"), _("Temperatura"), _("Redox")):
			tmp = gtk.CheckButton (i)
			f1_checks.append (tmp)
			fbox.pack_start (tmp, False, False, 0)


		f1.add (fbox)

		# Aggiungi il resto
		
		tbl = gtk.Table(4, 2)
		tbl.set_border_width(5)
		
		x = 0; labels = ('1', '2', '3', '4'); f2_checks = list ()
		for i in labels:
			widget = gtk.CheckButton(_("Uscita ") + i)
			f2_checks.append (widget)
			tbl.attach (widget, 0, 1, x, x+1, yoptions=gtk.SHRINK); x += 1
		
		self.uscita1 = utils.Combo ()
		self.uscita1.append_text(_("Filtro"))
		self.uscita1.append_text(_("Co2"))
		self.uscita1.append_text(_("Neon 1"))
		self.uscita1.append_text(_("Neon 2"))
		self.uscita1.append_text(_("Neon 3"))
		self.uscita1.append_text(_("Neon 4"))
		
		

		self.uscita2 = utils.Combo ()
		
		tbl.attach(self.uscita1, 1, 2, 0, 1, yoptions=0)
		tbl.attach(self.uscita2, 1, 2, 1, 2, yoptions=0)
		
		
		tbl_alba = gtk.Table(2, 2)
		tbl_alba.set_border_width(5)
		
		tbl_alba.attach(utils.new_label(_('Alba')), 0, 1, 0, 1, yoptions=gtk.SHRINK)
		tbl_alba.attach(utils.new_label(_('Tramonto')), 0, 1, 1, 2, yoptions=gtk.SHRINK)
		
		#qui e da modificare! invece che scegliere la data bisogna far scegliere
		# l ora dell alba e del tramonto.
		
		self.alba = utils.DataButton ()
		self.tramonto = utils.DataButton ()
		
		tbl_alba.attach(self.alba, 1, 2, 0, 1, yoptions=0)
		tbl_alba.attach(self.tramonto, 1, 2, 1, 2, yoptions=0)
		
		f2.add(tbl)
		f3.add(tbl_alba)
		
		self.add(box)
		self.connect ('delete_event', self.exit)

	def stop (self):
		print "** Stopping", self.__name__

		self.item.hide ()
		self.item.destroy ()
	
	def on_activated(self, widget):
		self.show_all()
		
	def exit(self, *w):
		self.hide()
		return True # Per non distruggere il contenuto
