#!/usr/bin/env python
# -*- coding: iso-8859-15 -*- 
#Copyright (C) 2005, 2006 Luca Sanna - Italy
#http://pyacqua.altervista.org
#email: pyacqua@gmail.com  
#
#   
#Py-Acqua is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#Py-Acqua is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Py-Acqua; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
import webbrowser
import locale
import gettext
import sys


APP = 'acqua'
DIR = 'locale'

try:
	locale.setlocale(locale.LC_ALL, 'en_US')
	gettext.bindtextdomain(APP, DIR)
	gettext.textdomain(APP)
	gettext.install("acqua", DIR, unicode=1)
except (IOError, locale.Error), e:
	print "(%s): WARNING **: %s" % (APP, e)
	__builtins__.__dict__["_"] = lambda x : x
	__builtins__.__dict__["ngettext"] = gettext.ngettext

try:
	# Richiediamo gtk2
	import pygtk
	pygtk.require('2.0')
except:
	# Gtk2 assente proviamo lo stesso con gtk
	pass

try:
	import gtk
except:
	print _("You need to install pyGTK or GTKv2")

try:
	#import pysqlite2 as sqlite
	from pysqlite2 import dbapi2 as sqlite
except:
	print _("You need to install pysqlite")

import os
#import files.finestre

os.environ['PATH'] += r";lib;etc;bin;ghost\gs8.53\bin"

### creiamo la directory che contiene le immagini

if not os.path.exists('Immagini'):
	os.mkdir('Immagini')
### creiamo la directory per i plugin ###	
if not os.path.exists('Plugin'):
			os.mkdir('Plugin')
	
### creiamo la directory che contiene il database

if not os.path.exists('Data'):
	os.mkdir('Data')
	
### creiamo il database con sqlite



if not os.path.exists("Data/db"):
	connessione=sqlite.connect("Data/db")
	cursore=connessione.cursor()
	cursore.execute("create table vasca (id integer, vasca TEXT, date DATE, nome TEXT, tipo TEXT, filtro TEXT, co TEXT, illuminazione TEXT, img TEXT)")
	cursore.execute("create table test(id integer, date DATE, vasca TEXT, ph FLOAT, kh FLOAT, gh FLOAT, no FLOAT, noo FLOAT, con FLOAT, amm FLOAT, fe FLOAT, ra FLOAT, fo FLOAT)")
	cursore.execute("create table pesci(id integer, date DATE, vasca FLOAT, quantita NUMERIC, nome TEXT, img TEXT)")
	cursore.execute("create table invertebrati(id integer, date DATE, vasca FLOAT, quantita NUMERIC, nome TEXT, img TEXT)")
	cursore.execute("create table piante(id integer, date DATE, vasca FLOAT, quantita NUMERIC, nome TEXT, img TEXT)")
	cursore.execute("create table fertilizzante (id integer,date DATE, nome TEXT, quantita FLOAT, giorni NUMERIC)")
	cursore.execute("create table spese(id integer, date DATE, vasca FLOAT, tipologia TEXT, quantita NUMERIC, nome TEXT,soldi TEXT, img TEXT)")
	cursore.execute("create table filtro (id integer,date DATE, giorni NUMERIC)")
	cursore.execute("create table datapesci (nome TEXT, cara TEXT)")
	cursore.execute("create table datapiante (nome TEXT, cara TEXT)")
	connessione.commit()
	
def fix_actions(actions, instance):
	retval = []
	
	# Iteriamo l'array e sostituiamo la stringa della callback
	# con l'indirizzo del metodo
	
	for i in range(len(actions)):
		curr = actions[i]
		if len(curr) > 5:
			curr = list(curr)
			curr[5] = getattr(instance, curr[5])
			curr = tuple(curr)

		retval.append(curr)
	
	# Ritorniamo la lista con le modifiche
	return retval
	
