#!/usr/bin/python

import sys
import re
try:
	import psyco
except:
	pass
import os

BUFSIZE = 40960
STARTTAG = '<page>'
ENDTAG = '</page>'
MINSIZE = 100 * 1024 * 1024
SEVENZIP = "7z"

# Method:
## Read in the input XML in 4096-byte chunks, incrementing *byte-count*
## always append the result to *growing-string*
## See if it contains </page>
## If it does, see if *byte-count* > 100M
## if so, then:
### increment *outfile-number*
### append the string up to and including ENDTAG to *growing-string*
### write *growing-string* to a file called *outfile-number*
### set *growing-string* to everything after ENDTAG

chunk = ''
growing_string = ''
outfile_number = 0

def sevenzip(s, filename):
	cmd = SEVENZIP + " -si a " + filename
	pipe = os.popen(cmd, 'w')
	pipe.write('<chunk>\n' + s + '</chunk>') # without this, the result isn't valid XML, I suppose
	pipe.close()

# filter out everything before the first STARTAG
# this assumes BUFSIZE is big enough to include the first STARTTAG
chunk = sys.stdin.read(BUFSIZE)
trash, chunk = chunk.split(STARTTAG, 1) # a left split
chunk = STARTTAG + chunk # STARTTAG removed by the split
growing_string += chunk

while chunk:
	if ENDTAG in chunk:
		if len(growing_string) > MINSIZE:
			outfile_number += 1
			# declare our intentions
			print 'Yay!  Writing file number', outfile_number
			# now we write
			start, end = chunk.rsplit(ENDTAG, 1) # a right split
			growing_string += start + ENDTAG # removed by the splitting operation
			sevenzip(growing_string, str(outfile_number)) # compress it and save it
			# now we initialize state for next hundred megs
			growing_string = end
	else:
		growing_string += chunk
	# in all cases
	chunk = sys.stdin.read(BUFSIZE)
	# because chunk is set last in this loop, and the next thing that happens is the while(),
	# we can be sure that every last byte gets processed.
