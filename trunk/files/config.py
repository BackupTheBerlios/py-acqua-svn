import pygtk
pygtk.require('2.0')
import gtk, os, pango, sys

class Config(gtk.Window):	
	def __init__(self):
		gtk.Window.__init__(self)
		
		self.path = os.getcwd()+'/files/'
			
		self.set_title("config.cfg")
		self.set_size_request(400, 600)
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		self.connect("destroy", self.exit_save)
		
		self.bar = gtk.Statusbar()
		self.bar.push(0, '')
		
		vbox = gtk.VBox()
		
		##Bottoni
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_START)
		bb.set_spacing(5)
		
		btn = gtk.Button(stock=gtk.STOCK_SAVE)
		btn.connect('clicked', self.save)
		bb.pack_start(btn)
		
		vbox.pack_start(bb, False, False, 2)
		
		self.textview = gtk.TextView()
		self.textview.set_wrap_mode(gtk.WRAP_WORD)
		self.textbuffer = self.textview.get_buffer()
		
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
	
		sw.add(self.textview)
		
		vbox.pack_start(sw)
		vbox.pack_end(self.bar, False, False, 0)
		
		testo = open(os.path.join(self.path, 'config.cfg'), 'r').read()
		self.textbuffer.set_text(testo)
		
		self.add(vbox)
		self.show_all()
		
	def save(self, widget):
		start, end = self.textbuffer.get_bounds()
		text = self.textbuffer.get_text(start, end)
		try:
			os.rename(os.path.join(self.path, 'config.cfg'), os.path.join(self.path, 'config.cfg~'))
			testo = open(os.path.join(self.path, 'config.cfg'), 'w').write(text)
			self.set_title("config.cfg (Salvato)")
			self.bar.push(1, 'File salvato')
		except:
			self.bar.push(1, 'Errore durante il salvataggio del file: %s') % sys.exc_value()
			
	def exit_save(self, widget):
		pass
