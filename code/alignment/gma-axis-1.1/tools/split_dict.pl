#!/usr/local/bin/perl

# take in a dictionary of the form: 
# (English Word, tab, English POS, tab, Other Lang Word, tab, Other Lang POS)
# Outputs: English dictionary, OtherLang Dictionary
# -Ali (06/12/03) 

open(INPUTDICT, "< @ARGV[0]");
open(OUTPUTENG,"> @ARGV[1]");
open(OUTPUTOL,"> @ARGV[2]"); 

#print "$_\n";
while(<INPUTDICT>)
{
    #print "\n";
    #print $_;
    ($eng,$ol) = m/([\S ]*)[\s]*[\S]*[\s]*([\S ]*)[\t]*[\S]*/;
    print OUTPUTENG $eng . "\n";
    print OUTPUTOL $ol . "\n";
}
close OUTPUTENG;
close OUTPUTOL;


