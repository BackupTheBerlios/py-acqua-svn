#!/bin/sh 
#clear
#. init_env
#cd apps
#cd py
make clean
make cris-axis-linux-gnu -Wall 
make
cris-strip --strip-unneeded py
#scp py root@192.168.1.90:/usr/local/bin
