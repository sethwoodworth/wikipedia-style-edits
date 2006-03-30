import bag
import re
from sets import Set
CUTOFF=0.42 # ?...

# Here's what I believe: I believe that the best match will be fairly
# obvious, and that it's not a huge problem if the next stage of
# processing gets given too many "matching" sentences.

# I'm more worried about the opposite problem, in fact - that we
# accidentally omit data from the next stage.

# Eisner wanted the Jaccard value to be made available to later
# processing.  Fine.

# Diff the two revisions.
## This code forgets how far diff hunks were away from each other.
class HunkOfSentences:
    def __init__(self, olds, news, confidence=-1):
        self.olds = olds
        self.news = news
        self.confidence = confidence # Confidence of -1 means unknown

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

def test_only_typo_editops():
    e1 = [('delete', 2, 2), ('delete', 3, 2), ('replace', 10, 8), ('replace', 11, 9)]
    e2 = [('replace', 2, 2), ('replace', 3, 3), ('replace', 10, 10), ('replace', 11, 11)]
    e3 = [('insert', 0, 0), ('insert', 0, 1), ('insert', 0, 2), ('insert', 0, 3), ('insert', 0, 4)]
    e4 = [('insert', 0, 0), ('insert', 0, 1), ('insert', 0, 2), ('insert', 0, 3), ('insert', 0, 4), ('insert', 3, 8), ('insert', 3, 9)]
    e5 = [('insert', 0, 0), ('insert', 0, 1), ('insert', 0, 2), ('insert', 0, 3), ('insert', 0, 4), ('insert', 2, 7), ('replace', 2, 8)]

    for everything, good in ( (e1, e1),
                              (e2, e2),
                              (e3, []),
                              (e4, e4[-2:]),
                              (e5, []),
                              ):
        assert(only_typo_editops(everything) == good)
    print "Yay-uh!"

def only_typo_editops(eo):
    ''' Input: a list of edit operations
    Output: A list, perhaps empty, perhaps smaller, of edit operations'''
    ret = []

    ## 2. Look for typo edits in that alignment: places where at most
    ## two chars were replaced by at most two chars (via any edit
    ## operations) and this little region is buffered from any other
    ## edit regions by at least three perfectly matched characters.
    ## (Note that a local edit at the start of a sentence doesn't have
    ## to be preceded by perfectly matched chars.)
    before_this_pair_offset = -3
    last_good_edit = []
    for edit_op in eo:
        type, from_offset, to_offset = edit_op
        # If there's something growing
        if last_good_edit:
            # then, if we're three away from it, and it's the kind of thing we want to keep, keep it
            if from_offset - last_good_edit[-1][1] >= 3:
                if len(last_good_edit) <= 2:
                    ret += last_good_edit
                last_good_edit = []
        # If the from_offset is three away from the last edit we saw
        if from_offset - before_this_pair_offset >= 3:
            # then add to the last_good_edit
            last_good_edit.append(edit_op)
        else:
            before_this_pair_offset = from_offset
            if len(last_good_edit) <= 2:
                ret += last_good_edit
                last_good_edit = []
    if len(last_good_edit) <= 2:
        ret += last_good_edit
    return ret

import Levenshtein as lev # spellign Levnshtein...
def make_improved_old(old, new):
    ''' 3. Modify the old version of the hunk by these typo edits, so
    that it looks more like the new version.'''
    # Calculate the edit moves necessary
    eo = lev.editops(old, new)

    # Now, filter those through something that looks for only "typo edits"
    do_these = only_typo_editops(eo)

    # Now, do them to old
    return lev.apply_edit(eo, old, new)

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
            old_jaccard_this = apply_typo_edits(old_jaccard_this, new)
            competitors.append( (jaccard_two_sentences(old_jaccard_this, new), old_set, olds) )
    competitors.sort()
    competitors.reverse() # YOW!  This way the best is first.
    return competitors

def append_good_competitor(src, dst, new_set):
    for (jaccard, old_set, olds) in src:
        if jaccard < CUTOFF: # forget it; it's only getting worse
            return False
        else: # First time we're >= CUTFF
            dst.append( (old_set, new_set, jaccard) )
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
            
    
    ret = [ HunkOfSentences(olds=old, news=new, confidence=value)
            for (old, new, value) in almost_ret ]
    return ret

# LAME:
# On module init, I'll open a pipe to sed.
# Sosumi.
import tokenize
t = tokenize.TreebankSedExpecter()

def test_jaccard():
    for from_s, to_s, exp_val in (
        ("a a b b b b c c d d", "c c c x x b y z", 0.2),
        ("ab b b", "ab b b", 1.0)):
        assert(jaccard_two_sentences(from_s, to_s) == exp_val)
    print "Everything is swell."

def jaccard_two_sentences(from_s, to_s):
    # from and to are strings.  Turn them into lists of words.
    # "Tokenize aggressively."
    from_list = [s.lower() for s in t.tokenize(from_s)]
    to_list   = [s.lower() for s in t.tokenize(to_s)  ]
    return jaccard_two_lists(from_list, to_list)

def jaccard_two_lists(from_list, to_list):
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
    ret += str(l.confidence) + "\n"
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
    Some NUMBER on a line of its own that represents confidence.
    Some number of lines preceded by "-" that indicate the thing that got replaced.
    Some number of lines preceded by "+" that indicate the thing that replaced it.
    There is the explicit delimeter of confidence value.'''
    diffhunks = diff2hunks(s)
    sentencepairs = hunks2sentencepairs(diffhunks)
    return format_hunk_list(sentencepairs)
