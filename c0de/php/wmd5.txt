#!/usr/bin/php
<?php

/*
 * Name: wmd5 - MD5 Hash Web Search
 * Credits: Charles "real" F. <charlesfol[at]hotmail.fr>
 * Date: 25/04/08
 */

$md5loc = array(
array('http://www.milw0rm.com/cracker/search.php','hash=','<TD align="middle" nowrap="nowrap" width=90>([^<]+)</TD><TD align="middle" nowrap="nowrap" width=90>cracked</TD></TR>'),
array('http://gdataonline.com/qkhash.php?mode=txt&hash=','','</td><td width="35%"><b>([^<]+)</b></td></tr>'),
array('http://pepowned.free.fr/?act=&x=52&y=16&md5=','','Le Plain Text de <b>\w{32}</b> est : <b>([^<]+)</b>'),
array('http://passcracking.ru/index.php','admin=false&admin2=77.php&datafromuser=','<td>\w{32}</td><td bgcolor=\#FF0000>([^<]+)</td><td>'),
array('http://md5.rednoize.com/?p&s=md5&_=&q=','','<div id="result">([^<]+)</div>'),
array('http://ice.breaker.free.fr/md5.php?hash=','','<b><br><br> - ([^<]+)<br><br><br><a href=http://ice\.breaker\.free\.fr/'),
);

for($k=1;$k<$argc;$k++)
{
	$md5 = strtolower($argv[$k]);
	for($i=0;$i<sizeof($md5loc);$i++)
	{
		$r = crack($md5loc[$i][0],$md5loc[$i][1],$md5loc[$i][2]);
		if($r) { print "$md5 is $r\n";break; }
	}
} 

function crack($url,$post,$gex)
{
	global $md5;
	if($post!=''&&preg_match("#$gex#",post("$url","$post$md5"),$res)) return $res[1];
	elseif(preg_match("#$gex#",get("$url$md5"),$res)) return $res[1];
	return 0;
}


function post($url,$data,$get=1,$headers='')
{
	$result = '';
	preg_match("#^http://([^/]+)(/.*)$#i",$url,$info);
	$host = $info[1];
	$page = $info[2];
	$fp = fsockopen($host, 80, &$errno, &$errstr, 30);
	
	$req  = "POST $page HTTP/1.1\r\n";
	$req .= "Host: $host\r\n";
	$req .= "User-Agent: Mozilla Firefox\r\n";
	$req .= $headers;
	$req .= "Connection: close\r\n";
	$req .= "Content-type: application/x-www-form-urlencoded\r\n";
	$req .= "Content-length: ".strlen( $data )."\r\n";
	$req .= "\r\n";
	$req .= $data."\r\n";

	fputs($fp,$req);
	
	if($get) while(!feof($fp)) $result .= fgets($fp,128);
	
	fclose($fp);
	return $result;
}

function get($url,$get=1,$headers='')
{
	$result = '';
	$result = '';
	$infos = parse_url($url);
	$host = $infos['host'];
	$page = $infos['path'];
	$fp = fsockopen($host, 80, &$errno, &$errstr, 30);
	
	$req  = "GET $page HTTP/1.1\r\n";
	$req .= "Host: $host\r\n";
	$req .= "User-Agent: Mozilla Firefox\r\n";
	$req .= $headers;
	$req .= "Connection: close\r\n\r\n";

	fputs($fp,$req);
	
	if($get) while(!feof($fp)) $result .= fgets($fp,128);
	
	fclose($fp);
	return $result;
}

?>
