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
        for maybedel in self.lastlast, self.last:
            if maybedel is not None:
                os.unlink(maybedel)
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

class DiffParser:
    def __init__(self, s):
        ''' Takes some string s as input and parses it. '''
        self.hunks = [] # a list of (from, to) tuples
        # Has no built-in idea of distance, but does understand different hunks
        # self.hunks will be built in the order the lines appear in the diff

        # Hey, wait!  The first two lines of any diff are wasted on filename junk.
        lines = s.split('\n')
        assert(lines[0][:3] == '---')
        assert(lines[1][:3] == '+++')
        lines = lines[2:]
        self._parse(lines)
        
    def _parse(self, lines):
        this_hunk_from = []
        this_hunk_to = []
        for line in lines:
            if line:
                if line[0] == '+':
                    this_hunk_to.append(line[1:])
                elif line[0] == '-':
                    this_hunk_from.append(line[1:])
                else:
                    # we're out of a hunk; let's try to add the hunk we just made
                    if this_hunk_from or this_hunk_to:
                        self.hunks.append( (this_hunk_from, this_hunk_to) )
                        this_hunk_from = []
                        this_hunk_to = []
        # Look ma, no return!
        if this_hunk_from or this_hunk_to:
            self.hunks.append( (this_hunk_from, this_hunk_to) )
            this_hunk_from = []
            this_hunk_to = []
