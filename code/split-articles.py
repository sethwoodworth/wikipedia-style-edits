#!/usr/bin/python

import sys
import re
try:
	import psyco
except:
	pass
import os

CHUNK_SIZE = 100 * 1024 * 1024 * 1024
STARTTAG = '<page>'
ENDTAG = '</page>'
SEVENZIP = "7z"

def sevenzip(s, filename):
	cmd = SEVENZIP + " -si a " + filename
	pipe = os.popen(cmd, 'w')
	pipe.write('<xml version="1.0" charset="utf-8">' + s + '</xml>') # without this, the result isn't valid XML, since it contains multiple top-level tags
	pipe.close()

NEXT_OUTFILE = 1 # This is the first filename we'll use.  We'll increment it.
LOOKS_USEFUL_YET = 0 # Set this to a true value when we've seen the first input
THIS_CHUNK = '' # This stores the chunk that we want to save, or at least might want to save later

for line in sys.stdin:
	# Once we've seen the STARTTAG, we know we're in business
	if LOOKS_USEFUL_YET or (STARTTAG in line):
		LOOKS_USEFUL_YET = 1
		THIS_CHUNK += line
		# Note that the iterator preserves the trailing '\n'.  That's so sweet of it.
		if len(THIS_CHUNK) > CHUNK_SIZE:
			# It's huge!
			# Q. Should we save it?
			if ENDTAG in line:
				# A. IFF ENDTAG in line
				# This works because ENDTAG is *always* on a line of its own.
				# This fact presumes things beyond the XML nature of the document,
				# and is as such dangerous.  Buyer beware!

				# declare our intentions
				print 'Yay!  Writing file number', outfile_number
				# now we write
				sevenzip(THIS_CHUNK, str(outfile_number)) # compress it and save it
				
				NEXT_OUTFILE += 1 # Sorta necessary :-)
				THIS_CHUNK = '' # Clear it!

# Now, we've stopped reading.
# The last <page> is probably still trapped inside THIS_CHUNK
# So let's solve this fencepost problem:

if ENDTAG in THIS_CHUNK:
	# Do a right-split to ignore trailing junk after </page>
	THIS_CHUNK = THIS_CHUNK.rsplit(ENDTAG, 1) + ENDTAG + '\n'

	# declare our intentions
	print 'Yay!  Writing final file, number', outfile_number
	# now we write
	sevenzip(THIS_CHUNK, str(outfile_number)) # compress it and save it
	THIS_CHUNK = '' # Clear it!

# Now I think the jig is up.
