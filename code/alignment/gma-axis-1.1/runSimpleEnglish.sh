#!/bin/bash

# top-level program for the Simple English Axis Generation package
# contains basic axis creation functionality

########################################################################################
#                      runSimpleEnglish.sh
#
# This script creates axis files for use with GMA Geometric Mapping and Alignment
# 
#     english language files:
# 
# 1. creates simple axis files
# 
# Input   directory where English language text files can be found w/extension .e.txt
# Outputs the coresponding axis files for each text file in that same directory
# Author: Ali
#######################################################################################


ARGS=1        # Number of arguments expected.
E_BADARGS=65  # Exit value if incorrect number of args passed.

test $# -ne $ARGS && echo "Usage: `basename $0` $ARGS argument(s)" && exit $E_BADARGS

function englishAxis
{
    if [ ! -e "$1" ]; then
	echo "file $1 does not exist."
	return 1
    else
	fname=`basename $1`
	
	cat $1 | ./tools/tokposlen_WithEOLMark | ./tools/axis.afterTPL  
    fi
}

# go through each of the files in the given directory
for filename in "$1"/*; do

    case $filename in
	 *.axis )  echo "$filename already exists"
	           ;;
	*.e.txt )  base=`echo $filename | sed s/\.e\.txt//g`
	           # if you want to generate the axis each time regardless of 
	           # whether or not an axis already exists, remove the following
	           # condition
	           if ! [ -s "$filename.axis" ]; then
		       echo "Computing axis file $filename.axis..."
		       englishAxis "$filename" > $filename.axis 
		       echo "done."

		   else echo "Already done"
		   fi
		   ;;
	       * ) echo "$filename is neither a text file or an axis file... moving on."
	           ;;
    esac
done


