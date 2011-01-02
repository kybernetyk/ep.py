#!/bin/bash

# reads in ~/.ep.py.rc and shows the next airing date for each show
#
# .ep.py.rc format:
#showname
#showname
#showname
#
#
# see _sample_.ep.py.rc
#
# by d. arndt
# https://github.com/daarndt
#


exec 10<~/.ep.py.rc

while read LINE <&10; do
	   ep.py "$LINE" | head -n 2
		 echo ""
done

exec 10>&-

