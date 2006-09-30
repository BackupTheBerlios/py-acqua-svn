import os.path
import utils
import generate

def fill_fs_structure (path):
	lst = path.split (os.path.sep); lst.pop () # Eliminiamo la parte del file

	current = utils.UPDT_DIR

	for i in lst:
		current = os.path.join (current, i)

		print ">> Checking", current,
		
		if not os.path.exists (current):
			os.mkdir (current)
			print "created"

def rmgeneric(path, __func__):
	try:
		__func__(path)
		print '>> Removed ', path
	except OSError, (errno, strerror):
		print "!! Error while removing %s (%s)" % (path, strerror)
            
def removeall(path):
	if not os.path.isdir(path):
		return
	files=os.listdir(path)
	
	for x in files:
		fullpath=os.path.join(path, x)
		if os.path.isfile(fullpath):
			f=os.remove
			rmgeneric(fullpath, f)
		elif os.path.isdir(fullpath):
			removeall(fullpath)
			f=os.rmdir
			rmgeneric(fullpath, f)

def update ():
	path = os.path.join (utils.UPDT_DIR, ".checklist")
	
	if not os.path.exists (path):
		return
	
	file = open (path, 'r')
	list = file.readlines ()
	file.close ()

	for i in list:
		line = i[:-1]
		name, bytes, sum = line.split ("|")
		
		path = os.path.join (utils.UPDT_DIR, name)

		new_path = os.path.join (".", name)

		bytes = int (bytes)

		print ">> File", path

		if sum == '0':
			# Questo file deve essere zappato via.. via!
			print ">> Deleting", name, 

			if os.path.isfile (new_path):
				os.remove (new_path)
				print "file OK"
			elif os.path.isdir (new_path):
				os.rmdir (new_path)
				print "dir OK"
		else:
			# File da aggiornare.. controlla il checksum se corretto sposta
			new_sum = generate.Generator.checksum (path)

			if new_sum == sum:
				print ">> Sum is ok.. Moving ;)",
				if os.path.isfile (new_path):
					os.remove (new_path)
					print "file OK"
				elif os.path.isdir (new_path):
					os.rmdir (new_path)
					print "dir OK"

				fill_fs_structure (name)
				os.rename (path, new_path)			
			else:
				print "!! Error in checksum"
	
	print "Cleaning Update dir"
	removeall (utils.UPDT_DIR)

def check_for_updates ():
	if os.path.exists (os.path.join (utils.UPDT_DIR, ".checklist")):
		print ">> Proceding with update ()"
		update ()
	else:
		print ">> No files to merge"
