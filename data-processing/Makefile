# Written by Asheesh Laroia
# Assumes that there are 2425 pieces

7ZIP=/usr/bin/7za

TARGETS := $(patsubst %.chunk.7z,%.done,$(wildcard *.chunk.7z))

chunksizes := $(patsubst %.chunk.7z,%.chunk.size,$(wildcard *.chunk.7z))
sentences := $(patsubst %.chunk.7z,%.sentences.7z,$(wildcard *.chunk.7z))

*.done:

%.size: %.7z
	$(7ZIP) l $*.7z |  head -n9 | tail -n1  | awk '{print $$4}' > $*.size

chunk-total-size: $(chunksizes)
	cat $(chunksizes) | awk ' { sum += $$1 ; } END {print sum; } ' > chunk-total-size
	# FIXME: replace chunk-total-size with some variable

makefile-test: 
	-rm chunk-total-size
	make chunk-total-size

%.sentences.7z: %.paragraphs.7z
	~/dnet/run_on_machine.sh $*.paragraphs.7z " ~/bin/7za e  -so  /tmp/$*.paragraphs.7z | \
	( cd  ~/dnet/collab/code/ ; sh paragraphs2sentences.sh  file:///dev/stdin ) \
	| ~/bin/7za a -si /tmp/$*.sentences.7z ; scp /tmp/$*.sentences.7z paulproteus@fomalhaut.acm.jhu.edu:/mnt/paul/wikipedia-data/makefile-test/ ; \
	rm /tmp/$*.sentences.7z  "

all-paragraphs: $(paragraphs)

all-sentences: all-paragraphs $(sentences)

