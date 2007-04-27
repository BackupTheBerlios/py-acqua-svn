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

if [ -f ~/.pyacqua/program/share/src/acqua.py ]; then
	python ~/.pyacqua/program/share/pyacqua/src/acqua.py
else
	python $directory/share/pyacqua/src/acqua.py
fi
EOF

chmod +x build/bin/pyacqua

unz "Creating the list.xml for this revision.."
cd build/share/
python pyacqua/src/generate.py makelist
mv list.xml pyacqua/

unz "Install complete. Now starting..."

unz "PyAcqua exited."
