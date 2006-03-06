#!/bin/sh -xe
number=${RANDOM}
let "number = number % 20 + 1"
sleep ${number}
FILE=$1
#number=$(echo ${FILE} | sed -r 's/([^0-9]*?)([0-9]+)(.*?)/\2/' )
MACHINECOUNT=$(wc -l < ~/dnet/machines)
let "number = $number % ${MACHINECOUNT} + 1 "
MACHINE=$(cat ~/dnet/machines | head -n${number} | tail -n1)
shift
scp ${FILE} ${MACHINE}:/tmp/
ssh ${MACHINE} "$@"
ssh ${MACHINE} rm /tmp/${FILE}
echo -n "Finished ${FILE} at "; date
