import gtk

class DataButton(gtk.Button):
	def __init__(self, label=None):
		gtk.Button.__init__(self, label)
		self.set_relief(gtk.RELIEF_NONE)
		self.connect('clicked', self.on_change_date)
		self.cal = gtk.Calendar()
		
		if label == None:
			self.update_label(self.cal.get_date())
			
	def update_label(self, date):
		self.set_label("%02d/%02d/%04d" % (date[2], date[1]+1, date[0]))
	
	def on_change_date(self, widget):
		d = gtk.Dialog("Seleziona una data", None, gtk.DIALOG_MODAL,
		(gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
		d.vbox.pack_start(self.cal, False, False, 0)
		d.vbox.show_all()
		self.callback(d)
	
	def get_date(self):
		return self.cal.get_date()
	
	def get_text(self):
		date = self.cal.get_date()
		return "%02d/%02d/%02d" % (date[2], date[1]+1, date[0])
	def set_text(self, date):
		# Per adesso aggiustiamo solo la label senza controlli
		self.set_label(date)
	
	def callback(self, diag):
		id = diag.run()
		if id == gtk.RESPONSE_OK:
			self.update_label(self.get_date())
		diag.hide()
		diag.destroy()

class FloatEntry(gtk.SpinButton):
	def __init__(self, min=0, max=99, inc=0.1, page=1):
		gtk.SpinButton.__init__(self, digits=2)
		self.set_range(min, max)
		self.set_increments(inc, page)
		self.set_wrap(True)
	
	def set_text(self, value):
		try:
			value = float(value)
		except:
			value = 0

		self.set_value(value)
	
	def get_text(self):
		return self.get_value()

class IntEntry(FloatEntry):
	def set_text(self, value):
		try:
			value = int(value)
		except:
			value = 0
		self.set_value(value)
	
	def get_text(self):
		return self.get_value_as_int()
class Combo(gtk.ComboBox):
	def __init__(self):
		liststore = gtk.ListStore(str)
		gtk.ComboBox.__init__(self, liststore)
		
		cell = gtk.CellRendererText()
		self.pack_start(cell, True)
		self.add_attribute(cell, 'text', 0)
		
	def get_text(self):
		it = self.get_active_iter()
		mod = self.get_model()

		return str(mod.get_value(it, 0))
	def set_text(self, txt):
		mod = self.get_model()
		it = mod.get_iter_first()

		while it != None:
			if str(mod.get_value(it, 0)) == txt:
				self.set_active_iter(it)
				return
			it = mod.iter_next(it)
		
class Test:
	def __init__(self, i):
		w = gtk.Window()
		w.set_title("Testing")
		
		if i == 0:
			self.e = e = FloatEntry()
		else:
			self.e = e = IntEntry()
		box = gtk.VBox()
		box.pack_start(e)
		btn = gtk.Button('a')
		btn.connect('clicked', self.a)
		box.pack_start(btn)
		w.add(box)
		w.show_all()
	def a(self, w):
		print self.e.get_text()
		
if __name__ == "__main__":
	Test(0)
	Test(1)
	gtk.main()
