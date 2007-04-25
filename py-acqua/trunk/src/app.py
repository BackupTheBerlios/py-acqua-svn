# -*- coding: iso-8859-15 -*- 
#Copyright (C) 2005, 2007 Py-Acqua
#http://www.pyacqua.net
#email: info@pyacqua.net  
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

import gtk
import os
import utils
from impostazioni import get

App = None
	
class Gui(gtk.Window):
	"""
	Questa e' la classe che rappresenta la finestra principale di PyAcqua.
	"""
	
	def _fix_actions(self, actions, instance):
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
	
	def _create_menu(self):
		
		w = [
		('Acquario', None, _('_Acquario')),
			('Calcoli', None, _('_Calcoli'), '<control>C', _('Calcoli...'), '_on_open_calcoli'),
			
			('Vasche', None, _('_Vasche'), '<control>V', _('Vasche...'), '_on_open_vasca'),
			
			('Test', None, _('_Test'), '<control>T', _('Test'), '_on_open_test'),
			
			('Pesci', None, _('_Pesci'), '<control>P', _('Pesci...'), '_on_open_pesci'),
			
			('Piante', None, _('_Piante'), '<control>I', _('Piante...'), '_on_open_piante'),
			
			('Invertebrati', None, _('_Invertebrati'), '<control>R', _('Invertebrati...'), '_on_open_invertebrati'),
			
			#('Importa', gtk.STOCK_CONVERT, _('_Importa/Esporta...'), None, _('Importa/Esporta...'), '_on_open_importa'),
			
			('Quit', gtk.STOCK_QUIT, _('_Quit'), None, _('Esci da Py-Acqua'), 'exit'),
			
		('Impostazioni', None, _('_Impostazioni')),
		
			('Tips Tricks',	gtk.STOCK_DIALOG_INFO, _('_Tips Tricks'), None, _('Tips and Tricks...'), '_on_open_tips'),
			
			('Skin', gtk.STOCK_SELECT_COLOR, _('_Skin'), None, _('Skin...'), '_on_open_skin'),

			('Update', None, _('_Web Update'), None, _('Aggiorna PyAcqua'), '_on_open_update'),
			
			('Lingua', None, _('_Lingua'), None, _('Selezione Lingua...'), '_on_open_lang'),

		('Plugins', None, _('Plugins')),

			('PluginManager', gtk.STOCK_INDEX, _('_Manager'), None, _('Plug-in...'), '_on_open_plugin'),

			# i vari Plugin aggiungeranno qui le entry
		
		('Aiuto', None, _('_Aiuto')),
		
			('Info', gtk.STOCK_ABOUT, _('_Informazioni'), None, _('Riguardo Py-Acqua'), '_on_open_info'),
			
			
			('Help', None, _('_Aiuto'), None, _('Aiuto...'), '_on_open_help'),
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
			<separator/>
			<separator/>
			<menuitem action='Quit'/>
		</menu>
		<menu action='Impostazioni'>
			<menuitem action='Tips Tricks'/>
			<separator/>
			<menuitem action='Skin'/>
			<menuitem action='Update'/>
			<menuitem action='Lingua'/>
		</menu>
		<menu action='Plugins'>
			<menuitem action='PluginManager'/>
			<separator/>
		</menu>
		<menu name='AboutMenu' action='Aiuto'>
			<menuitem action='Info'/>
			
			<menuitem action='Help'/>
		</menu>
		</menubar></ui>"""
		
		ag = gtk.ActionGroup('WindowActions')
		
		actions = self._fix_actions(w, self)
		
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
		
		self.p_window = {
			"calcoli" : None,
			"test" : None,
			"pesci" : None,
			"piante" : None,
			"invertebrati" : None,
			"vasca" : None,
			"skin" : None,
			"plugin" : None,
			"lang" : None,
			"update" : None
		}
		
		utils.set_icon (self)
		
		image = gtk.Image()

		# Settiamo lo skin

		file = os.path.join (utils.SKIN_DIR, os.path.join (get ("skin"), "main.png"))
		
		if not os.path.exists (file):
			file = os.path.join (utils.DSKIN_DIR, os.path.join (get ("skin"), "main.png"))
		
		if os.path.exists (file):
			image.set_from_file(file)
		
		# Proviamo ad applicare lo stile gtk se presente
		path = os.path.join (get ("skin"), "gtkrc")
		
		if os.path.exists (os.path.join (utils.SKIN_DIR, path)):
			path = os.path.join (utils.SKIN_DIR, path)
		elif os.path.exists (os.path.join (utils.DSKIN_DIR, path)):
			path = os.path.join (utils.DSKIN_DIR, path)
		else:
			path = None
		
		if path:
			gtk.rc_set_default_files ([path])
			gtk.rc_reparse_all_for_settings (gtk.settings_get_default (), True)
		
		# Menu
		self._create_menu()
		
		vbox = gtk.VBox()
		
		vbox.pack_start(self.ui.get_widget('/Menubar'), False, False, 0)
		vbox.pack_start(image)
		
		self.add(vbox)
		self.show_all()
		self.connect('destroy', self.exit)

		self.tray = True
		
		if get ("show_tips"):
			import tips
			tips.TipsDialog()
		
	def exit(self, *w):
		gtk.main_quit()

	def _on_open_calcoli(self, widget, data=None):
		if not App.p_window["calcoli"]:
			import calcoli
			App.p_window["calcoli"] = calcoli.Calcoli()
	
	def _on_open_test(self, widget, data=None):
		if not App.p_window["test"]:
			import test
			App.p_window["test"] = test.Test()
		
	def _on_open_pesci(self, widget, data=None):
		if not App.p_window["pesci"]:
			import pesci
			App.p_window["pesci"] = pesci.Pesci()
		
	def _on_open_piante(self, widget, data=None):
		if not App.p_window["piante"]:
			import piante
			App.p_window["piante"] = piante.Piante()
		
	def _on_open_invertebrati(self, widget, data=None):
		if not App.p_window["invertebrati"]:
			import invertebrati
			App.p_window["invertebrati"] = invertebrati.Invertebrati()
		
	def _on_open_vasca(self, widget, data=None):
		if not App.p_window["vasca"]:
			import vasca
			App.p_window["vasca"] = vasca.Vasca()
		
	def _on_open_tips(self, widget, data=None):
		import tips
		tips.TipsDialog()	
		
	def _on_open_skin(self, widget, data=None):
		if not App.p_window["skin"]:
			import skin
			App.p_window["skin"] = skin.Skin()
		
	def _on_open_plugin(self, widget, data=None):
		if not App.p_window["plugin"]:
			import plugin
			App.p_window["plugin"] = plugin.Plugin()
	
	def _on_open_lang(self, widget, data=None):
		if not App.p_window["lang"]:
			import lang
			App.p_window["lang"] = lang.LangWindow()
		
	#def _on_open_importa(self, widget, data=None):
	#	import importa
	#	importa.Importa()
		
	def _on_open_info(self, widget, data=None):
		dialog = gtk.AboutDialog()
	
		dialog.set_name("PyAcqua 1.0")
		dialog.set_copyright("\302\251 Copyright (C) 2005, 2007 Luca Sanna - Italy")
		dialog.set_website("http://www.pyacqua.net")
		
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
			"Luca Sanna - Founder and lead developer",
			"Pietro Grassi - Release Tester",
			"Francesco Piccinno - Developer",
			"Giovanni Manzoni - Developer and Electronic"
		]
		
		dialog.set_authors (text)
		dialog.connect ("response", lambda d, r: d.destroy())
		dialog.run ()
		dialog.hide ()
		dialog.destroy ()
		
	def _on_open_help(self, widget, data=None):
		utils.info (_("Prova a vedere su http://www.pyacqua.net"))

	def _on_open_update(self, widget, data=None):
		if not App.p_window["update"]:
			import webupdate
			App.p_window["update"] = webupdate.WebUpdate()
		
	def main(self):
		self.active_toggle = False
		gtk.main()
	
	def get_plugin_menu(self):
		"""
		Ritorna il menu dei plugin.
		Questo metodo viene utilizzato dai plugin per aggiungere MenuItem al
		menu Plugins di questa classe.
		"""
		return self.ui.get_widget('/Menubar/Plugins').get_submenu()
