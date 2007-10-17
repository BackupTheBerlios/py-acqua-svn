#   Makefile
#
#   Package Management for FoxBoard 
#   and FOXVHDL Board 
  
#   This file is part of fpkg.

#   Fpkg is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.

#   Fpkg is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

AXIS_USABLE_LIBS = UCLIBC GLIBC

include $(AXIS_TOP_DIR)/tools/build/Rules.axis

PROGS    = fpkg

OBJS     = common.o install.o remove.o fpkg.o update.o

INSTDIR = $(prefix)/usr/bin

all: $(PROGS)
$(PROGS): $(OBJS)
	$(CC) $(LDFLAGS) $^ $(LDLIBS) -o $@
	$(STRIP) $@

#install: $(PROGS)
#	$(INSTALL) -p -o root -g root -m 0777 $(PROGS) $(INSTDIR)

clean:
	rm -f $(PROGS) *.o core
