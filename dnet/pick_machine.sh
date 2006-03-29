#!/bin/sh
MAX=52

# Calculate last_line + 1
touch /tmp/last_line
LAST=$(cat /tmp/last_line)
let "LAST= LAST % $MAX + 1"

# Store it
echo $LAST > /tmp/last_line

# Now print the machine
head -n$LAST ~/dnet/machines.randomized  | tail -n1
