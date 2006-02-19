# Setup.py
from distutils.core import setup
import py2exe
import glob

setup(
	name="PyAcqua",
	scripts["guy.py"],
	data_files[
		("pixmaps". glob.glob("pixmaps/*"))
	]
)
