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
	def __init__(self, min=0, max=99):
		gtk.SpinButton.__init__(self)
if __name__ == "__main__":
	w = gtk.Window()
	w.set_title("Testing")
	w.add(DataButton("Prova"))
	w.show_all()
	gtk.main()
