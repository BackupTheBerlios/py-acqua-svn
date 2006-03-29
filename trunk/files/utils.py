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
import os
import os.path
from pysqlite2 import dbapi2 as sqlite

class DataButton(gtk.Button):
	def __init__(self, label=None, set_cb=None, get_cb=None):
		gtk.Button.__init__(self, label)
		self.set_relief(gtk.RELIEF_NONE)
		self.connect('clicked', self.on_change_date)
		self.cal = gtk.Calendar()
		
		self.set_cb = set_cb; self.get_cb = get_cb
		
		if label == None:
			self.update_label(self.cal.get_date())
			
	def update_label(self, date):
		self.set_label("%02d/%02d/%04d" % (date[2], date[1]+1, date[0]))
	
	def on_change_date(self, widget):
		d = gtk.Dialog(_("Seleziona una data"), None, gtk.DIALOG_MODAL,
		(gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
		d.vbox.pack_start(self.cal, False, False, 0)
		d.vbox.show_all()
		self.callback(d)
	
	def get_date(self):
		return self.cal.get_date()
	
	def get_text(self):
		if self.get_cb == None:
			date = self.cal.get_date()
			return "%02d/%02d/%02d" % (date[2], date[1]+1, date[0])
		else:
			return self.get_cb()
	def set_text(self, date):
		if self.set_cb == None:
			# Per adesso aggiustiamo solo la label senza controlli
			if date != None:
				self.set_label(date)
		else:
			self.set_cb(date)

	def callback(self, diag):
		id = diag.run()
		if id == gtk.RESPONSE_OK:
			self.update_label(self.get_date())
		diag.hide()
		diag.destroy()

class FloatEntry(gtk.SpinButton):
	def __init__(self, min=0, max=9999, inc=0.1, page=1):
		gtk.SpinButton.__init__(self, digits=2)
		self.set_range(min, max)
		self.set_increments(inc, page)
		self.set_wrap(True)
	
	def set_text(self, value):
		try:
			value = float(value)
		except:
			value = 0

		self.set_value(value)
	
	def get_text(self):
		return self.get_value()

class IntEntry(FloatEntry):
	def __init__(self):
		FloatEntry.__init__(self)
		self.set_digits(0)
		self.set_increments(1, 2)
		
	def set_text(self, value):
		try:
			value = int(value)
		except:
			value = 0
		self.set_value(value)
	
	def get_text(self):
		return self.get_value_as_int()

class ImgEntry (gtk.HBox):
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
		ret = FileChooser ("Selezione Immagine", None).run ()

		if ret != None:
			self.set_text(copy_image(ret))

class Combo(gtk.ComboBox):
	def __init__(self):
		liststore = gtk.ListStore(str)
		gtk.ComboBox.__init__(self, liststore)
		
		cell = gtk.CellRendererText()
		self.pack_start(cell, True)
		self.add_attribute(cell, 'text', 0)
		
	def get_text(self):
		it = self.get_active_iter()
		mod = self.get_model()

		if it != None: return str(mod.get_value(it, 0))
		else: return None
	def set_text(self, txt):
		mod = self.get_model()
		it = mod.get_iter_first()

		while it != None:
			if str(mod.get_value(it, 0)) == txt:
				self.set_active_iter(it)
				return
			it = mod.iter_next(it)

class InputDialog(gtk.MessageDialog):
	def __init__(self, parent, text):
		gtk.MessageDialog.__init__(self,
			parent,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			gtk.MESSAGE_QUESTION,
			gtk.BUTTONS_OK,
			text)
		
		self.entry = gtk.Entry()
		self.vbox.add(self.entry)
		self.entry.show()
		self.set_size_request(250, 150)
	
	def run(self):
		id = gtk.Dialog.run(self)
		
		self.hide()
		self.destroy()
		
		return self.entry.get_text()

class FileChooser(gtk.FileChooserDialog):
	def __init__(self, text, parent):
		gtk.FileChooserDialog.__init__(
			self,
			text,
			parent,
			buttons=(gtk.STOCK_OK, gtk.RESPONSE_OK,
			gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
		
		self.set_use_preview_label(False)

		img = gtk.Image()
		
		self.set_preview_widget(img)
		self.set_size_request(128, -1)

		# Creiamo i filtri

		filter = gtk.FileFilter()
		filter.set_name("Immagini")
		filter.add_mime_type("image/png")
		filter.add_mime_type("image/jpeg")
		filter.add_mime_type("image/gif")
		filter.add_pattern("*.png")
		filter.add_pattern("*.jpg")
		filter.add_pattern("*.gif")
		self.add_filter(filter)
		
		self.connect('update-preview', self.on_update_preview)
	
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

def new_label (txt, bold=True):
	lbl = gtk.Label ()
	
	if bold:
		lbl.set_use_markup (True)
		lbl.set_label ('<b>' + txt + '</b>')
		lbl.set_alignment (0, 1.0)
	else:
		lbl.set_label (txt)
		lbl.set_alignment (0.5, 0)
	
	return lbl

def make_thumb (twh, w, h):
	if w == h:
		return twh, twh
	if w < h:
		y = twh
		x = int (float (y * w) / float (h))
		return x, y
	if w > h:
		x = twh
		y = int (float (x * h) / float (w))
		return x, y

def cmd (txt, *w):
	conn = sqlite.connect (os.path.join ('Data', 'db'))
	cur = conn.cursor ()

	cur.execute (txt, w)

	conn.commit ()

def get (txt):
	conn = sqlite.connect (os.path.join ('Data', 'db'))
	cur = conn.cursor ()
	cur.execute (txt)

	return cur.fetchall()

def make_image (name):
	try:
		pixbuf = gtk.gdk.pixbuf_new_from_file (os.path.join ('Immagini', name))
		w, h = make_thumb (50, pixbuf.get_width (), pixbuf.get_height ())
		return pixbuf.scale_simple (w, h, gtk.gdk.INTERP_HYPER)
	except:
		return None

def copy_image (name):
	img_dir = os.path.join (os.path.abspath (os.getcwd ()), "Immagini")
	img_dir = os.path.join (img_dir, os.path.basename (name))
	
	if img_dir != name:
		try:
			import shutil
			shutil.copy (name, 'Immagini/')
		except:
			print "Errore mentre copiavo (%s)" % sys.exc_value
	
	return os.path.basename (name)

class Test:
	def __init__(self, i):
		w = gtk.Window()
		w.set_title("Testing")
		
		if i == 0:
			self.e = e = FloatEntry()
		else:
			self.e = e = IntEntry()
		box = gtk.VBox()
		box.pack_start(e)
		btn = gtk.Button('a')
		btn.connect('clicked', self.a)
		box.pack_start(btn)
		box.pack_start(ImgEntry())
		w.add(box)
		w.show_all()
	def a(self, w):
		print self.e.get_text()
		
if __name__ == "__main__":
	Test(0)
	#FileChooser("asd", None)
	gtk.main()