class Gui(gtk.Window):
	
	def create_menu(self):
		w = [
		('Acquario', None, _('_Acquario')),
			('Calcoli', None, _('_Calcoli'), '<control>C', _('Calcoli...'), 'calcoli_apri'),
			
			('Vasche', None, _('_Vasche'), '<control>V', _('Vasche...'), 'vasca_apri'),
			
			('Test', None, _('_Test'), '<control>T', _('Test'), 'test_apri'),
			
			('Pesci', None, _('_Pesci'), '<control>P', _('Pesci...'), 'pesci_apri'),
			
			('Piante', None, _('_Piante'), '<control>I', _('Piante...'), 'piante_apri'),
			
			('Invertebrati', None, _('_Invertebrati'), '<control>R', _('Invertebrati...'), 'invertebrati_apri'),
			
			('Database', None, _('_Database'), '<control>D', _('Database...')),
			
			('Quit', gtk.STOCK_QUIT, _('_Quit'), None, _('Esci da Py-Acqua'), 'exit'),
			
		('Impostazioni', None, _('_Impostazioni')),
		
			('Tips Tricks',	None, _('_Tips Tricks'), None, _('Tips and Tricks...'), 'tips_apri'),
			
			('Fertilizzante', None, _('_Fertilizzante'), None, _('fertilizzante...'), 'fertilizzante_apri'),
			
			('Filtro', None, _('_Filtro'), None, _('filtro...'), 'filtro_apri'),

			('Calendario', None, _('_Calendario'), None, _('Calendario...'),'calendario_apri'),
			
			('Inserisci', None, _('_Inserisci'), None, _('Inserisci...'), 'inserisci_apri'),
			
			('Allarmi', None, _('_Allarmi'), None, _('Allarmi...'), 'allarmi_apri'),
			
			('Spese', None, _('_Spese'), None, _('Spese...'), 'spese_apri'),
			
			('Skin', None, _('_Skin'), None, _('Skin...'), 'skin_apri'),
			
			('Configurazione', None, _('_Configurazione'), None, _('Configurazione'), 'config_apri'),
		
		('Plug-in', None, _('_Plug-in')),
			
			('Plugins',	None, _('_Plug-in'), None, _('Plug-in...'), 'plugin_apri'),
			
		('Update', None, _('_Update')),
			
			('Aggiorna',	None, _('_Aggiorna'), None, _('Aggiorna...'), 'update_apri'),

		('Aiuto', None, _('_Aiuto')),
		
			('Info', gtk.STOCK_ABOUT, _('_Informazioni'), None, _('Riguardo Py-Acqua'), 'informazioni_apri'),
			
			('Help', None, _('_Aiuto'), None, _('Aiuto...'), 'aiuto_apri'),
		]
		
		ui = """<ui>
		<menubar name='Menubar'>
		<menu action='Acquario'>
			<menuitem action='Calcoli'/>
			<menuitem action='Vasche'/>
			<menuitem action='Test'/>
			<menuitem action='Pesci'/>
			<menuitem action='Piante'/>
			<menuitem action='Invertebrati'/>
			<menuitem action='Database'/>
			<separator/>
			<menuitem action='Quit'/>
		</menu>
		<menu action='Impostazioni'>
			<menuitem action='Tips Tricks'/>
			<menuitem action='Fertilizzante'/>
			<menuitem action='Filtro'/>
			<menuitem action='Calendario'/>
			<menuitem action='Inserisci'/>
			<menuitem action='Allarmi'/>
			<menuitem action='Spese'/>
			<menuitem action='Skin'/>
			<menuitem action='Configurazione'/>
		</menu>
		<menu action='Plug-in'>
			<menuitem action='Plugins'/>
		</menu>
		<menu action='Update'>
			<menuitem action='Aggiorna'/>
		</menu>
		<menu name='AboutMenu' action='Aiuto'>
			<menuitem action='Info'/>
			<menuitem action='Help'/>
		</menu>
		</menubar></ui>"""
		
		ag = gtk.ActionGroup('WindowActions')
		
		actions = fix_actions(w, self)
		
		# Aggiungiamo le varie azioni.. (vedi
		# gtk.ActionGroup.add_actions)
		
		ag.add_actions(actions)
		
		self.ui = gtk.UIManager()
		self.ui.insert_action_group(ag, 0)
		self.ui.add_ui_from_string(ui)
		self.add_accel_group(self.ui.get_accel_group())
		
		self.ui.get_widget('/Menubar/AboutMenu').set_right_justified(True)
		
	def __init__(self):
		gtk.Window.__init__(self)
		
		self.set_title('Py-Acqua')
		self.set_size_request(467, 332)
		self.set_resizable(False)
		
		import files.impostazioni
		
		
		self.set_icon_from_file("pixmaps/logopyacqua.jpg")
		image = gtk.Image()
		image.set_from_file(files.impostazioni.sfondo)
		
		# Menu
		self.create_menu()
		
		vbox = gtk.VBox()
		
		vbox.pack_start(self.ui.get_widget('/Menubar'), False, False, 0)
		vbox.pack_start(image)
		
		self.add(vbox)
		self.show_all()
		self.connect('destroy', self.exit)
		
		import files.impostazioni
		if files.impostazioni.show_tips == "1":
			import files.tips
			files.tips.TipsDialog()
  
	def exit(*w):
		gtk.main_quit()
		
	def calcoli_apri(self, widget, data=None):
		import files.calcoli
		return files.calcoli.Calcoli()
	
	def test_apri(self, widget, data=None):
		import files.test
		return files.test.Test()
		
	def pesci_apri(self, widget, data=None):
		import files.pesci
		return files.pesci.Pesci()
		
	def piante_apri(self, widget, data=None):
		import files.piante
		return files.piante.Piante()
		
	def invertebrati_apri(self, widget, data=None):
		import files.invertebrati
		return files.invertebrati.Invertebrati()
		
	def vasca_apri(self, widget, data=None):
		import files.vasca
		return files.vasca.Vasca()
		
	def tips_apri(self, widget, data=None):
		import files.tips
		files.tips.TipsDialog()	
		
	def calendario_apri(self,widget, data=None):
		import files.calendario
		return files.calendario.Calendario()
		
	def inserisci_apri(self,widget, data=None):
		import files.inserisci
		return files.inserisci.Inserisci()
		
	def allarmi_apri(self, widget, data=None):
		import files.allarmi
		files.allarmi.Allarmi()
		
	def spese_apri(self, widget, data=None):
		import files.spese
		files.spese.Spese()
		
	def skin_apri(self, widget, data=None):
		import files.skin
		files.skin.Skin()
		
	def fertilizzante_apri(self, widget, data=None):
		import files.fertilizzante
		files.fertilizzante.Fertilizzante()
		
	def filtro_apri(self, widget, data=None):
		import files.filtro
		files.filtro.Filtro()
		
	def plugin_apri(self, widget, data=None):
		import files.plugin
		files.plugin.Plugin()
		
	def config_apri(self, widget, data=None):
		import files.config
		files.config.Config()
	
	def update_apri(self, widget, data=None):
		import files.update
		files.update.Update()		
		
	def informazioni_apri(self, widget, data=None):
		dialog = gtk.AboutDialog()
		
		dialog.set_name("PyAcqua 0.8")
		dialog.set_copyright("\302\251 Copyright (C) 2005, 2006 Luca Sanna - Italy")
		dialog.set_website("http://pyacqua.altervista.org")
		
		text = "Py-Acqua is free software; you can redistribute it and/or modify it under\n"
		text += "the terms of the GNU General Public License as published by the Free Software\n"
		text += "Foundation; either version 2 of the License, or (at your option) any later version.\n"
		text += "Py-Acqua is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;\n"
		text += "without even the implied warranty of MERCHANTABILITY or FITNESS FOR A\n"
		text += "PARTICULAR PURPOSE.  See the GNU General Public License for more details.\n\n"
		text += "You should have received a copy of the GNU General Public License along\n"
		text += "with Py-Acqua; if not, write to the Free Software Foundation, Inc.,\n"
		text += "51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA\n"
		
		dialog.set_license(text)
		
		text = [
			"Luca Sanna - Founder and lead developer - pyacqua@gmail.com",
			"Encrico Giubertoni - Web Site Manager - enrico.giubertoni@gmail.com",
			"Federico Degrandis - Developer - danger90@gmail.com",
			"Massimiliano Sist - DB and Tips and Tricks Manager -  massimiliano.sist@gmail.com",
			"Pietro Grassi - Release Tester - gnatophillum@gmail.com",
			"Piero Musu - Graphic - admin@irk.it",
			"Francesco Piccinno - Developer - stack@fallasa.it"
		]
		
		dialog.set_authors(text)
		dialog.connect ("response", lambda d, r: d.destroy())
		dialog.show()
	def aiuto_apri(self, widget, data=None):
		webbrowser.open('http://pyacqua.netsons.org/wiki/index.php/Wikipedia')
		
	def main(self):
		gtk.main()
	
if __name__ == "__main__":
	menu = Gui()
	menu.main()
