#!/bin/sh
for network in asheesh@ugradx.cs.jhu.edu asheesh@kvetch.cs.jhu.edu paulproteus@acm.jhu.edu
do
	ssh $network "cd dnet/collab ; svn up"
done
