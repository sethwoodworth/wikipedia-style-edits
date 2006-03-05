import sys
# Based on http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/265881
from xml.sax.saxutils import XMLFilterBase

class text_normalize_filter(XMLFilterBase):
    """
    Takes an argument in text_filter: a function with two arguments.
    The first argument is the name of the WP page we're processing,
    and the second argument is the data in its <text> segment of a
    given revision.

    This is necessary to ensure stateful processing agents (like the
    revision differ) can differentiate between different WP pages.
    """
    
    def __init__(self, upstream, downstream, text_filter, manualOverride = False):
        XMLFilterBase.__init__(self, upstream)
        self._downstream = downstream
        self._accumulator = []
        self.text_filter = text_filter
        self.should_filter = False
        self.should_record_title = False
        self.title = None
	self.manualOverride = manualOverride # Set this to True if you want text_filter never to run
        return

    def _complete_text_node(self):
        if self._accumulator:
            text = ''.join(self._accumulator)
            if self.should_filter and not self.manualOverride:
                text = self.text_filter(self.title, text) # no stripping for me
            elif self.should_record_title:
                self.title = text
                #print >> sys.stderr, 'zomg', self.title
            self._downstream.characters(text)
            self._accumulator = []
        return

    def startElement(self, name, attrs):
        self._complete_text_node()
        if name == 'text':
            self.should_filter = True
        if name == 'title':
            self.should_record_title = True
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
        self.should_record_title = False
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

