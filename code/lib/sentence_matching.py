import bag
import re
from sets import Set
CUTOFF=0.38
# Function words from http://www.webconfs.com/stop-words.php


# Diff the two revisions.
## This code forgets how far diff hunks were away from each other.
class HunkOfSentences:
    def __init__(self, olds, news):
        self.olds = olds
        self.news = news

def diff2hunks(s):
    ''' This is for diff -u .  Also, I hate lines with only
    whitespace.  I will remove them with extreme prejudice.'''
    almost_ret = []
    olds, news = [], []
    assert(not(olds is news))
    lines = s.split('\n')
    # throw away first two lines that describe the filename and date
    lines = lines[2:]

    for line in lines:
        if line:
            if line[0] == '@' or line[0] == ' ':
                # Then a hunk is over
                if olds or news:
                    almost_ret.append( (olds, news) )
                    olds, news = [], []
                    assert(not(olds is news))
            elif line[0] == '-':
                olds.append(line[1:])
            elif line[0] == '+':
                news.append(line[1:])
    if olds or news:
        almost_ret.append( (olds, news) )
    ret = [ HunkOfSentences(olds=[old for old in olds if old.strip()], news=[new for new in news if new.strip()])
            for (olds, news) in almost_ret ]
    return ret

def make_sorted_competitors(new, oldss, oldslicelen):
    competitors = []
    for olds in oldss:
        if oldslicelen == 1:
            try_this_many = len(olds)
        elif oldslicelen == 2:
            try_this_many = len(olds) - 1
        for k in range(try_this_many):
            old_set = olds[k:k + oldslicelen]
            if len(old_set) > 1:
                old_jaccard_this = ' '.join(old_set)
            else:
                old_jaccard_this = old_set[0]
            competitors.append( (jaccard_two_sentences(old_jaccard_this, new), old_set, olds) )
    competitors.sort()
    competitors.reverse() # YOW!  This way the best is first.
    return competitors

def append_good_competitor(src, dst, new_set):
    for (jaccard, old_set, olds) in src:
        if jaccard < CUTOFF: # forget it; it's only getting worse
            return False
        else: # First time we're >= CUTFF
            dst.append( (old_set, new_set) ) # FIXME: This will break for pairs.
            for old in old_set:
                olds.remove(old)
            return True

