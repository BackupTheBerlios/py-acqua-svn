AXIS_USABLE_LIBS = GLIBC
include $(AXIS_TOP_DIR)/tools/build/Rules.axis

PROGS     = py
INSTDIR   = $(prefix)/mnt/flash/
INSTMODE  = 0755
INSTOWNER = root
INSTGROUP = root
OBJS      = py.o
OPTIONS   = -static

all: $(PROGS)

$(PROGS): $(OBJS)
	$(CXX)	$(OPTIONS)	$(LDFLAGS)	$^ $(LDLIBS)	-o	$@

install:	$(PROGS)
	$(INSTALL)	-d	$(INSTDIR)
	$(INSTALL)	-m	$(INSTMODE)	-o	$(INSTOWNER)	-g	$(INSTGROUP)	$(PROGS)	$(INSTDIR)
   
clean: 
	rm	-f	$(PROGS)	*.o core
