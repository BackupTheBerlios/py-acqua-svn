AXIS_USABLE_LIBS = UCLIBC GLIBC
include $(AXIS_TOP_DIR)/tools/build/Rules.axis

CC = gcc-cris


OUTPUTFILE = py

OBJ=include/foxacqua_timer.o py.o

LFLAGS = -isystem ${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/include -mlinux -mno-mul-bug-workaround -Wall -Wshadow -O2 -c


all: $(OBJ)
	#$(CC) $(LFLAGS) py.c -o py.o 

#	$(CC) -isystem ${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/include -mlinux -mno-mul-bug-workaround -s -L${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/lib  py.o  -o $(OUTPUTFILE) $(OBJ)
#-L. -lsqlite

	$(CC) -isystem ${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/include -mlinux -mno-mul-bug-workaround -s -L${AXIS_TOP_DIR}/target/cris-axis-linux-gnu/lib -o $(OUTPUTFILE) $(OBJ)


run:
	./$(OUTPUTFILE)

clean:
	rm -rf $(OUTPUTFILE)
	rm -rf *.o
