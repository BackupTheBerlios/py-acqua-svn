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

class Test (dbwindow.DBWindow):
	PyChart = True
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
			float,	# NO
			float,	# NO2
			float,	# COND
			float,	# AMMO
			float,	# FERRO
			float,	# RAME
			float,	# FOSFATI
			float,	# calcio
			float,	# magnesio
			float)	# densita

		cols = [_('Id'), _('Data'), _('Vasca'), _('Ph'), _('Kh'), _('Gh'), _('No'), _('No2'),
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

		btn = gtk.Button (_("Grafico"))
		btn.connect ('clicked', self.on_draw_graph)
		btn.set_relief (gtk.RELIEF_NONE)

		self.button_box.pack_start (btn)

		self.show_all ()

	def  after_refresh (self, it):
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
	
	def on_draw_graph(self, widget):
		if not Test.PyChart:
			dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL,
				gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
				_("PyChart non installato.\nScaricalo da http://home.gna.org/pychart/"))
			
			dialog.run()
			dialog.hide()
			dialog.destroy()
			
		else:
			date = self.vars[0].get_text ()
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

			can = canvas.init(os.path.join('Immagini', 'grafico.png'))
			
			theme.use_color = 2
			theme.reinitialize()
			
			data = [
				[_('Ph'), ph], [_('Kh'), kh],
				[_('Gh'), gh], [_('No'), no],
				[_('No2'), no2], [_('Cond.'), cond],
				[_('Ammon.'), ammo], [_('Ferro'), ferro],
				[_('Rame'), rame], [_('Fosf.'), fosfati],
				[_('Calcio'), calcio], [_('Magnes.'), magnesio],
				[_('Densità'), densita]
				]
			ar = area.T(x_coord = category_coord.T(data, 0),
				y_range = (0, None),
				size = (400, 250),

				x_axis = axis.X(label=_('Test')),
				y_axis = axis.Y(label=_('Valori')))
			ar.add_plot(bar_plot.T(data = data, label = _("Legenda")))
			ar.draw(can)
			can.close()

			# InfoDialog
			d = gtk.MessageDialog(self, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK)
			d.set_markup(_("<span size=\"large\"><b>PyAcqua Graph</b></span>\n\n<b>Tipo Vasca:</b> %s\n<b>Data:</b> %s") % (vasca, date))
			
			img = gtk.Image(); img.set_from_file(os.path.join('Immagini', 'grafico.png'))
			
			sw = gtk.ScrolledWindow()
			sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			#sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
			
			sw.add_with_viewport(img)
			
			d.vbox.pack_start(sw)
			d.vbox.show_all()
			d.set_border_width(4)
			
			d.set_size_request(600, 450)
			
			d.run()
			d.hide(); d.destroy()
			
			if os.path.isfile(os.path.join('Immagini', 'grafico.png')):
				os.remove(os.path.join('Immagini', 'grafico.png'))

try:
	from pychart import *
except:
	Test.PyChart = False
