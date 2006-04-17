import gtk
import impostazioni

class LangWindow (gtk.Window):
	def __init__ (self):
		gtk.Window.__init__ (self)

		self.set_title (_("PyAcqua - Selezione Lingua"))
		self.set_size_request (400, 200)
		self.set_icon_from_file ("pixmaps/logopyacqua.jpg")
		self.connect ('delete-event', self.exit)

		mbox = gtk.VBox ()
		vbox = gtk.VBox ()

		mbox.set_border_width (4)
		vbox.set_border_width (4)

		self.it = it = gtk.RadioButton (None, _("Italiano"))
		self.en = en = gtk.RadioButton (it, _("Inglese"))

		it_icon = gtk.Image (); en_icon = gtk.Image ()
		it_icon.set_from_file ("pixmaps/it.xpm")
		en_icon.set_from_file ("pixmaps/en.xpm")

		box = gtk.HBox ()
		box.pack_start (it_icon, False, False, 0)
		box.pack_start (it)
		vbox.pack_start (box, False, False, 0)

		box = gtk.HBox ()
		box.pack_start (en_icon, False, False, 0)
		box.pack_start (en)
		vbox.pack_start (box, False, False, 0)

		frm = gtk.Frame (_("Seleziona Lingua:"))
		frm.add (vbox)

		mbox.pack_start (frm)

		bb = gtk.HButtonBox ()
		bb.set_layout (gtk.BUTTONBOX_END)

		btn = gtk.Button (stock=gtk.STOCK_CANCEL)
		btn.connect ('clicked', self.exit)
		bb.pack_start (btn)

		btn = gtk.Button (stock=gtk.STOCK_OK)
		btn.connect ('clicked', self.on_ok)
		bb.pack_start (btn)

		mbox.pack_start (bb, False, False, 0)

		self.add (mbox)

		if impostazioni.lang.lower () == "it":
			it.set_active (True)
		elif impostazioni.lang.lower () == "en":
			en.set_active (True)

		self.show_all ()
	
	def exit (self, *w):
		self.hide ()
	
	def on_ok (self, widget):
		if self.en.get_active ():
			impostazioni.lang = "en"
		elif self.it.get_active ():
			impostazioni.lang = "it"
		else:
			return

		impostazioni.save ()
		self.exit ()
