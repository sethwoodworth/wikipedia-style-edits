# From www.sims.berkeley.edu:8000/courses/.../lecture3.ppt
import commands
import tempfile
import sys
import os
import string
#import nltk.token
#import nltk.tokenizer
url = r'((http:\/\/)?[A-Za-z]+(\.[A-Za-z]+){1,3}(\/)?(:\d+)?)'
hyphen = r'(\w+\-\s?\w+)'
apostro = r'(\w+\'\w+)'
numbers = r'((\$|#)?\d+(\.)?\d+%?)'
punct = r'([^\w\s]+)'
wordr = r'(\w+)'
regexp = '|'.join([url, hyphen, apostro, numbers, wordr, punct])
#RT = nltk.tokenizer.RegexpTokenizer(regexp, SUBTOKENS='WORDS')

def nltk_tokenize(u):
    if type(u) == type(''):
        u = unicode(u)
    assert(type(u) == type(u''))
    s = u.encode('utf-8') # sad
    t = nltk.token.Token(TEXT=s)
    fromRT = RT.tokenize(t)
    words = t['WORDS']
    ret = []
    for thing in words:
        ret.extend(thing.values())
    return ret

import tempfile
import os
import commands
def treebank_tmpfile_sed(s):
    fname = tempfile.mktemp()
    fd = open(fname, 'w')
    fd.write(s.encode('utf-8'))
    fd.close()
    sedded = commands.getoutput('sed -f tokenizer.sed < ' + fname)
    u = unicode(sedded, 'utf-8')
    ret = u.split()
    os.unlink(fname)
    return ret

import pexpect
class TreebankSedExpecter:
    def __init__(self):
        self.sed = pexpect.spawn("perl", ["tokenizer.pl"])
        self.cache = {}
        self.sed.setecho(False)
        self.sed.delaybeforesend = 0

    def filter_line(self, u):
        if type(u) == type(''):
            u = unicode(u, 'utf-8')
        assert(type(u) == type(u''))
        #s = u.encode('utf-8') # still sad
        self.sed.sendline(u.rstrip())
        out = self.sed.readline().rstrip()
#        try:
#            
#        except:
#            out = '' # OW MY HEAD
#            self.__init__()
#            print >> sys.stderr, "For some reason,", u.encode('utf-8'), "failed to get sedded."
            
        unicode_out = unicode(out, 'utf-8')
        return unicode_out.strip()

    def tokenize_word(self, u):
        if u not in self.cache:
            self.cache[u] = self.filter_line(u)
        return self.cache[u]
    
    def tokenize(self, u):
        # I'm going to cache every freaking word.
        # Stop looking at me like that.
        return [ self.tokenize_word(w) for w in u.split() ]

if __name__ == '__main__':
    import sys
    t = TreebankSedExpecter()
    for line in sys.stdin:
        print t.filter_line(line)
    
