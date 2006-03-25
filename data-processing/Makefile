# Written by Asheesh Laroia

# FIXME: Do something smarter and move these into place only if they're generated correctly, I guess

7ZIP=/usr/bin/7za

TARGETS := $(patsubst %.chunk.7z,%.done,$(wildcard *.chunk.7z))

chunksizes := $(patsubst %.chunk.7z,%.chunk.size,$(wildcard *.chunk.7z))
paragraphs := $(patsubst %.chunk.7z,%.paragraphs.7z,$(wildcard *.chunk.7z))
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

%.paragraphs.7z: %.chunk.7z
	~/dnet/run_on_machine.sh $*.chunk.7z " set -e ; ~/bin/7za e -so /tmp/$*.chunk.7z | \
	( set -e ; cd ~/dnet/collab/code/ ; nice python wikitext2paragraphs.py  file:///dev/stdin ) \
	| nice ~/bin/7za a -si /tmp/$*.paragraphs.7z && scp /tmp/$*.paragraphs.7z paulproteus@acm.jhu.edu:wikipedia-data/makefile-test/ ; \
	rm /tmp/$*.paragraphs.7z "

%.sentences.7z: %.paragraphs.7z
	~/dnet/run_on_machine.sh $*.paragraphs.7z " set -e ; ~/bin/7za e  -so  /tmp/$*.paragraphs.7z | \
	( set -e ; cd  ~/dnet/collab/code/ ; nice sh paragraphs2sentences.sh  file:///dev/stdin ) \
	| nice ~/bin/7za a -si /tmp/$*.sentences.7z && scp /tmp/$*.sentences.7z paulproteus@acm.jhu.edu:wikipedia-data/makefile-test/ ; \
	rm /tmp/$*.sentences.7z  "

all-paragraphs: $(paragraphs)

all-sentences: all-paragraphs $(sentences)

%.revision-index.csv: %.7z
	~/dnet/run_on_machine.sh $*.7z " set -e ; ~/bin/7za e -so /tmp/$*.7z | \
	python ~/dnet/collab/code/create_revision_index.py " > $*.revision-index.csv

%.title-index.csv: %.7z
	~/dnet/run_on_machine.sh $*.7z " set -e ; ~/bin/7za e -so /tmp/$*.7z | \
	python ~/dnet/collab/code/create_title_index.py " > $*.title-index.csv

%.diffedsentences.7z: %.sentences.7z
	~/dnet/run_on_machine.sh $*.sentences.7z " set -e ; ~/bin/7za e  -so  /tmp/$*.sentences.7z | \
	( set -e ; cd  ~/dnet/collab/code/ ; python sentences2diffs.py  file:///dev/stdin ) \
	| nice ~/bin/7za a -si /tmp/$*.diffedsentences.7z && scp /tmp/$*.diffedsentences.7z paulproteus@acm.jhu.edu:wikipedia-data/makefile-test/ ; \
	rm /tmp/$*.diffedsentences.7z  "

%.matchedsentences.7z: %.diffedsentences.7z
	~/dnet/run_on_machine.sh $*.diffedsentences.7z " set -e ; ~/bin/7za e  -so  /tmp/$*.diffedsentences.7z | \
	( set -e ; cd  ~/dnet/collab/code/ ; python diffs2matchedsentences.py  file:///dev/stdin ) \
	| nice ~/bin/7za a -si /tmp/$*.matchedsentences.7z && scp /tmp/$*.matchedsentences.7z paulproteus@acm.jhu.edu:wikipedia-data/makefile-test/ ; \
	rm /tmp/$*.matchedsentences.7z  "

