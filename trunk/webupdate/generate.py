import os
from os.path import join, getsize
import md5

__rev__ = 1

class Generator (object):
	def checksum (self, path):
		fobj = file (path, 'rb')
		m = md5.new()

		while True:
			d = fobj.read(8096)
			if not d:
				break
			m.update(d)
		
		return m.hexdigest()

	def ParseDir (self):
		dir = "/home/stack/pyacqua/trunk"
		os.chdir (dir)
		stack = ["."]

		while stack:
			dir = stack.pop ()
			for file in os.listdir (dir):
				fullname = os.path.join (dir, file)
				if not os.path.isdir (fullname):
					print fullname[2:] + "|" + str (getsize (fullname)) + "|" + str (self.checksum (fullname))
				elif not os.path.islink (fullname):
					if file != ".svn":
						stack.append (fullname)

if __name__ == "__main__":
	gen = Generator ()
	gen.ParseDir ()
