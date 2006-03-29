# From www.sims.berkeley.edu:8000/courses/.../lecture3.ppt
import string
import nltk.token
import nltk.tokenizer
url = r'((http:\/\/)?[A-Za-z]+(\.[A-Za-z]+){1,3}(\/)?(:\d+)?)'
hyphen = r'(\w+\-\s?\w+)'
apostro = r'(\w+\'\w+)'
numbers = r'((\$|#)?\d+(\.)?\d+%?)'
punct = r'([^\w\s]+)'
wordr = r'(\w+)'
regexp = '|'.join([url, hyphen, apostro, numbers, wordr, punct])
RT = nltk.tokenizer.RegexpTokenizer(regexp, SUBTOKENS='WORDS')

def tokenize(u):
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

