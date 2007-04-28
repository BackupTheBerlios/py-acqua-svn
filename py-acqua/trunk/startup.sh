#!/bin/sh
function unz {
        echo -e "\033[01;34m[\033[01;32m*\033[01;34m]\033[1;37m $1\033[00m"
}

if [ "$1" == "" ]; then
	directory="`pwd`/build"
else
	directory="$0"
fi

unz "Cleaning up for backup file (~)"
. scripts/clean.sh

unz "Cleaning the build/ directory..."
rm -rf build/

unz "Installing pyacqua to `pwd`/build/ ..."

mkdir -p build/share/pyacqua
mkdir -p build/bin

cp -rf src build/share/pyacqua
cp -rf pixmaps build/share/pyacqua
cp -rf tips build/share/pyacqua
cp -rf skins build/share/pyacqua
cp -rf plugins build/share/pyacqua
cp -rf locale build/share

unz "Creating the bash wrapper with the name of bin/pyacqua"
cat > build/bin/pyacqua << EOF
#!/bin/sh

function unz {
        echo -e "\033[01;34m[\033[01;32m*\033[01;34m]\033[1;37m \$1\033[00m"
}

if [ -f ~/.pyacqua/program/share/src/acqua.py ]; then
	unz "PyAcqua is already installed in home directory. Launching from ~/.pyacqua/program/share/pyacqua"
	python ~/.pyacqua/program/share/pyacqua/src/acqua.py
else
	unz "Making dir structure..."
	mkdir -p ~/.pyacqua/program/share/locale/en/LC_MESSAGES/
	unz "Copyng the program..."
	cp $directory/share/pyacqua ~/.pyacqua/program/share -rf
	unz "Copying the locale dir..."
	cp $directory/share/locale/en/LC_MESSAGES/acqua.mo ~/.pyacqua/program/share/locale/en/LC_MESSAGES/

	unz "Ok. Now we are going to launch pyacqua from home directory..."
	unz "Good work pyacqua-user ;)"

	python ~/.pyacqua/program/share/pyacqua/src/acqua.py

	unz "Are you ok? .. Really? .. No crash? No explosion? .. mhh very strange.."
	unz "Hei \$USER! Remember to visit our site at http://www.pyacqua.net"
fi
EOF

chmod +x build/bin/pyacqua

unz "Creating the list.xml for this revision.."
cd build/share/
python pyacqua/src/generate.py makelist
mv list.xml pyacqua/

unz "Install complete. Now starting..."

unz "PyAcqua exited."
