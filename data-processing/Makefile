# Written by Asheesh Laroia
# Assumes that there are 2425 pieces

7ZIP=/usr/bin/7za


TARGETS := $(patsubst %.chunk.7z,%.done,$(wildcard *.chunk.7z))

*.done:

%.size: %.7z
	$(7ZIP) l $*.7z |  head -n9 | tail -n1  | awk '{print $$4}' > $*.size

chunk-total-size: $(chunksizes)
	cat $(chunksizes) | awk ' { sum += $$1 ; } END {print sum; } ' > total-size
