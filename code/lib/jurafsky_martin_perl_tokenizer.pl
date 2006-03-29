#!/usr/bin/perl

## Taken from http://www.cs.colorado.edu/~martin/SLP/Updates/3.pdf

$letternumber = "[A-Za-z0-9]";
$notletter = "[ˆA-Za-z0-9]";
$alwayssep = "[\\?!()\";/\\|‘]";
$clitic = "(’|:|-|’S|’D|’M|’LL|’RE|’VE|N’T|’s|’d|’m|’ll|’re|’ve|n’t)";
$abbr{"Co."} = 1; $abbr{"Dr."} = 1; $abbr{"Jan."} = 1; $abbr{"Feb."} = 1;
while (<>){
      # put whitespace around unambiguous separators
      s/$alwayssep/ $& /g;
      # put whitespace around commas that aren’t inside numbers
      s/([ˆ0-9]),/$1 , /g;
      s/,([ˆ0-9])/ , $1/g;
      # distinguish singlequotes from apostrophes by
      # segmenting off single quotes not preceded by letter
      s/ˆ’/$& /g;
      s/($notletter)’/$1 ’/g;
      # segment off unambiguous word-final clitics and punctuation
      s/$clitic$/ $&/g;
      s/$clitic($notletter)/ $1 $2/g;
    # now deal with periods. For each possible word
    @possiblewords=split(/\s+/,$_);
    foreach $word (@possiblewords) {
        # if it ends in a period,
        if (($word =˜ /$letternumber\./)
               && !($abbr{$word}) # and isn’t on the abbreviation list
                  # and isn’t a sequence of letters and periods (U.S.)
                  # and doesn’t resemble an abbreviation (no vowels: Inc.)
               && !($word =˜ /ˆ([A-Za-z]\.([A-Za-z]\.)+|[A-Z][bcdfghj-nptvxz]+\.)$/)) {
            # then segment off the period
            $word =˜ s/\.$/ \./;
        }
        # expand clitics
        $word =˜s/’ve/have/;
        $word =˜s/’m/am/;
        print $word," ";
    }
  print "\n";
}
