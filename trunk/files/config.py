import pygtk
pygtk.require('2.0')
import gtk, os, pango, sys, re

class Config(gtk.Window):	
	def __init__(self):
		gtk.Window.__init__(self)
		
		##Variabili
		self.path = os.getcwd()+'/files/'
		self.control_save = ''
		
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
		
		self.tag = gtk.TextTag("color_defualt")
		self.tag.set_property("weight", pango.WEIGHT_BOLD)
				
		table = self.textbuffer.get_tag_table()
		table.add(self.tag)
		
		self.textbuffer.set_modified(0)
		
		iter = self.textbuffer.get_iter_at_line(0)
		iter2 = self.textbuffer.get_iter_at_line(1)
		iter3 = self.textbuffer.get_iter_at_line(4)
		iter4 = self.textbuffer.get_iter_at_line(5)

		self.textbuffer.apply_tag_by_name('color_defualt', iter, iter2)
		self.textbuffer.apply_tag_by_name('color_defualt', iter3, iter4)
		
		self.regex()		
		self.add(vbox)
		self.show_all()
		
	def save(self, widget):
		start, end = self.textbuffer.get_bounds()
		text = self.textbuffer.get_text(start, end)
		try:
			os.rename(os.path.join(self.path, 'config.cfg'), os.path.join(self.path, 'config.cfg~'))
			testo = open(os.path.join(self.path, 'config.cfg'), 'w').write(text)
			self.bar.push(1, 'File salvato')
			self.set_title("config.cfg")
			self.control_save = True
		except:
			self.bar.push(1, 'Errore durante il salvataggio del file: %s') % sys.exc_value()
			
	def exit_save(self, widget, data=None):
		if self.control_save != True:
			if self.textbuffer.get_modified() == 1:
				msg = gtk.MessageDialog(self, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, "Salvare le modifiche prima di uscire?")
				msg1 = msg.run()
				msg.destroy()
				if msg1 == gtk.RESPONSE_YES:
					self.save(widget)
	
	def regex(self):
		regex = '\[.*\]'
		start, end = self.textbuffer.get_bounds()
		text = self.textbuffer.get_text(start, end)
		p = re.compile('\[.*\]')
		iterator = p.finditer(text)
		for iter in iterator:
			 iter_start = self.textbuffer.get_iter_at_line(iter.start())
			 iter_end = self.textbuffer.get_iter_at_line(iter.end())
			 self.textbuffer.apply_tag_by_name('color_defualt', iter_start, iter_end)
			 print iter.start() 
			 print iter.end()
