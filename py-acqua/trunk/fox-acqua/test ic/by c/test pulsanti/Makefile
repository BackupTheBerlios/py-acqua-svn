#21/10/2007 - claudyus - Modifiche al makefile: le seguenti righe sono state aggiornate/
#
#CC = gcc-cris
#LFLAGS = -isystem ${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/include -mlinux -mno-mul-bug-workaround -Wall -Wshadow -O2
#$(CC) $(LFLAGS) py.c -o py.o 

#	$(CC) -isystem ${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/include -mlinux -mno-mul-bug-workaround -s -L${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/lib  py.o  -o $(OUTPUTFILE) $(OBJ)
#-L. -lsqlite
#
# Per compilare: 
# make cris-axis-linux-gnu; make


AXIS_USABLE_LIBS = UCLIBC GLIBC
include $(AXIS_TOP_DIR)/tools/build/Rules.axis

OUTPUTFILE = test
OBJ= include/ritardi.o include/foxacqua_i2c.o include/mcp230xx_sub.o include/funzioni.o  test.o
CFLAGS = -isystem ${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/include -mlinux -mno-mul-bug-workaround -Wall -Wshadow -O2 -g
LDFLAGS = -isystem ${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/include -mlinux -mno-mul-bug-workaround -s -L${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/lib

all: $(OBJ)
	$(CC) $(LDFLAGS) -o $(OUTPUTFILE) $(OBJ)


clean:
	rm -rf $(OUTPUTFILE)
	find . -name \*.o -exec rm -f {} \;
