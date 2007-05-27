#!/bin/sh 
. init_env
cd apps
cd py
make clean
make cris-axis-linux-gnu
make
cris-strip --strip-unneeded py
scp py root@192.168.0.90:/mnt/flash
(sleep 3; echo root; sleep 3; echo pass; \
   sleep 1;echo cd ..; echo sleep 1;echo cd mnt/flash; sleep 1; echo chmod +x py; sleep 1; echo ./py  ) | telnet 192.168.0.90





