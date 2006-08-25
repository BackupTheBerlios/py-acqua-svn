import files.utils as utils
import os.path
import files.generate as generate

def update ():
	#path = os.path.join (utils.UPDT_DIR, ".checklist")
	path = os.path.join ("/home/stack/.pyacqua/Update",  ".checklist")
	
	if not os.path.exists (path):
		return
	
	file = open (path, 'r')
	list = file.readlines ()
	file.close ()

	for i in list:
		line = i[:-1]
		name, bytes, sum = line.split ("|")
		
		#path = os.path.join (utils.UPDT_DIR, name)
		path = os.path.join ("/home/stack/.pyacqua/Update", name)

		new_path = os.path.join (".", name)

		bytes = int (bytes)

		print path, new_path

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
				print ">> Sum is ok.. Moving ;)"
				if os.path.isfile (new_path):
					os.remove (new_path)
					print "file OK"
				elif os.path.isdir (new_path):
					os.rmdir (new_path)
					print "dir OK"
				os.rename (path, new_path)				
			else:
				print "!! Error in checksum"

if __name__ == "__main__":
	update ()
