#!/bin/sh
for network in asheesh@ugrad3.cs.jhu.edu asheesh@kvetch.cs.jhu.edu paulproteus@acm.jhu.edu
do
	echo "Starting on $network"
	ssh -t $network "cd dnet ; cd collab ; svn up" 
done
