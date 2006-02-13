#!/usr/bin/python
from lib.remove_wiki_markup import sub
from lib.text_normalize_filter import text_normalize_filter
from lib.pexpect import spawn
# Stage 1:

# Use SAX to write a program
# That echoes what input it gets.
# Stage 2:
# Not necessary.

# Stage 3: Make it remove wiki markup.
# Stage 3a: Make it de-wiki 

# Stage 4: Make it mxterminate the de-wiki-markup'd junk.

class opennlp_pipe:
	def __init__(self):
		""" These tokens came from pwgen -C | sed 's/ //g' """
		self.delimiter = 'bokohgepohkeebuuiecieweuboyiehivoosupuaxquahfeerowiequeeaeceimay'
		self.pipe = spawn('./lib/opennlp-wrap.sh', searchwindowsize=100,maxread= (2 * 1024 * 1024) )
		self.pipe.setecho(0)
		self.buffer = ''
	def handle(self, s):
		self.pipe.send(s + '\n\n')
		self.pipe.send('\n\n' + self.delimiter + '\n\n')
		self.pipe.expect(self.delimiter)
		return (self.pipe.before, self.pipe.after)


if __name__ == "__main__":
    sentence_splitter = opennlp_pipe()
    import sys
    from xml import sax
    from xml.sax.saxutils import XMLGenerator
    parser = sax.make_parser()
    #XMLGenerator is a special SAX handler that merely writes
    #SAX events back into an XML document
    downstream_handler = XMLGenerator(encoding='utf-8')
    #upstream, the parser, downstream, the next handler in the chain
    filter_handler = text_normalize_filter(parser, downstream_handler, sentence_splitter.handle)
    #The SAX filter base is designed so that the filter takes
    #on much of the interface of the parser itself, including the
    #"parse" method
    filter_handler.parse(sys.argv[1])