# For each new sentence mentioned by the diff, keep the best "good"
# match (if any!) from the old revision.
def hunks2sentencepairs(hunks):
    ''' Input: a list of hunks from diff, sorted by order of
    appearance.

    Output: A list of hunks, where each sentence (or two) in news maps
    to a single sentence in olds.'''

    # First, let's remove duplicate sentences.
    all_olds = {} # maps from sentence strings to list of places it occurs
    all_news = {} # same deal
    for hunk in hunks:
        for new in hunk.news:
            if new not in all_news:
                all_news[new] = []
            all_news[new].append(hunk)
        for old in hunk.olds:
            if old not in all_olds:
                all_olds[old] = []
            all_olds[old].append(hunk)

    # Now, remove duplicates
    for new in all_news:
        if new in all_olds:
            # Then remove from both containing hunks
            assert(not(all_olds[new][0].olds is all_news[new][0].news))
            all_olds[new][0].olds.remove(new)
            all_news[new][0].news.remove(new)
            # Clean up all_olds and all_news
            for thing in all_olds[new]:
                if thing == []:
                    all_olds[new].remove(thing)
            for thing in all_news[new]:
                if thing == []:
                    all_news[new].remove(thing)

            if all_olds[new] == []:
                del all_olds[new]
            if all_news[new] == []:
                del all_olds[new]

    del all_news # just to
    del all_olds # be clear

    almost_ret = [] # list of (old, new) pairs

    # For now, do single sentences only.

    # First, within the hunk.
    for hunk in hunks:
        for new in hunk.news:
            competitors = make_sorted_competitors(new = new, oldss = [hunk.olds], oldslicelen=1)
            KEEP_GOING = not append_good_competitor(src=competitors, dst=almost_ret, new_set=[new])
            if KEEP_GOING: # Then try all the other hunks, too.
                olds = [ not_this_hunk.olds for not_this_hunk in hunks if not_this_hunk is not hunk ] 
                competitors = make_sorted_competitors(new = new, oldss = olds, oldslicelen=1)
                KEEP_GOING = not append_good_competitor(src=competitors, dst=almost_ret, new_set=[new])
            if KEEP_GOING: # Then try 1-from-2 matching within this hunk
                competitors = make_sorted_competitors(new = new, oldss = [hunk.olds], oldslicelen=2)
                KEEP_GOING = not append_good_competitor(src=competitors, dst=almost_ret,new_set=[new])
            if KEEP_GOING: # Then try 1-from-2 matching within this hunk
                olds = [ not_this_hunk.olds for not_this_hunk in hunks if not_this_hunk is not hunk ]
                competitors = make_sorted_competitors(new = new, oldss = olds, oldslicelen=2)
                KEEP_GOING = not append_good_competitor(src=competitors, dst=almost_ret, new_set=[new])
    # Whew.  Now, we just need 2-from-1 matching and we're set.
    for hunk in hunks:
        for k in range(len(hunk.news)-1):
            new_set = hunk.news[k:k+2]
            if len(new_set) < 2:
                break # loop over the next hunk now
            spaced_out_news = ' '.join(new_set)
            competitors = make_sorted_competitors(new = spaced_out_news,
                                                  oldss = [hunk.olds],
                                                  oldslicelen = 1)
            KEEP_GOING = not append_good_competitor(src=competitors, dst=almost_ret, new_set=new_set)
            if not KEEP_GOING: # then we found one, and better remove it from news
                hunk.news.remove(new_set[0]) ; hunk.news.remove(new_set[1])
            # What's that?  Still haven't found one?
            # Try to find a 2-from-1 across the other hunks.
            else: # if KEEP_GOING
                olds = [ not_this_hunk.olds for not_this_hunk in hunks if not_this_hunk is not hunk ]
                competitors = make_sorted_competitors(new = spaced_out_news,
                                                      oldss = olds,
                                                      oldslicelen = 1)
                success = append_good_competitor(src=competitors, dst=almost_ret, new_set=new_set)
                if success:
                    hunk.news.remove(new_set[0]) ; hunk.news.remove(new_set[1])
            
    
    ret = [ HunkOfSentences(olds=old, news=new)
            for (old, new) in almost_ret ]
    return ret

tokenizer = re.compile(r'[\s-]')
def jaccard_two_sentences(from_s, to_s):
    # from and to are strings.  Turn them into lists of words.
    # "Tokenize aggressively."
    from_list = [s.lower() for s in tokenizer.split(from_s)]
    to_list   = [s.lower() for s in tokenizer.split(to_s)  ]

    # bag it
    from_bag = bag.bag(from_list)
    to_bag   = bag.bag(to_list)

    # In the intersection (respectively union) of two multisets A and
    # B, the count of x is the min (respectively sum) of its counts in
    # A and B.)

    union_count = 0
    intersection_count = 0
    keys = Set()
    keys.update(from_bag.iterunique())
    keys.update(to_bag.iterunique())
    for thing in keys:
        union_count += max(to_bag[thing],from_bag[thing])
        intersection_count += min(to_bag[thing],from_bag[thing])
        
    # Jaccard's coefficient: size of intersection over size of union.
    return float(intersection_count) / float(union_count)

# Prefer a good match within the same diff hunk to a match from a
# different diff hunk.

# Don't consider matching to anything that doesn't appear in a diff
# hunk (because it was an exact match for something else, in
# position).

# Possibly look for matches between 1 new and 2 old sentences, or
# vice-versa.

def format_hunk_list(l):
    ret = ''
    for hunk in l:
        for old in hunk.olds:
            assert('\n' not in old)
            ret += '-' + old + '\n'
        for new in hunk.news:
            assert('\n' not in new)
            ret += '+' + new + '\n'
    return ret # That's a wrap!
    

def transform(s):
    ''' Takes the output of diff as input, since that what is XMLified.
    Returns
    TAKE NOTE: The data format of this is:
    Some number of lines preceded by "-" that indicate the thing that got replaced.
    Some number of lines preceded by "+" that indicate the thing that replaced it.
    There is no explicit delimeter except the unambiguous implicit delimiting based on + -> -.'''
    diffhunks = diff2hunks(s)
    sentencepairs = hunks2sentencepairs(diffhunks)
    return format_hunk_list(sentencepairs)
