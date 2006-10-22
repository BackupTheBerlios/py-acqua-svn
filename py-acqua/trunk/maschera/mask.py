import gtk
import sys
from xml.dom.minidom import getDOMImplementation, parse

class FileEntry (gtk.HBox):
	def __init__ (self):
		gtk.HBox.__init__ (self)

		self.entry = gtk.Entry ()
		self.entry.set_property ('editable', False)

		self.btn = gtk.Button (stock=gtk.STOCK_OPEN)
		self.btn.set_relief (gtk.RELIEF_NONE)
		self.btn.connect ('clicked', self.callback)

		self.pack_start (self.entry)
		self.pack_start (self.btn, False, False, 0)
	def set_text (self, value):
		self.entry.set_text(value)
	
	def get_text (self):
		return self.entry.get_text()
	
	def callback (self, widget):
		pass


class ImgEntry (FileEntry):
	def __init__ (self):
		FileEntry.__init__ (self)
	
	def callback (self, widget):
		ret = FileChooser ("Selezione Immagine", None).run ()

		if ret != None:
			self.set_text(copy_image(ret))


class FileChooser(gtk.FileChooserDialog):
	def __init__(self, text, parent, filter=None, for_images=True, act=gtk.FILE_CHOOSER_ACTION_OPEN):
		gtk.FileChooserDialog.__init__(
			self,
			text,
			parent,
			act,
			buttons=(gtk.STOCK_OK, gtk.RESPONSE_OK,
			gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
		
		if for_images:
			self.set_use_preview_label(False)
			
			img = gtk.Image()
			
			self.set_preview_widget(img)
			
			self.connect('update-preview', self.on_update_preview)
		
		#self.set_size_request(128, -1)

		# Creiamo i filtri
		
		if filter == None:
			filter = gtk.FileFilter()
			filter.set_name(_("Immagini"))
			filter.add_mime_type("image/png")
			filter.add_mime_type("image/jpeg")
			filter.add_mime_type("image/gif")
			filter.add_pattern("*.png")
			filter.add_pattern("*.jpg")
			filter.add_pattern("*.gif")
			self.add_filter(filter)
		else:
			self.add_filter(filter)
	
	def run(self):
		id = gtk.Dialog.run(self)

		self.hide()

		if id == gtk.RESPONSE_OK:
			ret = self.get_filename()
		else:
			ret = None

		self.destroy()

		return ret

	def on_update_preview(self, chooser):
		uri = chooser.get_uri()
		try:
			pixbuf = gtk.gdk.pixbuf_new_from_file(uri[7:])
			
			w, h = make_thumb(50, pixbuf.get_width(), pixbuf.get_height())
			pixbuf = pixbuf.scale_simple(w, h, gtk.gdk.INTERP_BILINEAR)
			
			chooser.get_preview_widget().set_from_pixbuf(pixbuf)
		except:
			chooser.get_preview_widget().set_from_stock(gtk.STOCK_DIALOG_QUESTION,
				gtk.ICON_SIZE_DIALOG)
		
		chooser.set_preview_widget_active(True)


class Mask (gtk.Window):
	def __init__ (self):
		gtk.Window.__init__ (self)
		self.set_title ("Maschera Pesci Dolce")

		self.pvt_dict = {}

		self.tbl = tbl = gtk.Table (5, 2)

		self.nome_comune = self.dummy_attach ("Nome comune", 0)
		self.specie = self.dummy_attach ("Specie", 1)
		self.genere = self.dummy_attach ("Genere", 2)
		self.famiglia = self.dummy_attach ("Famiglia", 3)
		self.ordine = self.dummy_attach ("Ordine" , 4)
		self.luogo_provenienza = self.dummy_attach ("Luogo di provenienza", 5)
		self.allevamento = self.dummy_attach ("Allevamento", 6)
		self.compatibilita = self.dummy_attach ("Compatibilità", 7)
		self.riproduzione = self.dummy_attach ("Riproduzione", 8)
		self.temperatura = self.dummy_attach ("Temperatura", 9)
		self.gh = self.dummy_attach ("Gh", 10)
		self.ph = self.dummy_attach ("pH", 11)
		self.lunghezza_raggiunta = self.dummy_attach ("Lunghezza raggiunta", 12)
		self.zona_nuoto = self.dummy_attach ("Zona di nuoto", 13)
		self.immagine = self.dummy_attach ("Immagine", 14)
		
		

		btn = gtk.Button (stock = gtk.STOCK_SAVE)
		btn.connect ("clicked", self.on_save)
		tbl.attach (btn, 1, 2, 15, 16)

		btn = gtk.Button (stock = gtk.STOCK_OPEN)
		btn.connect ("clicked", self.on_open)
		tbl.attach (btn, 0, 1, 15, 16)

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

		nome_com = self.get ("Nome comune")
		specie_a  = self.get ("Specie")
		genere_a = self.get ("Genere")
		famiglia_a = self.get ("Famiglia")
		ordine_a = self.get ("Ordine")
		luogo_provenienza_a = self.get ("Luogo di Provenienza")
		allevamento_a = self.get ("Allevamento")
		compatibilita_a = self.get ("Compatibilità")
		riproduzione_a = self.get ("Riproduzione")
		temperatura_a = self.get ("Temperatura")
		gh_a = self.get ("Gh")
		ph_a = self.get ("pH")
		lunghezza_raggiunta_a = self.get ("Lunghezza raggiunta")
		zona_nuoto_a = self.get ("Zona di nuoto")
		

		# NB: Per adesso stampiamo solamente sullo stdout

		doc = getDOMImplementation ().createDocument (None, "pyacqua", None)

		# L'elemento principale e' questo
		fish_el = doc.createElement ("fish")
		fish_el.setAttribute ("name", name) # Settiamo il name <fish name="unz">

		doc.documentElement.appendChild (fish_el) # Appendiamo al documento

		# Creiamo il child nome comune di fish
		nome_el = doc.createElement ("nome comune")
		nome_el.setAttribute ("specie", nom)

		fish_el.appendChild (nome_el) # <fish><family /></fish>
		
		# Child del dell'elemento family che e' child di fish :P
		specie_el = doc.createElement ("specie")
		specie_el.setAttribute ("specie", spe)

		fish_el.appendChild (specie_el)

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
