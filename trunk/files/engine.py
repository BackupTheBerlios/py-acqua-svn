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
		#self.load ("asd")
		pass
	def load (self, name, klass):
		module = __import__ (name, globals (), locals (), [klass])
		instance = vars(module)[klass]
		
		plugin = instance ()
		
		plugin.start ()
		print "Plugin '%s' caricato" % plugin.__name__
		
		plugin.stop ()
		print "Plugin '%s' fermato" % plugin.__name__

if __name__ == "__main__":
	e = Engine ()