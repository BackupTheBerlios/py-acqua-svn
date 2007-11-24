import gtk
import gobject
import httplib
import threading
import generate
import app
import utils
import os
import os.path
import sys

from xml.dom.minidom import parseString, getDOMImplementation
from updater.database import DatabaseWrapper, DatabaseReader
from updater.xmlreport import ReportReader

REPOSITORY_ADDRESS = None
BASE_DIR = None
LIST_FILE = None

if os.name == 'nt':
	REPOSITORY_ADDRESS = "www.pyacqua.net"
	REPOSITORY_ADDRESS = "localhost"
	BASE_DIR = "/update/windows/"
	LIST_FILE = "/update/win32-list.xml"
else:
	REPOSITORY_ADDRESS = "www.pyacqua.net"
	BASE_DIR = "/update/source/"
	LIST_FILE = "/update/source-list.xml"

DB_FILE = "pyacqua.db"
XML_FILE = "pyacqua.xml"

REPOSITORY_ADDRESS = r"localhost"
#BASE_DIR = r"/~stack/update/source/"
#LIST_FILE = r"/~stack/update/source-list.xml"

class SchemaUpdateInterface(object):
	def __init__(self, data):
		doc = parseString(data)
		
		self.info = {
			"mainversion" : 	[None, int],
			"secondversion" : 	[None, int],
			"revision" : 		[None, int],
			"message" : 		[None, str]
		}
		
		self.arrays = {
			"downloads" : {
				"svn" : 	[],
				"windows" : 	[],
				"tarball" : 	[]
			},
			"actions" : {
				"pre" : 	[],
				"post" : 	[]
			},
			"mirrors" : {
				"url" : 	[]
			}
		}
		
		self.program = None # il database sara' => "%s/%s-update.db" % (mirrors[0], self.program)

		if doc.documentElement.tagName.lower().endswith("-update"):
			self.program = doc.documentElement.tagName[:-7]

		if self.program == None:
			raise Exception("No such program")
		
		for node in doc.documentElement.childNodes:
			if node.nodeName.lower() == "info":
				self.__parseInfo(node)
			elif node.nodeName.lower() == "mirrors" or node.nodeName.lower() == "actions" or node.nodeName.lower() == "downloads":
				self.__parseArray(node, node.nodeName.lower())
	
	def __parseInfo(self, node):
		for i in node.childNodes:
			if i.nodeName.lower() in self.info.keys():
				converter = self.info[i.nodeName.lower()][1]
				self.info[i.nodeName.lower()][0] = converter((i.lastChild) and(i.lastChild.data) or(None))
	
	def __parseArray(self, node, category):
		kittie_cat = self.arrays[category]
		print kittie_cat, category
		
		for i in node.childNodes:
			print i.nodeName, kittie_cat.keys()
			
			if i.nodeName.lower() in kittie_cat.keys():
				kittie_cat[i.nodeName.lower()].append(i.lastChild.data)
	
	def getInfo(self, id):
		if id in self.info:
			return self.info[id]
		return None
	
	def getList(self, cat, subcat):
		if cat in self.arrays:
			if subcat in self.arrays[cat]:
				return self.arrays[cat][subcat]
		return None
	
	def getProgramName(self):
		return self.program
	
	def checkDiff(self, other):
		"""
		Ritorna:
			3 se le versioni sono incompatibili
			2 se le versioni sono potenzialmente compatibile
			1 se le verrsioni sono compatibili
			0 se le versioni sono identiche
		"""
		o_m, o_s, o_r = other.getInfo("mainversion"), other.getInfo("secondversion"), other.getInfo("revision")
		c_m, c_s, c_r = self.getInfo("mainversion"), self.getInfo("secondversion"), self.getInfo("revision")
		
		if o_m == m and o_s == s and o_r == r: return 0
		if o_m != m: return 3
		else:
			if o_s != s: return 2
			if o_r != r: return 1
	
	def getCurrentSchema():
		return SchemaUpdate(os.path.join(utils.DHOME_DIR, "pyacqua.xml"))
	
	getCurrentSchema = staticmethod(getCurrentSchema)

