import os
import commands
# This thing should

class Differ:
	''' This class is a little special-purpose.'''
	def __init__(self):
		self.last = None

	def _save(self, datum):
		""" Take datum as input.  Stash it away in a file somewhere. """
		filename = os.tempnam()
		fd = open(filename, 'w')
		fd.write(datum)
		fd.write('\n') # just in case
		fd.close()
		self.last = filename
		return filename

	def feed(self, thing):
		""" Feed me a string.  If you've ever fed me any strings before,
		then I'll return the diff *from* the one I used to have *to* the input
		thing. """
		last = self.last
		this = self._save(thing) # side-effect of updating self.last
		if last is None:
			return ''
		# Okay, so now we actually diff.
		return commands.getoutput('diff --text -u --minimal %s %s' % (last, this))
