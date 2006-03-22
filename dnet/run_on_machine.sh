#!/bin/sh -xe
number=${RANDOM}
let "number = number % 20 + 1"
sleep ${number}
FILE=$1
#number=$(echo ${FILE} | sed -r 's/([^0-9]*?)([0-9]+)(.*?)/\2/' )
MACHINECOUNT=$(wc -l < ~/dnet/machines)
number=${RANDOM}
let "number = number % 20 + 1"
let "number = $number % ${MACHINECOUNT} + 1 "
MACHINE=$(sh ~/dnet/pick_machine.sh)
shift
scp ${FILE} ${MACHINE}:/tmp/
ssh ${MACHINE} "$@"
ssh ${MACHINE} rm /tmp/${FILE}
echo -n "Finished using ${FILE} at "; date
