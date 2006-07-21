import os
from os.path import join, getsize
import md5

__rev__ = 1

class Generator (object):
	def checksum (path):
		fobj = file (path, 'rb')
		m = md5.new()

		while True:
			d = fobj.read(8096)
			if not d:
				break
			m.update(d)
		
		return m.hexdigest()
	checksum = staticmethod (checksum)

	def ParseDir (dir):
		stack = [dir]
		data = list ()

		while stack:
			dir = stack.pop ()
			for file in os.listdir (dir):
				fullname = os.path.join (dir, file)
				if not os.path.isdir (fullname):
					data.append (fullname[2:] + "|" + str (getsize (fullname)) + "|" + str (Generator.checksum (fullname)))
				elif not os.path.islink (fullname):
					if file != ".svn":
						stack.append (fullname)
		return data
	ParseDir = staticmethod (ParseDir)

if __name__ == "__main__":
	for i in Generator.ParseDir ("."):
		for x in i.split ("|"):
			print x,
		print
