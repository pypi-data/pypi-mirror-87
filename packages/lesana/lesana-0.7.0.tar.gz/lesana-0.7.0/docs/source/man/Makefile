
MAN_TARGETS = $(patsubst %.rst,%.1,$(wildcard *.rst))

all: $(MAN_TARGETS)

%.1: %.rst
	rst2man $< > $@

clean:
	rm *.1

.PHONY: all clean
