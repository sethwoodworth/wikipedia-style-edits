#!/bin/sh
for network in asheesh@ugradx.cs.jhu.edu asheesh@kvetch.cs.jhu.edu paulproteus@acm.jhu.edu
do
	echo "Starting on $network"
	ssh $network "cd dnet ; cd collab ; svn up"
done
