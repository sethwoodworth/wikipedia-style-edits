#!/usr/bin/python
import remove_wiki_markup
# Stage 1:

# Use SAX to write a program
# That echoes what input it gets.
# Based on http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/265881
# Stage 2:
# Not necessary.

# Stage 3: Make it remove wiki markup.
# Stage 3a: Make it de-wiki 

# Stage 4: Make it mxterminate the de-wiki-markup'd junk.

from xml.sax.saxutils import XMLFilterBase

class text_normalize_filter(XMLFilterBase):
    """
    SAX filter to ensure that contiguous white space nodes are
    delivered merged into a single node
    """
    
    def __init__(self, upstream, downstream, text_filter):
        XMLFilterBase.__init__(self, upstream)
        self._downstream = downstream
        self._accumulator = []
        self.text_filter = text_filter
        self.should_filter = False
        return

    def _complete_text_node(self):
        if self._accumulator:
            text = ''.join(self._accumulator)
            if self.should_filter:
                text = self.text_filter(text).strip()
            self._downstream.characters(text)
            self._accumulator = []
        return

    def startElement(self, name, attrs):
        self._complete_text_node()
        if name == 'text':
            self.should_filter = True
        self._downstream.startElement(name, attrs)
        return

    def startElementNS(self, name, qname, attrs):
        self._complete_text_node()
        self._downstream.startElementNS(name, qname, attrs)
        return

    def endElement(self, name):
        self._complete_text_node()
        self._downstream.endElement(name)
        self.should_filter = False
        return

    def endElementNS(self, name, qname):
        self._complete_text_node()
        self._downstream.endElementNS(name, qname)
        return

    def processingInstruction(self, target, body):
        self._complete_text_node()
        self._downstream.processingInstruction(target, body)
        return

    def comment(self, body):
        self._complete_text_node()
        self._downstream.comment(body)
        return

    def characters(self, text):
        self._accumulator.append(text)
        return

    def ignorableWhitespace(self, ws):
        self._accumulator.append(text)
        return


if __name__ == "__main__":
    import sys
    from xml import sax
    from xml.sax.saxutils import XMLGenerator
    parser = sax.make_parser()
    #XMLGenerator is a special SAX handler that merely writes
    #SAX events back into an XML document
    downstream_handler = XMLGenerator(encoding='utf-8')
    #upstream, the parser, downstream, the next handler in the chain
    filter_handler = text_normalize_filter(parser, downstream_handler, remove_wiki_markup.sub)
    #The SAX filter base is designed so that the filter takes
    #on much of the interface of the parser itself, including the
    #"parse" method
    filter_handler.parse(sys.argv[1])
