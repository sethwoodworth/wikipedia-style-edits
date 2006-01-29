#!/bin/bash
PROJECT=revision-indices
JOBWAIT=30m

CHATDIR="/tmp/dnet/$PROJECT/chat/"
RESULTS="/tmp/dnet/$PROJECT/results/"
MAXJOBS=36 # 18 times two
PRE_SLEEP=12

# For each computer, clear the CHATDIR and RESULTS directories
for comp in $(cat ~/dnet/machines); do
ssh $comp rm -rf $CHATDIR
ssh $comp rm -rf $RESULTS
done
# For each computer, create them blank
for comp in $(cat ~/dnet/machines); do
ssh $comp mkdir -p $CHATDIR
ssh $comp mkdir -p $RESULTS
done


# randomly assign jobs to machines
for file in $(ssh paulproteus@fomalhaut.acm.jhu.edu '(cd /mnt/paul/space/ ; ls) ' | ~/bin/bogosort -n )
do
JOBCOUNT=$(jobs | wc -l)
if [[ $JOBCOUNT -ge $MAXJOBS ]]
then
sleep $JOBWAIT
fi
# no matter what, sleep for some seconds
sleep $PRE_SLEEP
MY_UGRAD=$(~/bin/bogosort -n ~/dnet/machines | head -n1)
ssh $MY_UGRAD "scp paulproteus@fomalhaut.acm.jhu.edu:/mnt/paul/space/$file /tmp/$file ; hostname ;   ~/bin/7za e -so /tmp/$file | ( cd  ~/dnet/collab/code/ ; python create_revision_index.py ) | gzip > $RESULTS/${file%.7z}.gz " 2>&1 | gzip > $CHATDIR/$file-chat  &
echo $file started on $MY_UGRAD
done

