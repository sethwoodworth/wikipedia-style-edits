import bag
import re
import string
CUTOFF=0.38
# Function words from http://www.webconfs.com/stop-words.php
f_words = ['a', 'able', 'about', 'above', 'abroad', 'according', 'accordingly', 'across', 'actually', 'adj', 'after', 'afterwards', 'again', 'against', 'ago', 'ahead', "ain't", 'all', 'allow', 'allows', 'almost', 'alone', 'along', 'alongside', 'already', 'also', 'although', 'always', 'am', 'amid', 'amidst', 'among', 'amongst', 'an', 'and', 'another', 'any', 'anybody', 'anyhow', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'appear', 'appreciate', 'appropriate', 'are', "aren't", 'around', 'as', "a's", 'aside', 'ask', 'asking', 'associated', 'at', 'available', 'away', 'awfully', 'b', 'back', 'backward', 'backwards', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'best', 'better', 'between', 'beyond', 'both', 'brief', 'but', 'by', 'c', 'came', 'can', 'cannot', 'cant', "can't", 'caption', 'cause', 'causes', 'certain', 'certainly', 'changes', 'clearly', "c'mon", 'co', 'co.', 'com', 'come', 'comes', 'concerning', 'consequently', 'consider', 'considering', 'contain', 'containing', 'contains', 'corresponding', 'could', "couldn't", 'course', "c's", 'currently', 'd', 'dare', "daren't", 'definitely', 'described', 'despite', 'did', "didn't", 'different', 'directly', 'do', 'does', "doesn't", 'doing', 'done', "don't", 'down', 'downwards', 'during', 'e', 'each', 'edu', 'eg', 'eight', 'eighty', 'either', 'else', 'elsewhere', 'end', 'ending', 'enough', 'entirely', 'especially', 'et', 'etc', 'even', 'ever', 'evermore', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'exactly', 'example', 'except', 'f', 'fairly', 'far', 'farther', 'few', 'fewer', 'fifth', 'first', 'five', 'followed', 'following', 'follows', 'for', 'forever', 'former', 'formerly', 'forth', 'forward', 'found', 'four', 'from', 'further', 'furthermore', 'g', 'get', 'gets', 'getting', 'given', 'gives', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'h', 'had', "hadn't", 'half', 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", 'hello', 'help', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', "here's", 'hereupon', 'hers', 'herself', "he's", 'hi', 'him', 'himself', 'his', 'hither', 'hopefully', 'how', 'howbeit', 'however', 'hundred', 'i', "i'd", 'ie', 'if', 'ignored', "i'll", "i'm", 'immediate', 'in', 'inasmuch', 'inc', 'inc.', 'indeed', 'indicate', 'indicated', 'indicates', 'inner', 'inside', 'insofar', 'instead', 'into', 'inward', 'is', "isn't", 'it', "it'd", "it'll", 'its', "it's", 'itself', "i've", 'j', 'just', 'k', 'keep', 'keeps', 'kept', 'know', 'known', 'knows', 'l', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', "let's", 'like', 'liked', 'likely', 'likewise', 'little', 'look', 'looking', 'looks', 'low', 'lower', 'ltd', 'm', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', "mayn't", 'me', 'mean', 'meantime', 'meanwhile', 'merely', 'might', "mightn't", 'mine', 'minus', 'miss', 'more', 'moreover', 'most', 'mostly', 'mr', 'mrs', 'much', 'must', "mustn't", 'my', 'myself', 'n', 'name', 'namely', 'nd', 'near', 'nearly', 'necessary', 'need', "needn't", 'needs', 'neither', 'never', 'neverf', 'neverless', 'nevertheless', 'new', 'next', 'nine', 'ninety', 'no', 'nobody', 'non', 'none', 'nonetheless', 'noone', 'no-one', 'nor', 'normally', 'not', 'nothing', 'notwithstanding', 'novel', 'now', 'nowhere', 'o', 'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', "one's", 'only', 'onto', 'opposite', 'or', 'other', 'others', 'otherwise', 'ought', "oughtn't", 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'own', 'p', 'particular', 'particularly', 'past', 'per', 'perhaps', 'placed', 'please', 'plus', 'possible', 'presumably', 'probably', 'provided', 'provides', 'q', 'que', 'quite', 'qv', 'r', 'rather', 'rd', 're', 'really', 'reasonably', 'recent', 'recently', 'regarding', 'regardless', 'regards', 'relatively', 'respectively', 'right', 'round', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'second', 'secondly', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sensible', 'sent', 'serious', 'seriously', 'seven', 'several', 'shall', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'since', 'six', 'so', 'some', 'somebody', 'someday', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specified', 'specify', 'specifying', 'still', 'sub', 'such', 'sup', 'sure', 't', 'take', 'taken', 'taking', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', "that'll", 'thats', "that's", "that've", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', "there'd", 'therefore', 'therein', "there'll", "there're", 'theres', "there's", 'thereupon', "there've", 'these', 'they', "they'd", "they'll", "they're", "they've", 'thing', 'things', 'think', 'third', 'thirty', 'this', 'thorough', 'thoroughly', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'till', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', "t's", 'twice', 'two', 'u', 'un', 'under', 'underneath', 'undoing', 'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'up', 'upon', 'upwards', 'us', 'use', 'used', 'useful', 'uses', 'using', 'usually', 'v', 'value', 'various', 'versus', 'very', 'via', 'viz', 'vs', 'w', 'want', 'wants', 'was', "wasn't", 'way', 'we', "we'd", 'welcome', 'well', "we'll", 'went', 'were', "we're", "weren't", "we've", 'what', 'whatever', "what'll", "what's", "what've", 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', "where's", 'whereupon', 'wherever', 'whether', 'which', 'whichever', 'while', 'whilst', 'whither', 'who', "who'd", 'whoever', 'whole', "who'll", 'whom', 'whomever', "who's", 'whose', 'why', 'will', 'willing', 'wish', 'with', 'within', 'without', 'wonder', "won't", 'would', "wouldn't", 'x', 'y', 'yes', 'yet', 'you', "you'd", "you'll", 'your', "you're", 'yours', 'yourself', 'yourselves', "you've", 'z', 'zero']

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
            all_olds[new][0].olds.remove(new) # SOMETHING EVIL HAPPENS HERE
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
    
    ret = [ HunkOfSentences(olds=old, news=new)
            for (old, new) in almost_ret ]
    return ret

tokenizer = re.compile(r'[\s-]')
def jaccard_two_sentences(from_s, to_s):
    # from and to are strings.  Turn them into lists of words.
    # "Tokenize aggressively."
    from_list = map(string.lower, tokenizer.split(from_s))
    to_list   = map(string.lower, tokenizer.split(to_s))

    # bag it
    from_bag = bag.bag(from_list)
    to_bag   = bag.bag(to_list)

    # In the intersection (respectively union) of two multisets A and
    # B, the count of x is the min (respectively sum) of its counts in
    # A and B.)

    # Iterating over only one bag is safe because we only consider things
    # in both bags anyway.
    intersection_counts = [ min(from_bag[thing], to_bag[thing])
                            for thing in from_bag.iterunique() ]
    union_counts = [ sum( (from_bag[thing], to_bag[thing]) )
                   for thing  in from_bag.iterunique() ]

    # "size" prefix to avoid shadowing builtin sum()
    size_intersection = sum(intersection_counts)
    size_union = sum(union_counts)

    # Jaccard's coefficient: size of intersection over size of union.
    return float(size_intersection) / float(size_union)



    


# Prefer a good match within the same diff hunk to a match from a
# different diff hunk.

# Don't consider matching to anything that doesn't appear in a diff
# hunk (because it was an exact match for something else, in
# position).

# Possibly look for matches between 1 new and 2 old sentences, or
# vice-versa.


def transform(s):
    ''' Takes the output of diff as input, since that what is XMLified.
    Returns
    TAKE NOTE: The data format of this is:
    Some number of lines preceded by "-" that indicate the thing that got replaced.
    Some number of lines preceded by "+" that indicate the thing that replaced it.
    There is no explicit delimeter except the unambiguous implicit delimiting based on + -> -.'''
    ret = ''
    diffhunks = diff2hunks(s)
    sentencepairs = hunks2sentencepairs(diffhunks)
    for hunk in sentencepairs:
        for old in hunk.olds:
            assert('\n' not in old)
            ret += '-' + old + '\n'
        for new in hunk.news:
            assert('\n' not in new)
            ret += '+' + new + '\n'
    return ret # That's a wrap!
