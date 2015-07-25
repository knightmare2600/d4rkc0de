<?php
/*
PLUGIN
CGI Scaner
*/
include('menu.php');
echo "<br><table BORDER COLS=1 WIDTH=\"600\" NOSAVE >";
echo "<tr ALIGN=CENTER NOSAVE><td>------------------------=(<font color=\"#FF3333\">CGI Scaner</font>)=---------------------------</td></tr>";
echo "</table>";

$Server=$HTTP_GET_VARS['server'];
$Cgi=$HTTP_GET_VARS['cgi'];
$TimeOut=$HTTP_GET_VARS['timeout'];
$Port=$HTTP_GET_VARS['port'];
$tryme=$HTTP_GET_VARS['tryme'];
$i=0;

$slash=substr(getcwd(),0,1);
if ($slash != "/") {
$slash="\\";
}

if ($TimeOut == null) {
$TimeOut="2";
}

if ($Cgi == null) {
$Cgi=getcwd().$slash."cgibugs.txt";
}

if ($Port == null) {
$Port="80";
}

function menu ($Server,$Cgi,$Port,$TimeOut) {
echo "<form action=\"cgiscan.php\" method=\"get\">";
echo "<input type=\"text\" name=\"cgi\" value=\"$Cgi\"> :List of CGI bugs<br>";
echo "<hr width=\"300\">";
echo "<input type=\"text\" name=\"tryme\" value=\"$tryme\"> :Individual CGI test (example: <b>/cgi-bin/formail.pl</b>)<br>";
echo "<input type=\"text\" name=\"server\" value=\"$Server\"> :Web Server Hostname<br>";
echo "<input type=\"text\" name=\"port\" value=\"$Port\"> :Port (example: 80)<br>";
echo "<input type=\"text\" name=\"timeout\" value=\"$TimeOut\"> :Time Out<br>";
echo "<input type=\"submit\" value=\"Scan\">";
echo "</form>";
}

if (!$Server) {
echo "<br>Please, select web server hostname.<br>";
menu($Server,$Cgi,$Port,$TimeOut);
die;
}

if (!$Port) {
echo "<br>ERROR: Please, select web server port.<br>";
menu($Server,$Cgi,$Port,$TimeOut);
die;
}

if (!$Cgi) {
	if (!$tryme) {
	echo "<br>ERROR: Please, select path to list of cgibugs.<br>";
	menu($Server,$Cgi,$Port,$TimeOut);
	die;
	}
}

if (!$TimeOut) {
echo "<br>ERROR: Please, select request TimeOut.<br>";
menu($Server,$Cgi,$Port,$TimeOut);
die;
}

echo "<b>Scaning....<br></b>";
$fs=fsockopen($Server,$Port);
if (!$fs) {
echo "<br>ERROR: Can't open $Server on $Port port.<br>";
die;
} else {
	if (!$tryme) {
	fclose($fs);
	$fp=fopen($Cgi,"r");
		while(!feof($fp)) {
		$line=trim(fgets($fp,20000));
			if (strlen($line)>1){
			scan($Server,$line,$Port,$TimeOut);
			}
		}
	fclose($fp);
	} else {
	$fs=fsockopen($Server,$Port);
	socket_set_timeout($fs,$TimeOut);
	fputs($fs,"GET $tryme HTTP/1.1\nHOST: LSA.cgi.test\n\n");
	$res=fread($fs,4000000);
	echo nl2br(htmlspecialchars($res));
	fclose($fs);
	}
echo "<br><b>The END:)</b>";
}
function scan ($Server,$line,$Port,$TimeOut) {
$fs=fsockopen($Server,$Port);
socket_set_timeout($fs,$TimeOut);
fputs($fs,"GET $line HTTP/1.1\nHOST: LSA.cgi.test\n\n");
$res=substr(trim(fgets($fs,30)),8);
	if (stristr($res,"200")) {
	$res="<font color=\"#FF0000\">$res</font>";
	}
echo "$line : $res <br>";
fclose($fs);
}
?>