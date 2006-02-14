#!/bin/bash
PROJECT=sentences
JOBWAIT=3m

SOURCE_MACHINE=paulproteus@fomalhaut.acm.jhu.edu
SOURCE_PATH=/mnt/paul/space/paragraphs/
DEST_PATH=/mnt/paul/space/paragraphs/sentences/

ssh $SOURCE_MACHINE mkdir -p $DEST_PATH

CHATDIR="/tmp/dnet/$PROJECT/chat/"
RESULTS="/tmp/dnet/$PROJECT/results/"
WORKDIR="/tmp/dnet/$PROJECT/work/"
MAXJOBS=30 # 18 times two
PRE_SLEEP=12

# For each computer, clear the CHATDIR and RESULTS directories
for comp in $(cat ~/dnet/machines); do
ssh $comp rm -rf $CHATDIR
ssh $comp rm -rf $RESULTS
ssh $comp rm -rf $WORKDIR
done
# For each computer, create them blank
for comp in $(cat ~/dnet/machines); do
ssh $comp mkdir -p $CHATDIR
ssh $comp mkdir -p $RESULTS
ssh $comp mkdir -p $WORKDIR
done


# randomly assign jobs to machines
for file in $(ssh $SOURCE_MACHINE "(cd $SOURCE_PATH ; ls *.7z) " | sort -n )
do
JOBCOUNT=$(jobs | wc -l)
if [[ $JOBCOUNT -ge $MAXJOBS ]]
then
sleep $JOBWAIT
fi
# no matter what, sleep for some seconds
sleep $PRE_SLEEP
MY_UGRAD=$(~/bin/bogosort -n ~/dnet/machines | head -n1)
( ssh $MY_UGRAD "scp $SOURCE_MACHINE:$SOURCE_PATH/$file $WORKDIR/$file ; hostname ;   ~/bin/7za e -so $WORKDIR/$file | ( cd  ~/dnet/collab/code/ ; sh paragraphs2sentences.sh  file:///dev/stdin ) | ~/bin/7za a -si $RESULTS/$file ; scp $RESULTS/$file $SOURCE_MACHINE:$DEST_PATH "  ; echo $file finished on $MY_UGRAD ) & 
echo $file started on $MY_UGRAD
done

