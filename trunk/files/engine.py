import os
import glob

class Plugin:
	__name__ = ""
	__desc__ = ""
	__ver__ = ""
	__author__ = ""
	
	def start (self):
		pass
	def stop (self):
		pass 

class PluginEngine:
	def __init__ (self):
		self.array = list () # Lista per contenere l'elenco di tutti i plugin
		self.load_defaults ()
	
	def load_defaults (self):
		# Carichiamo tutti i plugin presenti in Plugin/
		
		path = os.path.join(os.getcwd(), 'Plugin')
		
		for i in glob.glob(path + "/*.py"):
			if os.path.isfile(os.path.join(path, i)):
				file = os.path.join (path, i)
				base = os.path.basename(file)
				
				if base != "__init__.py":
					print _("Carico <%s>") % base[:-3]
					if self.load ("Plugin." + base[:-3], base[:-3]) == False:
						print _("Errori... Ignoro")
		
	def load (self, name, klass):
		try:
			module = __import__ (name, globals (), locals (), [klass])
			instance = vars(module)[klass]
			
			plugin = instance ()
			plugin.start ()
			
			self.array.append (plugin)
			
			return True
		except:
			return False

if __name__ == "__main__":
	e = Engine ()