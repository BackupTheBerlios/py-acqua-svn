#!/bin/bash
function unz {
        echo -e "\033[01;34m[\033[01;32m*\033[01;34m]\033[1;37m $1\033[00m"
}

function sbrah {
	echo -e "\033[01;32mo.O\033[1;37m $1\033[00m"
}

directory="$1"

if [ "$1" == "" ]; then
	echo
	sbrah  " ___        _"
	sbrah  "| _ \_  _  /_\  __ __ _ _  _ __ _"
	sbrah  "|  _/ || |/ _ \/ _/ _\` | || / _\` |"
	sbrah  "|_|  \_, /_/ \_\__\__, |\_,_\__,_|"
	sbrah  "     |__/            |_|"
	echo
	sbrah "ei you! probably you are trying to install pyacqua on your box."
       	sbrah "I'm sorry, but the task is not so simple. So you must read carefully"
	sbrah "this warning before proceeding :D"
	sbrah 
       	sbrah "In order to install py-acqua you must type as root"
	sbrah "# ./startup.sh /usr - in order to install pyacqua in /usr"
        sbrah "or"
	sbrah "# ./startup.sh /usr/local - in order to install pyacqua in /usr/local"
	sbrah 
       	sbrah "mhh..remember! For bugs, insults, porn-photos we have a mail: "
        sbrah "info@pyacqua.net and also a site http://www.pyacqua.net"
	sbrah
	sbrah "ok it's all. Good luck \$USER ;-)"

	echo
	sbrah "No animals were harmed during the making of this release."
	echo

	exit 
fi

unz "Cleaning up for backup file (~)"
. scripts/clean.sh

if [ "$1" == "makeupdate" ]; then
	# Creiamo la directory per l'update da piazzare sul sito

	unz "Cleaning the build-update/ directory..."
	rm -rf build-update/

	mkdir -p build-update/source/pyacqua

	cp -rf src build-update/source/pyacqua
	cp -rf pixmaps build-update/source/pyacqua
	cp -rf tips build-update/source/pyacqua
	cp -rf skins build-update/source/pyacqua
	cp -rf plugins build-update/source/pyacqua
	cp -rf locale build-update/source/
	
	unz "Creating the source-list.xml for this revision.."
	cd build-update/source/
	python pyacqua/src/generate.py makelist
	mv list.xml ../source-list.xml

	unz "Now you can put the build-update directory under your site with the name update"
else
	unz "Installing pyacqua to $directory ..."

	mkdir -p $directory/share/pyacqua
	mkdir -p $directory/bin

	cp -rf src $directory/share/pyacqua
	cp -rf pixmaps $directory/share/pyacqua
	cp -rf tips $directory/share/pyacqua
	cp -rf skins $directory/share/pyacqua
	cp -rf plugins $directory/share/pyacqua
	cp -rf locale $directory/share

	unz "Creating the bash wrapper with the name of bin/pyacqua"
	cat > $directory/bin/pyacqua << EOF
#!/bin/sh

function unz {
        echo -e "\033[01;34m[\033[01;32m*\033[01;34m]\033[1;37m \$1\033[00m"
}

if [ -f ~/.pyacqua/program/pyacqua/src/acqua.py ]; then
	unz "PyAcqua is already installed in home directory. Launching from ~/.pyacqua/program/share/pyacqua"
	
	cd ~/.pyacqua/program/pyacqua/

	if [ -f ~/.pyacqua/update/.diff.xml ]; then
		unz "Try to merge update..."
		python src/merger.py
	fi
	
	python src/acqua.py
else
	unz "Making dir structure..."
	mkdir -p ~/.pyacqua/program/locale/en/LC_MESSAGES/

	unz "Copyng the program..."
	cp $directory/share/pyacqua ~/.pyacqua/program/ -rf

	unz "Copying the locale dir..."
	cp $directory/share/locale/en/LC_MESSAGES/acqua.mo ~/.pyacqua/program/locale/en/LC_MESSAGES/

	unz "Ok. Now we are going to launch pyacqua from home directory..."
	unz "Good work pyacqua-user ;)"

	cd ~/.pyacqua/program/pyacqua/
	python src/acqua.py

	unz "Are you ok? .. Really? .. No crash? No explosion? .. mhh very strange.."
	unz "Hei \$USER! Remember to visit our site at http://www.pyacqua.net"
fi
EOF

	chmod +x $directory/bin/pyacqua

	unz "Creating the list.xml for this revision.."
	cd $directory/share/
	python pyacqua/src/generate.py makelist
	mv list.xml pyacqua/

	unz "Deleting .svn directories"
	cd ../
	for f in `find -name .svn -type d`; do rm -rf $f; done
fi
