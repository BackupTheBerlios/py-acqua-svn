#!/bin/sh
function unz {
	echo -e "\033[01;34m[\033[01;32m*\033[01;34m]\033[1;37m $1\033[00m"
}
unz "Cleaning the build/ directory..."
rm -rf build/
unz "Installing pyacqua to `pwd`/build/ ..."
python setup.py install --prefix=`pwd`/build > /dev/null
unz "Install complete. Now starting..."
PYTHONPATH="`pwd`/build/lib" ./build/bin/acqua.py
unz "PyAcqua exited."
