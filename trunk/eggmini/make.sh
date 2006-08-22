#!/bin/sh

rm -f *.so *.o
rm trayicon.c

pygtk-codegen-2.0 --override trayicon.override --register /usr/share/pygtk/2.0/defs/gtk-types.defs --register /usr/share/pygtk/2.0/defs/gdk-types.defs --prefix pytrayicon trayicon.defs > trayicon.c

gcc -c -fPIC `pkg-config --cflags gtk+-2.0 pygtk-2.0` -I/usr/include/python2.4 eggtrayicon.c
gcc -c -fPIC `pkg-config --cflags gtk+-2.0 pygtk-2.0` -I/usr/include/python2.4 trayicon.c
gcc -c -fPIC `pkg-config --cflags gtk+-2.0 pygtk-2.0` -I/usr/include/python2.4 trayiconmodule.c
gcc -shared -o trayicon.so -fPIC eggtrayicon.o trayicon.o trayiconmodule.o `pkg-config --libs gtk+-2.0`

# all'ultimo va linkato alle gtk
