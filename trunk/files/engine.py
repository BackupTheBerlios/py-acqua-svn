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
	def load (self, name):
		module = __import__ (name)
		print module
		#inst = vars(module)[name]
		#plug = inst ()
		
		#print plug.__name__
		#plug.start (); plug.stop ()

if __name__ == "__main__":
	e = Engine ()