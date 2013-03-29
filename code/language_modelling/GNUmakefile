NAME=tmPipe

MAKESHAREDLIB=False
# MAKESHAREDLIB=True


INCDIRS=-Ilibzutil/ -Ilibzstr/ $(EXTRA_INC_DIRS)
LIBDIRS=-Llibzutil/ -Llibzstr/ $(EXTRA_LIB_DIRS)
#INCDIRS=-I../util/libzutil/ -I../util/libzstr/ $(EXTRA_INC_DIRS)
#LIBDIRS=-L../util/libzutil/ -L../util/libzstr/ $(EXTRA_LIB_DIRS)
LIBS=-lzstr -lzutil -lJudy -lm

LIBPREFIX=lib
STATICLIBSUFFIX=.a
SHAREDLIBSUFFIX=.so

RANLIB=ranlib
AR=ar

DEBUGMODE=True
# DEBUGMODE=False

ifeq ($(DEBUGMODE),True)
CFLAGS=-Wall -O0
CFLAGS += -g
LDFLAGS += -g
else
CFLAGS=-Wall -O2
endif

CFLAGS += -fPIC -std=c99

CFLAGS += $(INCDIRS)
LDFLAGS += $(LIBDIRS) $(LIBS)

# SRCS=$(wildcard *.c)
SRCS=TrigramModel.c 
TMPIPESRCS=tmPipe.c
OBJS=$(SRCS:%.c=%.o)
TMPIPEOBJS=$(TMPIPESRCS:%.c=%.o)

TMPIPE=tmPipe
STATICLIB=$(LIBPREFIX)$(NAME)$(STATICLIBSUFFIX)
SHAREDLIB=$(LIBPREFIX)$(NAME)$(SHAREDLIBSUFFIX)


all: $(TMPIPE) 

./libzutil/libzutil.a: 
	cd libzutil && make libzutil.a

./libzstr/libzstr.a: libzutil/libzutil.a
	cd libzstr && make libzstr.a

staticlib: $(STATICLIB)

sharedlib: $(SHAREDLIB)

# .d auto-dependency files
ifneq ($(findstring clean,$(MAKECMDGOALS)),clean)
ifneq (,$(SRCS:%.c=%.d))
-include $(SRCS:%.c=%.d)
endif
endif

%.d: %.c
	@echo remaking $@
	@set -e; $(CC) $(CPPFLAGS) $(CFLAGS) -MM $< \
	| sed 's/\($*\)\.o[ :]*/\1.o $@ : GNUmakefile /g' > $@; \
	[ -s $@ ] || rm -f $@

$(STATICLIB): $(OBJS)
	$(AR) -r $@ $+
	$(RANLIB) $@

$(SHAREDLIB): $(OBJS)
	$(CC) -o $@ $+ -shared -fPIC

$(TMPIPE): $(TMPIPEOBJS) $(STATICLIB) libzstr/libzstr.a
	$(CC) $+ -o $@ $(LDFLAGS)

clean:
	-rm $(STATICLIB) $(SHAREDLIB) $(OBJS) $(TMPIPE) $(TMPIPEOBJS) *.d *.class 2>/dev/null

.PHONY: clean all staticlib sharedlib 
