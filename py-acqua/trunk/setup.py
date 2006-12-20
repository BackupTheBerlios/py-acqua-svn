#! /usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import glob
from distutils.core import setup

###
def moon_walk (root_dir, repl):
	packages, data_files = [], []
	
	for dirpath, dirnames, filenames in os.walk (root_dir):
		for i, dirname in enumerate (dirnames):
			if dirname.startswith('.'): del dirnames[i]
			data_files.append(("share/pyacqua/" + repl + dirpath[len(root_dir):], [os.path.join(dirpath, f) for f in filenames]))
	
	return data_files

if __name__ != "__main__":
	print moon_walk (sys.argv[1])
else:
	setup (
	name="py-acqua",
	version="1.0",
	description="PyAcqua program",
	author="Francesco Piccinno",
	author_email="stack.box@gmail.com",
	url="http://pyacqua.altervista.org",
	scripts=["src/acqua.py"],
	package_dir={'pyacqua': 'src'},
	packages=['pyacqua'],
	data_files=moon_walk ("skins", "skins") + [
		#("src", glob.glob ("src/*")),
		("share/pyacqua/plugins", glob.glob ("plugins/*.py")),
		("share/pyacqua/pixmaps", glob.glob ("pixmaps/*")),
		("share/pyacqua/tips", ["src/tip_of_the_day_en.txt", "src/tip_of_the_day.txt"])
	]
	)