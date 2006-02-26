#!/bin/sh
if [ -f messages.pot ]; then
	if [ -f $1 ]; then
		echo "Il file $1 esiste gia'"
	else
		msginit -i messages.po -l $1
	fi
else
	echo "Prima esegui ./update-messages.sh"
fi
