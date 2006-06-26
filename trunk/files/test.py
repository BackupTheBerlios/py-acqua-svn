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

import gtk
import gobject
import os
import sys
import utils
import dbwindow




class GraphPage (gtk.ScrolledWindow):
	
	def __init__ (self, legend=False):
		gtk.ScrolledWindow.__init__ (self)
		
		self.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
		self.legend = legend
		
		self.figure = Figure (figsize=(6,4), dpi=72)
		self.axis = self.figure.add_subplot (111)
		
		self.canvas = FigureCanvasGTK(self.figure)
		self.add_with_viewport (self.canvas)
		
		self.show_all ()
	
	def plot (self, values):
		
		self.axis.clear ()
		self.axis.set_ylabel('Valori')
		#self.axis.set_title('PyAcqua Grapher')
		self.axis.grid(True)
		
		self.values = values
		
		ind = arange (1)
		width = 0.25
		
		index = 0
		
		# TODO: i colori sono da sistemare
		colors = ('r', 'g', 'y', 'b', 'c', 'm', 'k', 'w', 'r', 'g', 'y', 'b', 'g')
		
		lst = zip (self.values, colors)
		
		bars = []
		labels = (_('pH'), _('KH'), _('GH'), _('NO2'), _('NO3'),
			_('Conducibilita'), _('Ammoniaca'), _('Ferro'), _('Rame'), _('Fosfati'),
			_('Calcio'), _('Magnesio'), _('Densita'))
		
		for i, c in lst:
			bars.append (self.axis.bar (ind + (width * index), i, width/2, color=c))
			index += 1
		
		self.axis.set_xticks (arange (12, step=0.25) + 0.25/4)
		self.axis.set_xticklabels (labels)
		self.axis.set_xlim (-width, 0.25 * 13)
		
		if self.legend:
			self.axis.legend (bars, labels, shadow=True, loc=1)
		
		self.canvas.draw ()
		

