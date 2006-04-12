class dummy:
	__name__ = "dummy plugin"
	__desc__ = "a dummy plugin"
	__ver__ = "0.0.1"
	__author__ = "PyAcqua team"

	def start (self):
		print ">> Starting ", self.__name__
	def stop (self):
		print "** Stopping ", self.__name__
