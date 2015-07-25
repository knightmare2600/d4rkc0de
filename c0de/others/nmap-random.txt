#!/bin/bash 
 
if [ x"${1}" = x"" ] ; then 
        echo 
        echo "Nmap Random ip List" 
	echo 
        echo "Author: homen3 <homen3@gmail.com>" 
        echo "License: GPL" 
        echo 
        echo "Usage: nmap-random.sh [PORT]" 
        ##### ################################################################################ 
        echo 
        exit 
fi 
 
function isint() { 
	ret=0 
	test -z $1 -o -n "$(echo $1 | grep  '^-\?[0-9]\+$')" || ret=1 
	return $ret 
} 
if isint "1" ; then 
        echo 
	echo "this can take a while. get a coffe." 
	nmap -v -iR 100000 -P0 -p $1 | tee /tmp/random-scan-at-$1 
	cat /tmp/random-scan-at-$1 | grep Discovered > random-scan-result 
	rm /tmp/random-scan-at-$1 
	exit 
fi 
 

