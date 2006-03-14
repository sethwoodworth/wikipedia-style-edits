#!/usr/local/bin/perl

# adds spaces between characters
no bytes;
#print "$_\n";
while(<>)
{
#print $_;
@bytes = split //, $_;

 for($i = 0; $i <$#bytes; $i++){
#    print stderr ord $bytes[$i], " ";
    print $bytes[$i];
    if( ord $bytes[$i] > 160)
    {
	if($i+1<$#bytes)
	{
	    print $bytes[$i+1], " ";
	    $i++;
	}
    }
    }
    print "\n";
}