class Fetcher(threading.Thread):
	
	def __init__(self, callback, url, args=None):
		self.data = None
		self.callback = callback
		self.url = url
		self.args = args
		threading.Thread.__init__(self, name="Fetcher")

	def run(self):
		try:
			self.response = None; self.data = None
			try:
				conn = httplib.HTTPConnection(REPOSITORY_ADDRESS)
				conn.request("GET", self.url)
				self.response = conn.getresponse()
				self.data = self.response.read()
			except:
				print _("!! Errore mentre scaricavo da %s") % self.url
		finally:
			gobject.idle_add(self.__onData)

	def __onData(self):
		gtk.gdk.threads_enter()
		
		try:
			self.callback(self.data, self.response, self.args)
		finally:
			gtk.gdk.threads_leave()
		
		return False

if not _:
	_ = lambda x: x

class WebUpdate(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		
		utils.set_icon(self)
		self.set_title(_("Web Update"))
		self.set_size_request(600, 400)
		
		vbox = gtk.VBox(False, 2)
		
		self.nb = gtk.Notebook()
		vbox.pack_start(self.nb)
		
		self.status = gtk.Statusbar()
		vbox.pack_start(self.status, False, False, 0)
		
		self.add(vbox)
		
		self.connect('delete-event', self._on_delete_event)
		
		# ---------------------------------------------------------------------------------------
		
		self.store = gtk.TreeStore(
			gtk.gdk.Pixbuf, # icona
			str, # nome file
			int, # new_revision
			int, # bytes
			str, # md5
			int, # old_revision
			int, # old bytes
			str, # old_md5
			int, # percentuale scaricamento
			bool, # da scaricare
			gtk.gdk.Color # colre di background
		)
		self.tree = gtk.TreeView(self.store)
		self.tree.append_column(gtk.TreeViewColumn("", gtk.CellRendererPixbuf(), pixbuf=0))

		rend = gtk.CellRendererText(); id = 1
		
		for i in(_("File"), _("Rev"), _("Bytes"), _("MD5"), _("oldRev"), _("oldBytes"), _("oldMD5")):
			col = gtk.TreeViewColumn(i, rend, text=id)
			self.tree.append_column(col)
			id += 1
			
		# Colonna percentuale
		rend = gtk.CellRendererProgress()
		col = gtk.TreeViewColumn(_("%"), rend, value=8)
		
		self.tree.append_column(col)
		
		# Background su tutte le celle
		for i in self.tree.get_columns():
			i.add_attribute(i.get_cell_renderers()[0], 'cell_background-gdk', 10)
		
		sw = gtk.ScrolledWindow()
		sw.add(self.tree)
		
		vbox = gtk.VBox(False, 2)
		vbox.pack_start(sw)
		
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		
		self.update_btn = btn = utils.new_button(_("Aggiorna"), gtk.STOCK_REFRESH)
		btn.connect('clicked', self._on_start_update)
		bb.pack_start(btn)

		btn.set_sensitive(False)

		self.get_btn = btn = utils.new_button(_("Controlla Aggiornamenti"), gtk.STOCK_APPLY)
		btn.connect('clicked', self.onGetList)
		bb.pack_start(btn)
		
		vbox.pack_start(bb, False, False, 0)
		
		self.nb.append_page(vbox)
		
		self.file = None
		self.it = None
		
		self.program_list = None
		
		self.icon_add = gtk.gdk.pixbuf_new_from_file(os.path.join(utils.DPIXM_DIR, "add.png"))
		self.icon_del = gtk.gdk.pixbuf_new_from_file(os.path.join(utils.DPIXM_DIR, "del.png"))
		self.icon_done = gtk.gdk.pixbuf_new_from_file(os.path.join(utils.DPIXM_DIR, "done.png"))
		self.icon_error = gtk.gdk.pixbuf_new_from_file(os.path.join(utils.DPIXM_DIR, "error.png"))
		self.icon_program = gtk.gdk.pixbuf_new_from_file(os.path.join(utils.DPIXM_DIR, "error.png"))
		
		self.color_add = gtk.gdk.color_parse('#70ef70')
		self.color_del = gtk.gdk.color_parse('#ff8080')
		self.color_done = gtk.gdk.color_parse('#bcfffc')
		self.color_error = gtk.gdk.color_parse('#ff9060')
		
		# ---------------------------------------------------------------------------------------

		# Dobbiamo inserire una checklist per scegliere quali componenti aggiornare.
		# Quindi facciamo un for sulle entry del database locale per creare la lista
		# dei vari programmi.
		
		vbox = gtk.VBox(False, 2)
		
		self.choice_store = gtk.ListStore(
			gtk.gdk.Pixbuf, # icona
			str, # nome programma
			bool, # checked
		)
		
		self.choice_tree = gtk.TreeView(self.choice_store)
		
		col = gtk.TreeViewColumn("", gtk.CellRendererPixbuf(), pixbuf=0)
		col.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		col.set_fixed_width(50)
		
		self.choice_tree.append_column(col)
		
		col = gtk.TreeViewColumn(_("Program"), gtk.CellRendererText(), text=1)
		col.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
		
		self.choice_tree.append_column(col)
		
		rend = gtk.CellRendererToggle()
		rend.connect('toggled', self.onToggled, self.choice_tree.get_model())
		
		col = gtk.TreeViewColumn("", rend, active=2)
		col.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		col.set_fixed_width(50)
		
		self.choice_tree.append_column(col)
		
		sw = gtk.ScrolledWindow()
		sw.add(self.choice_tree)
		
		vbox.pack_start(sw)

		self.program_db = DatabaseWrapper(os.path.join(utils.DHOME_DIR, DB_FILE))
		self.program_iters = []
		
		self.populateChoiceStore()
		
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		
		btn = utils.new_button(_("Procedi con l'aggiornamento"), gtk.STOCK_GO_FORWARD)
		btn.connect('clicked', self.onGoForward)
		bb.pack_start(btn)
		
		vbox.pack_start(bb, False, False, 0)
		
		self.nb.append_page(vbox)
		
		self.show_all()
	
	def populateChoiceStore(self):
		for i in self.program_db.select("SELECT name FROM program")[0]:
			self.choice_store.append([self.icon_program, i, False])
	
	def populateUpdateTree(self, p_list):
		for i in p_list:
			self.store.append(None,
				[
					self.icon_program,
					i,
					0,
					0,
					"",
					0,
					0,
					"",
					0,
					False,
					self.color_done
				]
			)
		
		self.program_list = p_list
	
	def onToggled(self, cell, path, model):
		iter = model.get_iter((int(path),))
		fixed = model.get_value(iter, 2)
		fixed = not fixed
		model.set(iter, 2, fixed)
	
	def onGoForward(self, widget):
		# Facciamo un for sugli iter e controlliamo quali sottoprogrammi abbiamo abilitato
		
		model = self.choice_tree.get_model()
		it = self.choice_tree.get_model().get_iter_first()
		
		p_list = []
		
		while it:
			if model.get_value(it, 2):
				p_list.append(model.get_value(it, 1))
			it = model.iter_next(it)
		
		if len(p_list) == 0:
			self.status.push(0, _("Seleziona almeno un componente per l'aggiornamento."))
		else:
			self.choice_store.clear()
			self.nb.set_current_page(0)
			self.populateUpdateTree(p_list)
	
	def onGetList(self, widget):
		widget.set_sensitive(False)

		idx = 0
	
		for i in self.program_list:
			self.startThread(
				self.populateProgramIter,
				BASE_DIR + i + "-update.xml",
				idx
			)
			idx += 1
	
	def startThread(self, callback, url, args=None):
		print _(">> Creo un thread per %s") % url
		f = Fetcher(callback, url, args)
		f.setDaemon(True)
		f.start()
	
	def getIterFromIndex(self, idx):
		prog = self.program_list[idx]
		
		model = self.tree.get_model()
		it = self.tree.get_model().get_iter_first()
		
		while it:
			if model.get_value(it, 1) == prog:
				return it
			
			it = model.iter_next(it)
		
		raise "ARGHHH No Iter!"

	def populateProgramIter(self, data, response, index):
		self.get_btn.set_sensitive(True)
		
		it = self.getIterFromIndex(index)
		model = self.tree.get_model()
		
		print response.status, data

		if data == None:
			#self.status.push(0, _("Impossibile recuperare la lista dei file dal server."))
			model.set_value(it, 10, self.color_error)
			return

		if response.status != 200:
			#self.status.push(0, _("Errore durante lo scaricamento della lista dei file(HTTP %d)") % response.status)
			model.set_value(it, 10, self.color_error)
			return
	
		try:
			# TODO: in pratica qui dovremmo leggere la revisione e piazzarla nella colonna
			# infatti suggerisco di modificare il nome delle colonne eliminando la col per l'md5
			# e inserirne solo 2 una per la revision nuova e una per la vecchia
			# NOTA: una sola colonna contenente revision tipo 1.2-r2
			report = ReportReader(data)
			new_schema = SchemaUpdateInterface(parseString(data))
			old_schema = SchemaUpdateInterface.getCurrentSchema()
			
			ret = old_schema.checkDiff(new_schema)
			
			if ret == 0:
				# messaggio nessun aggiornamento disponibile ecc...
				utils.info(_("Nessun aggiornamento disponibile"))
			if ret == 1:
				# versioni compatibili possiamo aggiornare
				self.__checkFileToUpdate(new_schema)
			if ret == 2:
				# TODO: Una choice ..
				# come una clean install
				utils.warning(_("Le versioni sono potenzialmente compatibili\nma _NON_ viene garantito il perfetto aggiornamento"))
				pass
			if ret == 3:
				utils.error(_("Versioni incompatibili per procedere con l'aggiornamento"))
				pass
		except:
			self.status.push(0, _("Impossibile interpretare il file xml"))
			return
		
		self.update_btn.set_sensitive(True)
	
	def __checkFileToUpdate(self, schema):
		self.mirrors = schema.getList("mirrors", "url")
		self.program = schema.getProgramName()

		if self.program == None or self.mirrors == None:
				utils.error(_("Impossibile procedere con l'aggiornamento. Nessun mirror trovato o nome programma assente"))
				self.status.push(0, _("Nessun mirror fornito o nome programma assente"))
				return

		self._thread(self.__markFileForUpdate, utils.url_encode("%s/%s-update.db" % (self.mirrors[0], self.program)))
	
	def __markFileForUpdate(self, data, response):
		
		# Finche non abbiamo scaricato il database proviamo con il mirror successivo

		if not data or response.status != 200:

			if len(self.mirrors) == 0:
				utils.error(_("Impossibile scaricare il database delle revisioni"))
				self.status.push(0, _("Impossibile scaricare il database delle revisioni"))
				return
			else:
				self._thread(self.__markFileForUpdate, utils.url_encode("%s/%s-update.db" % (self.mirrors[0], self.program)))
				del self.mirrors[0]

		# Ok abbiamo scaricato correttamente il database

		self.__diffDatabase(data)
	
	def __diffDatabase(self, data, programs_list):
		f = open(os.path.join(utils.UPDT_DIR, self.file), 'wb')
		f.write(data)
		f.close()

		new_db = DatabaseReader(os.path.join(utils.UPDT_DIR, self.file))
		old_db = DatabaseReader(os.path.join(utils.DHOME_DIR, DB_FILE))

		# Bisogna fare un diff sulle row e controllare le entry delle revisioni
		# Possiamo avere un update tra revision differenti e tra
		# revision e secondversion differenti

		if new_db.v_main != old_db.v_main:
			return False

		if new_db.v_ver != old_db.v_ver:
			# Full update di tutti i file..
			pass
		
		if new_db.v_rev == old_db.v_rev:
			return True

		return True
		
	def _on_start_update(self, widget):
		self.it = self.tree.get_model().get_iter_first()
		self._update_from_iter()
		
	def _update_file(self, data, response):
		# Dovremmo semplicemente salvare in una directory temporanea
		# del tipo ~/.pyacqua/.update o .update nella directory corrente
		# insieme ad una lista di file|bytes|checksum per il controllo sull'update
		# Al riavvio il programma dovrebbe controllare che in .update ci siano file
		# e aggiornare di conseguenza
		
		# TODO: da finire
		
		if not data:
			print _(">> Nessun file da ricevere")
		
		if response.status != 200:
			self._sign_error(response)
			return

		print response.status
		
		# Creiamo le subdirectory necessarie
		dirs = self.file.split(os.path.sep); dirs.pop()
		path = utils.UPDT_DIR
		
		try:
			for i in dirs:
				path = os.path.join(path, i)
				if not os.path.exists(path):
					os.mkdir(path)
		
			print _(">> File ricevuto %s") % self.file
		
			f = open(os.path.join(utils.UPDT_DIR, self.file), 'wb')
			f.write(data)
			f.close()
			
			self._update_percentage()
			self._go_with_next_iter()
		except:
			self._sign_error(response)
	
	def _sign_error(self, response):
		# Qualcosa di strano e' successo.. mhuahuahuau *_*
		# -.- come stiamo sotto
		
		self.tree.get_model().set_value(self.it, 0, self.icon_error)
		self.tree.get_model().set_value(self.it, 10, self.color_error)
		self.tree.get_model().set_value(self.it, 8, 0)
		
		self.status.push(0, _("Errore durante lo scaricamento di %s(response: %d)") %(self.file, response.status))
		
		# Qui dovresti bloccare tutto e cancellare i file gia scaricati
		# altrimenti nella callback di scaricamento dovresti inserire un check
		# se esistono gia dei file che dovrebbero essere scaricati controlli md5 e bytes e se giusti
		# non li scarichi
		
	def _update_percentage(self):
		self.tree.get_model().set_value(self.it, 0, self.icon_done)
		self.tree.get_model().set_value(self.it, 10, self.color_done)
		self.tree.get_model().set_value(self.it, 8, 100)
		
	def _go_with_next_iter(self):
		self.it = self.tree.get_model().iter_next(self.it)
		self._update_from_iter()
		
	def _update_from_iter(self):
		if self.it != None:
			self.file = self.tree.get_model().get_value(self.it, 1)
			
			if self.tree.get_model().get_value(self.it, 9):
				
				# FIXME: Controlla se esiste gia il file(se l'abbiamo scaricato precedentemente)
				tmp = os.path.join(utils.UPDT_DIR, self.file)
				
				if os.path.exists(tmp):
					# Controlliamo se il file e' corretto
					bytes = os.path.getsize(tmp)
					md5   = generate.Generator.checksum(tmp)
					
					if md5 != self.tree.get_model().get_value(self.it, 4) or int(bytes) != self.tree.get_model().get_value(self.it, 3):
						os.remove(tmp)
						self._thread(self._update_file, utils.url_encode(BASE_DIR + self.file))
					else:
						self._update_percentage()
						self._go_with_next_iter()
				else:
					self._thread(self._update_file, utils.url_encode(BASE_DIR + self.file))
			else:
				self._update_percentage()
				self._go_with_next_iter()
		else:
			self.xml_util.dump_tree_to_file(self.diff_object, os.path.join(utils.UPDT_DIR, ".diff.xml"))
			
			utils.info(_("Riavvia per procedere all'aggiornamento di PyAcqua"))
			
			self.destroy()
			
			# La list.xml la si becca dal sito.. ergo no problem
	def _on_delete_event(self, *w):
		app.App.p_window["update"] = None

if __name__ == "__main__":
	WebUpdater()
	gtk.main()
