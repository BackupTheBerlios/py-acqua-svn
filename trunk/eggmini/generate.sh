#!/bin/sh

rm trayicon.c

pygtk-codegen-2.0 --override trayicon.override --register /usr/share/pygtk/2.0/defs/gtk-types.defs --register /usr/share/pygtk/2.0/defs/gdk-types.defs --prefix pytrayicon trayicon.defs > trayicon.c
