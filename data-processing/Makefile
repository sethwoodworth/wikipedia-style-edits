# Written by Asheesh Laroia

# FIXME: Do something smarter and move these into place only if they're generated correctly, I guess
## Strategy: Suffix many operations with "|| rm /tmp/whatever"

7ZIP=/usr/bin/7za

.PHONY : chunksizes paragraphs sentences all-paragraphs all-sentences all-whitespacenormalizedsentences all-diffedsentences all-matchedsentences all-styleedits all-content-edits all-styleedits-sans-typofixes

TARGETS := $(patsubst %.chunk.7z,%.done,$(wildcard *.chunk.7z))

chunksizes := $(patsubst %.chunk.7z,%.chunk.size,$(wildcard *.chunk.7z))
paragraphs := $(patsubst %.chunk.7z,%.paragraphs.7z,$(wildcard *.chunk.7z))
sentences := $(patsubst %.chunk.7z,%.sentences.7z,$(wildcard *.chunk.7z))
whitespacenormalizedsentences := $(patsubst %.chunk.7z,%.whitespacenormalizedsentences.7z,$(wildcard *.chunk.7z))
diffedsentences := $(patsubst %.chunk.7z,%.diffedsentences.7z,$(wildcard *.chunk.7z))
matchedsentences := $(patsubst %.chunk.7z,%.matchedsentences.7z,$(wildcard *.chunk.7z))
styleedits := $(patsubst %.chunk.7z,%.styleedits.7z,$(wildcard *.chunk.7z))
content-edits := $(patsubst %.chunk.7z,%.content-edits.7z,$(wildcard *.chunk.7z))
styleedits-sans-typofixes := $(patsubst %.chunk.7z,%.styleedits-sans-typofixes.7z,$(wildcard *.chunk.7z))

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
	( set -e ; cd ~/dnet/collab/code/ ; nice ~/bin/python wikitext2paragraphs.py  file:///dev/stdin ) \
	| nice ~/bin/7za a -si /tmp/$*.paragraphs.7z && scp /tmp/$*.paragraphs.7z paulproteus@acm.jhu.edu:wikipedia-data/makefile-test/ ; \
	rm /tmp/$*.paragraphs.7z "

%.sentences.7z: %.paragraphs.7z
	~/dnet/run_on_machine.sh $*.paragraphs.7z " set -e ; ~/bin/7za e  -so  /tmp/$*.paragraphs.7z | \
	( set -e ; cd  ~/dnet/collab/code/ ; nice sh paragraphs2sentences.sh  file:///dev/stdin ) \
	| nice ~/bin/7za a -si /tmp/$*.sentences.7z && scp /tmp/$*.sentences.7z paulproteus@acm.jhu.edu:wikipedia-data/makefile-test/ ; \
	rm /tmp/$*.sentences.7z  "

%.whitespacenormalizedsentences.7z: %.sentences.7z
	~/dnet/run_on_machine.sh $*.sentences.7z " set -e ; ~/bin/7za e  -so  /tmp/$*.sentences.7z | \
	( set -e ; cd  ~/dnet/collab/code/ ; nice ~/bin/python sentences2whitespacenormalized.py  file:///dev/stdin ) \
	| nice ~/bin/7za a -si /tmp/$*.whitespacenormalizedsentences.7z && scp /tmp/$*.whitespacenormalizedsentences.7z paulproteus@acm.jhu.edu:wikipedia-data/makefile-test/ ; \
	rm /tmp/$*.whitespacenormalizedsentences.7z  "

all-paragraphs: $(paragraphs)

all-sentences: $(sentences)

all-whitespacenormalizedsentences: $(whitespacenormalizedsentences)

all-diffedsentences: $(diffedsentences)

all-matchedsentences: $(matchedsentences)

all-styleedits: $(styleedits)
all-content-edits: $(content-edits)
all-styleedits-sans-typofixes: $(styleedits-sans-typofixes)

%.revision-index.csv: %.7z
	~/dnet/run_on_machine.sh $*.7z " set -e ; ~/bin/7za e -so /tmp/$*.7z | \
	~/bin/python ~/dnet/collab/code/create_revision_index.py " > $*.revision-index.csv

%.title-index.csv: %.7z
	~/dnet/run_on_machine.sh $*.7z " set -e ; ~/bin/7za e -so /tmp/$*.7z | \
	~/bin/python ~/dnet/collab/code/create_title_index.py " > $*.title-index.csv

%.diffedsentences.7z: %.whitespacenormalizedsentences.7z
	~/dnet/run_on_machine.sh $*.whitespacenormalizedsentences.7z " set -e ; ~/bin/7za e  -so  /tmp/$*.whitespacenormalizedsentences.7z | \
	( set -e ; cd  ~/dnet/collab/code/ ; nice ~/bin/python sentences2diffs.py  file:///dev/stdin ) \
	| nice ~/bin/7za a -si /tmp/$*.diffedsentences.7z && scp /tmp/$*.diffedsentences.7z paulproteus@acm.jhu.edu:wikipedia-data/makefile-test/ ; \
	rm /tmp/$*.diffedsentences.7z  "

%.matchedsentences.7z: %.diffedsentences.7z
	~/dnet/run_on_machine.sh $*.diffedsentences.7z " set -e ; ~/bin/7za e  -so  /tmp/$*.diffedsentences.7z | \
	( set -e ; cd  ~/dnet/collab/code/ ; nice ~/bin/python diffs2matchedsentences.py  file:///dev/stdin ) \
	| nice ~/bin/7za a -si /tmp/$*.matchedsentences.7z && scp /tmp/$*.matchedsentences.7z paulproteus@acm.jhu.edu:wikipedia-data/makefile-test/ ; \
	rm /tmp/$*.matchedsentences.7z  "

%.styleedits.7z: %.matchedsentences.7z
	~/dnet/run_on_machine.sh $*.matchedsentences.7z " set -e ; ~/bin/7za e  -so  /tmp/$*.matchedsentences.7z | \
	( set -e ; cd  ~/dnet/collab/code/ ; nice ~/bin/python matches2styleedits.py  file:///dev/stdin ) \
	| nice ~/bin/7za a -si /tmp/$*.styleedits.7z && scp /tmp/$*.styleedits.7z paulproteus@acm.jhu.edu:wikipedia-data/makefile-test/ ; \
	rm /tmp/$*.styleedits.7z  "

%.content-edits.7z: %.matchedsentences.7z
	~/dnet/run_on_machine.sh $*.matchedsentences.7z " set -e ; ~/bin/7za e  -so  /tmp/$*.matchedsentences.7z | \
	( set -e ; cd  ~/dnet/collab/code/ ; nice ~/bin/python matches2content-edits.py  file:///dev/stdin ) \
	| nice ~/bin/7za a -si /tmp/$*.content-edits.7z && scp /tmp/$*.content-edits.7z paulproteus@acm.jhu.edu:wikipedia-data/makefile-test/ ; \
	rm /tmp/$*.content-edits.7z  "

%.styleedits-sans-typofixes.7z: %.styleedits.7z
	~/dnet/run_on_machine.sh $*.styleedits.7z " set -e ; ~/bin/7za e  -so  /tmp/$*.styleedits.7z | \
	( set -e ; cd  ~/dnet/collab/code/ ; nice ~/bin/python styleedits2sans-typos.py  file:///dev/stdin ) \
	| nice ~/bin/7za a -si /tmp/$*.styleedits-sans-typofixes.7z && scp /tmp/$*.styleedits-sans-typofixes.7z paulproteus@acm.jhu.edu:wikipedia-data/makefile-test/ ; \
	rm /tmp/$*.styleedits-sans-typofixes.7z  "