class Test (dbwindow.DBWindow):
	Chart = True
	Chart = False
	def __init__ (self): 
		# id integer, date DATE, vasca FLOAT, ph FLOAT, kh FLOAT, gh
		# NUMERIC, no NUMERIC, noo NUMERIC, con NUMERIC, amm NUMERIC, fe
		# NUMERIC, ra NUMERIC, fo NUMERIC
		
		lst = gtk.ListStore (
			int,	# ID
			str,	# DATA
			str,	# VASCA
			float,	# PH
			float,	# KH
			float,	# GH
			float,	# NO2
			float,	# NO3
			float,	# COND
			float,	# AMMO
			float,	# FERRO
			float,	# RAME
			float,	# FOSFATI
			float,	# calcio
			float,	# magnesio
			float)	# densita

		cols = [_('Id'), _('Data'), _('Vasca'), _('Ph'), _('Kh'), _('Gh'), _('No2'), _('No3'),
			_('Conducibilita\''), _('Ammoniaca'), _('Ferro'), _('Rame'), _('Fosfati'),
			_('Calcio'), _('Magnesio'), _('Densita\'')]
		
		inst = [utils.DataButton (), utils.Combo ()]
		
		for i in range (13): inst.append (utils.FloatEntry ())

		dbwindow.DBWindow.__init__ (self, 2, 7, cols, inst, lst)
		
		for y in utils.get ('select * from test'):
			lst.append ([y[0], y[1], y[2], y[3], y[4],
					y[5], y[6], y[7], y[8], y[9], y[10], y[11], y[12], y[13], y[14], y[15]])
		
		for y in utils.get ('select * from vasca'):
			self.vars[1].append_text (y[3])

		self.set_title (_("Test"))
		self.set_size_request (600, 400)
		self.set_icon_from_file ("pixmaps/logopyacqua.jpg")
		
		self.note.set_current_page (0)
		self.show_all ()
	
	def on_change_view (self, widget):
		id = widget.get_active ()
		
		if Test.Chart and id == 1:
			self.on_draw_graph (None)
			self.note.set_current_page (id)
		else:
			self.note.set_current_page (id)
	
	def pack_before_button_box (self, hb):
		cmb = utils.Combo ()
		
		cmb.append_text (_("Modifica"))
		
		if Test.Chart:
			cmb.append_text (_("Grafico"))
		
		cmb.append_text (_("Impostazioni"))
		
		cmb.set_active (0)
		
		cmb.connect ('changed', self.on_change_view)
		
		align = gtk.Alignment (0, 0.5)
		align.add (cmb)
		
		hb.pack_start (align, False, True, 0)
		
		if not Test.Chart:
			label = gtk.Label (_("<i>E' necessario matplotlib per i grafici.</i>"))
			label.set_use_markup (True)
			label.set_alignment (0, 0.5)
			hb.pack_start (label, False, True, 0)
		
		cmb.show ()
	
	def custom_page (self, edt_frame):
		import files.inserisci
		
		self.note = gtk.Notebook ()
		self.vbox.pack_start (self.note, False, False, 0)
		
		self.note.set_show_tabs (False)
		self.note.set_show_border (False)
		self.note.append_page (edt_frame)
		
		if Test.Chart:
			self.grapher = GraphPage ()
			self.note.append_page (self.grapher)
		
		self.note.append_page (files.inserisci.Inserisci ())
		
		# C'e' la custom page qui :P
		return True
		
	def after_refresh (self, it):
		mod, it = self.view.get_selection().get_selected()

		id = mod.get_value (it, 0)
		
		data = self.vars[0].get_text ()
		vasca = self.vars[1].get_text ()
		ph = self.vars[2].get_text ()
		kh = self.vars[3].get_text ()
		gh = self.vars[4].get_text ()
		no = self.vars[5].get_text ()
		no2 = self.vars[6].get_text ()
		cond = self.vars[7].get_text ()
		ammo = self.vars[8].get_text ()
		ferro = self.vars[9].get_text ()
		rame = self.vars[10].get_text ()
		fosfati = self.vars[11].get_text ()
		calcio = self.vars[12].get_text ()
		magnesio = self.vars[13].get_text ()
		densita = self.vars[14].get_text ()
		
		utils.cmd("update test set date='%(data)s', vasca='%(vasca)s', ph='%(ph)s', kh='%(kh)s', gh='%(gh)s', no='%(no)s', noo='%(no2)s', con='%(cond)s', amm='%(ammo)s', fe='%(ferro)s', ra='%(rame)s', fo='%(fosfati)s', calcio='%(calcio)s', magnesio='%(magnesio)s', densita='%(densita)s' where id=%(id)s" % vars ())
		
		self.update_status (dbwindow.NotifyType.SAVE, _("Row Aggiornata (ID: %d") % id)

	def add_entry (self, it):
		mod, id = self.view.get_selection ().get_selected ()

		id = mod.get_value (it, 0)
		
		utils.cmd ('insert into test values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', id,
				self.vars[0].get_text (),
				self.vars[1].get_text (),
				self.vars[2].get_text (),
				self.vars[3].get_text (),
				self.vars[4].get_text (),
				self.vars[5].get_text (),
				self.vars[6].get_text (),
				self.vars[7].get_text (),
				self.vars[8].get_text (),
				self.vars[9].get_text (),
				self.vars[10].get_text (),
				self.vars[11].get_text (),
				self.vars[12].get_text (),
				self.vars[13].get_text (),
				self.vars[14].get_text ()
				)

		self.update_status(dbwindow.NotifyType.ADD, _("Row aggiunta (ID: %d)") % id)
		
	def remove_id (self, id):
		utils.cmd ('delete from test where id=%d' % id)
		self.update_status(dbwindow.NotifyType.DEL, _("Row rimossa (ID: %d)" % id))
	
	def decrement_id (self, id):
		utils.cmd ('update test set id=%d where id=%d' % (id - 1, id))
		
	def after_selection_changed (self, mod, it):
		if self.note.get_current_page () == 1:
			self.on_draw_graph (None)

	def on_draw_graph (self, widget):
		if Test.Chart:
			mod, it = self.view.get_selection ().get_selected ()
			
			if it == None: return
			
			x = 0
			lst = [None,] * 13
			
			for i in range (13):
				if self.store.get_column_type (i + 3).pytype == gtk.gdk.Pixbuf:
					#print "image is %s" % mod.get_value (it, self.last + x)
					lst[i] = mod.get_value (it, self.last + x)
					x += 1
				else:
					lst[i] = mod.get_value (it, i + 3)
			
			self.grapher.plot (lst)
			
try:
	import matplotlib
	
	matplotlib.use ('GTKAgg')
	from matplotlib.figure import Figure
	from matplotlib.axes import Subplot
	from matplotlib.backends.backend_gtk import FigureCanvasGTK, NavigationToolbar
	from matplotlib.numerix import arange
	
except:
	Test.Chart = False
