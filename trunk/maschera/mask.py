import gtk
import sys
from xml.dom.minidom import getDOMImplementation

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

		# delete event da collegare
		# qui!

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

		name = self.get ("Nome")
		fam  = self.get ("Famiglia")
		ufam = self.get ("SottoFamiglia")

		# Dopo aver preso i vari campi apriamo un file e scriviamoci su

		# Per la scelta del nome del file di output serve na FileChooser.
		#
		# f = open ("file_out", "w")

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
		doc.writexml (sys.stdout, '\t', '\t', '\n')

		# doc.writexml (f, '\t', '\t', '\n')
		# f = close ()

	
	def on_open (self, widget):
		# NB: qui ce vole na FileChooser per l'apertura..
		# Per il caricamento dei file xml puoi vedere impostazioni.py
		
		# In linea di massima se fa cosi'
		# doc = parse ("/home/stack/file.xml")
		# if doc.documentElement.tagName == "pyacqua": # Seems valid
		# for node in doc.documentElement.childNodes:
		#	if node.nodeName == "fish": # e prendi gli attributi
		#		node.nodeName.attributes ["name"].nodeValue # ecc

		pass

if __name__ == "__main__":
	Mask ()
	gtk.main ()
