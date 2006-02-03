import gtk
import os
from pysqlite2 import dbapi2 as sqlite

class Vasca(gtk.Window):
	def __init__(self): 

		gtk.Window.__init__(self)
		self.set_name("Asdasso")
		box = gtk.VBox()
		
		
		
		self.vasca_store = gtk.ListStore(int, str, str, str, str, str, str, str, str)
		view = gtk.TreeView(self.vasca_store)
		lst = ['Id', 'Vasca', 'Data', 'Nome', 'Tipo Acquario', 'Tipo Filtro', 'Impianto Co2', 'Illuminazione']
		renderer = gtk.CellRendererText()
		
		for i in lst:
			id = lst.index(i)
			col = gtk.TreeViewColumn(i, renderer, text=id)
			col.set_sort_column_id(id+1)
			col.set_clickable(True)
			col.set_resizable(True)
			view.append_column(col)
		view.get_selection().connect('changed', self.on_clicked)
		box.pack_start(view)
		
		connessione=sqlite.connect(os.path.join('Data', 'db'))
		cursore=connessione.cursor()
		cursore.execute("select * from vasca")

		# Eliminiamo le vecchie righe
		self.vasca_store.clear()
		
		for y in cursore.fetchall():
			self.vasca_store.append([y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[8]])
		
		
		# Usiamo un expander per rendere tutto piu' appetibile
		self.exp = exp = gtk.Expander("<b>Editing</b>")
		# Facciamo in modo che riconosca i tag di formattazione (<b>)
		exp.set_use_markup(True)
		# Creiamo una buttonbox per contenere i bottoni di modifica
		bb = gtk.HButtonBox()
		bb.set_layout(gtk.BUTTONBOX_END)
		btn = gtk.Button("Aggiungi")
		btn.connect('clicked', self.on_add)
		bb.pack_start(btn)
		btn = gtk.Button("Save")
		btn.connect('clicked', self.on_save)
		bb.pack_start(btn)
		btn = gtk.Button("Rimuovi")
		btn.connect('clicked', self.on_del)
		bb.pack_start(btn)
		# Attacchiamo alla box expander e buttonbox
		# in modo da non farli allargare durante il
		# ridimensionamento :)
		box.pack_start(bb, False, False, 0)
		box.pack_start(exp, False, False, 0)
		# Creiamo la table che verra contenuta nell'expander
		tbl = gtk.Table(3, 2)
		tbl.attach(gtk.Label("Nome:"), 0, 1, 0, 1)
		tbl.attach(gtk.Label("Descrizione:"), 0, 1, 1, 2)
		self.e_name, self.e_desc = gtk.Entry(), gtk.Entry()
		tbl.attach(self.e_name, 1, 2, 0, 1)
		tbl.attach(self.e_desc, 1, 2, 1, 2)
		exp.add(tbl)
		self.add(box)
		self.show_all()
		gtk.main()

	def on_save(self, widget): 
# Prendiamo l'iter e il modello dalla selezione
		mod, it = self.view.get_selection().get_selected()
		# Se esiste una selezione aggiorniamo la row
		# in base al contenuto delle entry
	#if it != None:
		#mod.set_value(it, 0, self.e_name.get_text())
		#mod.set_value(it, 1, self.e_desc.get_text())

	def on_add(self, widget): 
# Aggiungiamo dei valori casuali che andranno subito ad essere modificati
# dall'utente
		it = self.store.append()
		self.store.set(it, 0, "EDIT ME")
		self.store.set(it, 1, "EDIT ME")
	def on_del(self, widget): 
# prendiamo l'iter selezionato e elimianiamolo dalla store
		mod, it = self.view.get_selection().get_selected()

	#if it != None:
		#self.store.remove(it)     

	def on_clicked(self, sel):
#Aggiorniamo il contenuto delle entry in base alla selezione
		mod, it = sel.get_selected()
	#if it != None:
		#self.e_name.set_text(mod.get_value(it, 0))
		#self.e_desc.set_text(mod.get_value(it, 1))
		#self.exp.set_expanded(True)
	#else:
		#self.e_name.set_text('')
		#self.e_desc.set_text('')
		#self.exp.set_expanded(False)
#if __name__ == "__main__":
 # Example()
