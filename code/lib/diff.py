import os
import commands
# This thing should

class Differ:
    ''' This class is a little special-purpose.'''
    def __init__(self):
        self.last = None
        self.lastlast = None
        self.document_id = None # when this changes, we should reset ourselves

    def _save(self, datum):
        """ Take datum as input.  Stash it away in a file somewhere.
        Also delete the old 'last'. """
        filename = os.tempnam()
        fd = open(filename, 'w')
        fd.write(datum)
        fd.write('\n') # just in case
        fd.close()
        if self.lastlast is not None:
            os.unlink(self.lastlast)
        self.lastlast = self.last
        self.last = filename
        return filename

    def feed(self, document_id, thing):
        """ Feed me a string.  If you've ever fed me any strings before,
        then I'll return the diff *from* the one I used to have *to* the input
        thing. """
        if (self.document_id is None) or (document_id == self.document_id):
            # Good.  The diff is sane.
            # save the ID for later comparisons
            if self.document_id is None:
                self.document_id = document_id
            return self._diff(thing)
        else:
            self._newdoc(document_id)
            return self._diff(thing)

    def _newdoc(self, d_id):
        self.lastlast = None
        self.last = None
        self.document_id = d_id

    def _diff(self, thing):
        last = self.last
        this = self._save(thing) # side-effect of updating self.last
        if last is None:
            return ''
        # Okay, so now we actually diff.
        return commands.getoutput('diff --text -u --minimal %s %s' % (last, this))
