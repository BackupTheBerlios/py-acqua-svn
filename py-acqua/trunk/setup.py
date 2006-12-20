#! /usr/bin/env python
# -*- coding: utf8 -*-

import os
import glob
from distutils.core import setup

def moon_walk (root_dir):
	packages, data_files = [], []
	
	for dirpath, dirnames, filenames in os.walk (root_dir):
		for i, dirname in enumerate (dirnames):
			if dirname.startswith('.'): del dirnames[i]
			if '__init__.py' in filenames:
				package = dirpath[len_root_dir:].lstrip('/').replace('/', '.')
				packages.append(package)
			else:
				data_files.append((dirpath, [os.path.join(dirpath, f) for f in filenames]))
	
	return data_files


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
	data_files=moon_walk ("Skin") + [
		#("src", glob.glob ("src/*")),
		("Plugin", glob.glob ("Plugin/*.py")),
		("pixmaps", glob.glob ("pixmaps/*"))
	]
)
