#!/usr/bin/python

import sys
import re
try:
	import psyco
except:
	pass
import os

CHUNK_SIZE = 100 * 1024 * 1024
STARTTAG = '<page>'
ENDTAG = '</page>'
SEVENZIP = "7za"

class sevenpipe:
	def __init__(self):
		self.so_far = 0
		self.filename = str(NEXT_OUTFILE)
		if NEXT_OUTFILE > 1606: # already did <= 1606
			cmd = SEVENZIP + " -si a " + self.filename
		else: # do a no-op for the ones we don't care about
			cmd = 'cat > /dev/null'
		self.pipe = os.popen(cmd, 'w')
		print "Created self:", self.filename
		self.pipe.write('<xml version="1.0" charset="utf-8">\n')
		self.buffer = []
		self.flush()

	def flush(self):
		for thing in self.buffer:
			self.pipe.write(thing)
		self.buffered_now = 0
		self.buffer = []

	def write(self, s):
		self.buffer.append(s)
		self.buffered_now += len(s)
		if self.buffered_now > 4096000: # 4000K buffer for no particular reason
			self.flush()
			print 'flushed at', self.so_far

		self.so_far += len(s)

	def close(self):
		self.flush()
		self.pipe.write("</xml>")
		self.pipe.close()
		global NEXT_OUTFILE
		NEXT_OUTFILE += 1

NEXT_OUTFILE = 1 # This is the first filename we'll use.  We'll increment it.
LOOKS_USEFUL_YET = 0 # Set this to a true value when we've seen the first input
THIS_CHUNK = sevenpipe() # This stores the chunk that we want to save, or at least might want to save later

for line in sys.stdin:
	# Once we've seen the STARTTAG, we know we're in business
	if LOOKS_USEFUL_YET or (STARTTAG in line):
		LOOKS_USEFUL_YET = 1
		if not '</mediawiki>' in line:
			THIS_CHUNK.write(line)
		# Note that the iterator preserves the trailing '\n'.  That's so sweet of it.
		if THIS_CHUNK.so_far > CHUNK_SIZE or '</mediawiki>' in line:
			# It's huge!
			# Q. Should we save it?
			if ENDTAG in line:
				# A. IFF ENDTAG in line
				# This works because ENDTAG is *always* on a line of its own.
				# This fact presumes things beyond the XML nature of the document,
				# and is as such dangerous.  Buyer beware!

				# declare our intentions
				print 'Yay!  Writing file number', NEXT_OUTFILE
				# now we write
				THIS_CHUNK.close() # compress it and save it
				
				THIS_CHUNK = sevenpipe() # Clear it!

# Now I think the jig is up.
