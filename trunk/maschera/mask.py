import gtk
import sys
from xml.dom.minidom import getDOMImplementation, parse

class Mask (gtk.Window):
	def __init__ (self):
		gtk.Window.__init__ (self)
		self.set_title ("Maschera Pesci")

		self.pvt_dict = {}

		self.tbl = tbl = gtk.Table (5, 2)

		self.nome = self.dummy_attach ("Nome", 0)
		self.family = self.dummy_attach ("Famiglia", 1)
		self.und_family = self.dummy_attach ("SottoFamiglia", 2)

		btn = gtk.Button (stock = gtk.STOCK_SAVE)
		btn.connect ("clicked", self.on_save)
		tbl.attach (btn, 1, 2, 3, 4)

		btn = gtk.Button (stock = gtk.STOCK_OPEN)
		btn.connect ("clicked", self.on_open)
		tbl.attach (btn, 0, 1, 3, 4)

		self.connect ("delete-event", lambda *k: gtk.main_quit ())

		self.edit_file = None

		vbox = gtk.VBox (2, False)
		vbox.pack_start (tbl, False, False, 0)
		self.add (vbox)
		self.show_all ()

	def dummy_attach (self, x, y):
		self.tbl.attach (gtk.Label (x), 0, 1, y, y+1)
		
		widget = gtk.Entry ()
		self.tbl.attach (widget, 1, 2, y, y+1)

		self.pvt_dict [x] = widget

		return widget
	
	def set (self, key, node):
		try:
			print node.attributes["name"].nodeValue
			self.pvt_dict[key].set_text (node.attributes ["name"].nodeValue)
		except:
			print "Some errors here"
			return
	
	def get (self, value):
		"""Ritorna il valore della chiave \(puo' tornare \"\" se nn e' inserito nulla nella entry\)
		Altrimenti ritorna un None in caso di chiave assente
		"""

		try:
			return self.pvt_dict[value].get_text ()
		except:
			return None
	
	def on_save (self, widget):
		# Le chiavi e i valori delle medesime si trovano in self.pvt_dict
		# Usa la self.get () per prendere i valori invece di usare l'indirizzamento diretto
		# tipo se devo prendere il nome del pesce famo:
		#	nome = self.get ("Nome")

		# Qui non so come dovrebbe essere la struttura in generale prendiamo i campi
		# generici. L'annnidamento si vede in seguito.

		if not self.edit_file:
			filter = gtk.FileFilter ()
			filter.add_pattern ("*.xml")
			filter.set_name ("PyAcqua fish (xml based)")
			
			chooser = gtk.FileChooserDialog ("Salva scheda pesce...", self, 
				gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_SAVE, 0, gtk.STOCK_CANCEL, 1))
			chooser.add_filter (filter)
			
			id = chooser.run ()
			chooser.hide ()
			
			file_name = chooser.get_filename ()
			
			chooser.destroy ()
			
			if file_name == None or id == 1:
				return
		else:
			file_name = self.edit_file

		try:
			f = open (file_name, "w+")
		except:
			print "ERRORACCIO"
			return

		name = self.get ("Nome")
		fam  = self.get ("Famiglia")
		ufam = self.get ("SottoFamiglia")

		# NB: Per adesso stampiamo solamente sullo stdout

		doc = getDOMImplementation ().createDocument (None, "pyacqua", None)

		# L'elemento principale e' questo
		fish_el = doc.createElement ("fish")
		fish_el.setAttribute ("name", name) # Settiamo il name <fish name="unz">

		doc.documentElement.appendChild (fish_el) # Appendiamo al documento

		# Creiamo il child Family di fish
		fami_el = doc.createElement ("family")
		fami_el.setAttribute ("name", fam)

		fish_el.appendChild (fami_el) # <fish><family /></fish>
		
		# Child del dell'elemento family che e' child di fish :P
		sub_fam_el = doc.createElement ("subfamily")
		sub_fam_el.setAttribute ("name", ufam)

		fish_el.appendChild (sub_fam_el)

		# Scriviamo sullo stdout..
		# Se vuoi la scrittura su file decommenta sotto e commenta esto :P
		# ... ah .. devi decommentare su pure :P
		# doc.writexml (sys.stdout, '\t', '\t', '\n')

		doc.writexml (f, '\t', '\t', '\n')
		f.close ()
	
	def on_open (self, widget):
		filter = gtk.FileFilter ()
		filter.add_pattern ("*.xml")
		filter.set_name ("PyAcqua fish (xml based)")

		chooser = gtk.FileChooserDialog ("Salva scheda pesce...", self, 
			gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_OPEN, 0, gtk.STOCK_CANCEL, 1))
		chooser.add_filter (filter)

		id = chooser.run ()
		chooser.hide ()

		file_name = chooser.get_filename ()

		chooser.destroy ()

		if file_name == None or id == 1:
			return
		try:
			doc = parse (file_name)
		except:
			print "uhm"
			return
		
		if doc.documentElement.tagName == "pyacqua": # Seems valid
			for node in doc.documentElement.childNodes:
				if node.nodeName == "fish": # e prendi gli attributi
					self.set ("Nome", node)
					for x in node.childNodes:
						if x.nodeName == "family":
							self.set ("Famiglia", x)
						elif x.nodeName == "subfamily":
							self.set ("SottoFamiglia", x)

		self.edit_file = file_name

if __name__ == "__main__":
	Mask ()
	gtk.main ()
