# From www.sims.berkeley.edu:8000/courses/.../lecture3.ppt
import commands
import tempfile
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

def treebank_tokenize_lines(u):
    if type(u) == type(''):
        u = unicode(u)
    assert(type(u) == type(u''))
    s = u.encode('utf-8') # still sad
    # Holy secure temp file handling, Batman!
    fd, fname = tempfile.mkstemp()
    os.write(fd, s)
    os.close(fd)
    out = commands.getoutput("sed -f tokenizer.sed < " + fname)
    unicode_out = unicode(out, 'utf-8')
    os.unlink(fname)
    return [line.strip().split(' ') for line in unicode_out.split('\n') if line]
if __name__ == '__main__':
    import sys
    for line in sys.stdin:
        val = treebank_tokenize_lines(line)
        if val:
            print ' '.join(treebank_tokenize_lines(line)[0])
    
