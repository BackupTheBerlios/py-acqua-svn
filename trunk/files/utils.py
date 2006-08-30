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
import sys
from pysqlite2 import dbapi2 as sqlite
import re
import _winreg

HOME_DIR = None
PLUG_DIR = None
IMGS_DIR = None
DATA_DIR = None
UPDT_DIR = None
SKIN_DIR = None

# FIXME: prima della release
DHOME_DIR = os.getcwd()		# N.B. Questa nella release finale dovrebbe essere /usr/share/pyacqua
				# o robe simili
DPLUG_DIR = os.path.join (DHOME_DIR, "Plugin")
DDATA_DIR = os.path.join (DHOME_DIR, "Data")
DSKIN_DIR = os.path.join (DHOME_DIR, "Skin")
DPIXM_DIR = os.path.join (DHOME_DIR, "pixmaps")

def prepare_enviroment ():
	init_dir_structure ()

def tray_apri():#self, widget, data=None):
	import tray
	return tray.TrayIcon()

def init_dir_structure ():
	global HOME_DIR, PLUG_DIR, DATA_DIR, UPDT_DIR, SKIN_DIR, IMGS_DIR
	
	if os.name != "nt":
		path = os.environ["HOME"]
	else:
		hkey = _winreg.OpenKey (_winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders")
		path, type = _winreg.QueryValueEx (hkey, "AppData")

	print "Creating %s/.pyacqua" % path
	
	HOME_DIR = create_dir (path, ".pyacqua")
	
	path = os.path.join (path, ".pyacqua")
	
	IMGS_DIR = create_dir (path, "Immagini")
	PLUG_DIR = create_dir (path, "Plugin")
	DATA_DIR = create_dir (path, "Data")
	UPDT_DIR = create_dir (path, "Update")
	SKIN_DIR = create_dir (path, "Skins")

# FIXME: da controllare per eccezioni ecc.. dara' scazzi senza controllo
def create_dir (path, name):
	temp = os.path.join (path, name)
	
	if not os.path.exists (temp):
		os.mkdir (temp)
	else:
		print "Already present", temp
	
	return temp
###
# From http://www.decafbad.com/trac/browser/trunk/feedreactor/lib/jon/cgi.py
###
_url_encre = re.compile(r"[^A-Za-z0-9_./!~*()-]") # RFC 2396 section 2.3
_url_decre = re.compile(r"%([0-9A-Fa-f]{2})")

def url_encode(raw):
	"""Return the string parameter URL-encoded."""
	if not isinstance(raw, unicode):
		raw = str(raw)
	return re.sub(_url_encre, lambda m: "%%%02X" % ord(m.group(0)), raw)

def url_decode(enc):
	"""Return the string parameter URL-decoded (including '+' -> ' ')."""
	s = enc.replace("+", " ")
	return re.sub(_url_decre, lambda m: chr(int(m.group(1), 16)), s)

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
		
		
class TimeEntry(gtk.HBox):
	def __init__(self):
		gtk.HBox.__init__ (self, False, 2)

		self.spin_h = gtk.SpinButton (digits=0)
		self.spin_m = gtk.SpinButton (digits=0)

		self.spin_h.set_range (0, 23)
		self.spin_m.set_range (0, 59)
		
		self.spin_h.set_increments (1, 2)
		self.spin_m.set_increments (1, 2)

		self.spin_h.set_wrap (True)
		self.spin_m.set_wrap (True)
		
		self.pack_start (self.spin_h, False, False, 0)
		self.pack_start (self.spin_m, False, False, 0)

	def set_text(self, value):
		try:
			lst = value.split (':')
			self.spin_h.set_value (float (lst[0]))
			self.spin_m.set_value (float (lst[1]))
		except:
			pass
	
	def get_text(self):
		return str (self.spin_h.get_value_as_int()) + ":" + str (self.spin_m.get_value_as_int ())

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

class CheckedFloatEntry (gtk.HBox):
	def __init__ (self, min=0, max=9999, inc=0.1, page=1):
		gtk.HBox.__init__ (self, 0, False)
		
		self.check = gtk.CheckButton ()
		self.check.connect ('toggled', self.on_switch)
		
		self.float_entry = FloatEntry (min, max, inc, page)
		
		self.pack_start (self.check, False, False, 0)
		self.pack_start (self.float_entry, False, False, 0)
		
		self.check.set_active (True)
	
	def on_switch (self, widget):
		self.float_entry.set_sensitive (widget.get_active ())
		
	def set_text (self, value):
		self.float_entry.set_text (value)
		
		if value == None:
			self.check.set_active (False)
		else:
			self.check.set_active (True)
	
	def get_text (self):
		if self.check.get_active ():
			return self.float_entry.get_value ()
		else:
			return None

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

class Combo(gtk.ComboBox):
	def __init__(self, lst=None):
		liststore = gtk.ListStore(str)
		gtk.ComboBox.__init__(self, liststore)
		
		cell = gtk.CellRendererText()
		self.pack_start(cell, True)
		self.add_attribute(cell, 'text', 0)

		if lst != None:
			for i in lst: self.append_text (i)
		
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
class NoteEntry (gtk.Expander):
	def __init__(self, len=500):
		gtk.Expander.__init__(self, _("Mostra/Nascondi"))
		
		sw = gtk.ScrolledWindow ()
		sw.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type (gtk.SHADOW_ETCHED_IN)

		self.view = gtk.TextView ()
		self.view.set_wrap_mode (gtk.WRAP_WORD)
		self.view.get_buffer ().connect ('changed', self.on_changed)
		self.len = len

		sw.add (self.view)
		self.add (sw)

	def on_changed (self, buffer):
		if buffer.get_char_count() > self.len:
			buffer.set_text (buffer.get_text (buffer.get_start_iter (), buffer.get_end_iter ())[0:self.len])
	
	def get_text (self):
		buffer = self.view.get_buffer ()
		return buffer.get_text (buffer.get_start_iter (), buffer.get_end_iter ())
	
	def set_text (self, txt):
		self.view.get_buffer ().set_text (txt)

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
		self.set_size_request(300, 150)
	
	def run(self):
		id = gtk.Dialog.run(self)
		
		self.hide()
		self.destroy()
		
		return self.entry.get_text()

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

def msg (text, type=gtk.MESSAGE_WARNING, flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT, parent=None, buttons=gtk.BUTTONS_OK):
	d = gtk.MessageDialog (parent, flags, type, buttons, text)
	
	d.run ()
	d.hide (); d.destroy ()

def warning (text):
	msg (text)

def info (text):
	msg (text, gtk.MESSAGE_INFO)

def error (text):
	msg (text, gtk.MESSAGE_ERROR)

def new_label (txt, bold=True, x=0, y=0):
	lbl = gtk.Label ()
	
	if bold:
		lbl.set_use_markup (True)
		lbl.set_label ('<b>' + txt + '</b>')
		#lbl.set_alignment (0, 1.0)
		lbl.set_alignment (0, 0.5)
	else:
		lbl.set_label (txt)
		lbl.set_alignment (0.5, 0)
	
	if x != 0 and y != 0:
		lbl.set_alignment (x, y)
	
	return lbl

def new_button (txt, stock=None):
	button = gtk.Button ()
	hb = gtk.HBox (0, False)
	
	if stock:
		img = gtk.Image()
		img.set_from_stock (stock, gtk.ICON_SIZE_MENU)
		#img.set_size_request (8, 6)
		hb.add (img)
	hb.add (gtk.Label (txt))
	button.add (hb)
	
	return button

def set_icon (window):
	window.set_icon_from_file (os.path.join (DPIXM_DIR, "logopyacqua.jpg"))

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

def connect ():
	if os.path.exists (os.path.join (DATA_DIR, "db")):
		return sqlite.connect (os.path.join (DATA_DIR, "db"))
	else:
		raise Exception ("Cannot find the db in DATA_DIR")
	
def cmd (txt, *w):
	conn = connect ()
	cur = conn.cursor ()

	cur.execute (txt, w)

	conn.commit ()

def get (txt):
	conn = connect ()
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
			print _("Errore mentre copiavo (%s)") % sys.exc_value
	
	return os.path.basename (name)

def copy_plugin (name):
	plg_dir = os.path.join (os.path.abspath (os.getcwd ()), "Plugin")
	plg_dir = os.path.join (plg_dir, os.path.basename (name))
	
	if plg_dir != name:
		try:
			import shutil
			shutil.copy (name, 'Plugin/')
		except:
			print _("Errore mentre copiavo (%s)") % sys.exc_value

def create_skin (name, file):
	path = os.path.join (SKIN_DIR, name)

	if not os.path.exists (path):
		os.mkdir (path)

		pix = gtk.gdk.pixbuf_new_from_file (file)
		
		if pix.get_width () != 467 or pix.get_height () != 309:
			pix = pix.scale_simple (467, 309, gtk.gdk.INTERP_HYPER)
		
		pix.save (os.path.join (path, "main.png"), "png")

class InfoDialog (gtk.Dialog):
	def __init__ (self, parent, text, lbl_lst, lst, img=None):

		gtk.Dialog.__init__ (self, text, parent,
				gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_OK))
		
		assert len (lbl_lst) == len (lst)

		self.set_size_request (400, 300)
		self.vbox.set_border_width (10)

		self.set_has_separator (False)
		
		tbl = gtk.Table (len (lst), 2)
		tbl.set_border_width (4)

		if img != None:
			
			gimg = gtk.Image ()
			
			try:
				gimg.set_from_file (os.path.join ('Immagini', img))
			except:
				gimg.set_from_stock (gtk.STOCK_MISSING_IMAGE, gtk.ICON_SIZE_DIALOG)
			
			sw = gtk.ScrolledWindow ()
			sw.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			
			sw.add_with_viewport (gimg)
			self.vbox.pack_start (sw)

		attach = lambda t, x: tbl.attach (new_label (t), 0, 1, x, x+1)
		
		x = 0
		for i in lbl_lst:
			attach (i, x)
			x += 1

		attach = lambda t, x: tbl.attach (gtk.Label (t), 1, 2, x, x+1)

		x = 0
		for i in lst:
			attach (i.get_text (), x)
			x += 1

		self.vbox.pack_start (tbl, False, False, 0)
		self.show_all ()

		self.connect ('response', self.on_response)
	
	def on_response (self, dial, id):
		if id == gtk.RESPONSE_OK:
			self.hide ()
			self.destroy ()

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
		box.pack_start(TimeEntry())
		w.add(box)
		w.show_all()
	def a(self, w):
		print self.e.get_text()
		
if __name__ == "__main__":
	Test(0)
	#FileChooser("asd", None)
	gtk.main()
