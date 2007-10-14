AXIS_USABLE_LIBS = UCLIBC GLIBC
include $(AXIS_TOP_DIR)/tools/build/Rules.axis

CC = gcc-cris


OUTPUTFILE = py


LFLAGS = -isystem ${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/include -mlinux -mno-mul-bug-workaround -Wall -Wshadow -O2 -c


all:
	$(CC) $(LFLAGS) py.c -o py.o

	$(CC) -isystem ${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/include -mlinux -mno-mul-bug-workaround -s -L${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/lib  py.o  -o $(OUTPUTFILE) 
#-L. -lsqlite

run:
	./$(OUTPUTFILE)

clean:
	rm -rf $(OUTPUTFILE)
	rm -rf *.o
