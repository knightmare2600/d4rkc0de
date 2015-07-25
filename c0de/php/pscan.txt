<?

##############################################
#       php proxy scanner- by Jackh4xor
#       j4ckh4xor [at ]gmail [.com]
##############################################
##############################################
## ##
## USAGE ##
## ##
## //TEST IP AND DEFINED PORT ##
## PSCAN.PHP?IP=<IP>&PORT=<PORT> ##
## ##
## ##
## //SCAN IP (ports 80 - 65200) ##
## PSCAN.PHP?IP=<IP>&SCAN=TRUE ##
## ##
## ##
##############################################
## ##
## TESED ON WINDOWS PHP5 & APACHE 2 ##
## UNTESTED ON NIX BUT SHOULD WORK ##
## ##
##############################################
## ##


set_time_limit(0);

$_port = $_GET['PORT'];
$_ip = $_GET['IP'];
$_scan = $_GET['SCAN'];
$Query = $_GET['q'];


function Port_Check($host, $port)
{
if (isset($host) && isset($port)) {
$i=(int)$port;
$fp = @fsockopen("tcp://".$host,$i,$errno,$errstr,10);

if($fp) { $res = TRUE; } else { $res = FALSE; }

} else {
$res = FALSE;
}
return $res;
}

function getmicrotime() ## USED IN PING
{
list ($usec, $sec) = explode(" ", microtime());
return ((float)$usec + (float)$sec);
}


function Sockcheck($host,$port,$type)
{
$Response = '..GOODCON..';

$ch = curl_init();


curl_setopt($ch, CURLOPT_URL, "http://".$_SERVER['SERVER_NAME']."".$_SERVER['PHP_SELF']."?q=true");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt($ch, CURLOPT_USERAGENT,'[DB]');

curl_setopt($ch, CURLOPT_PROXY, $host.":".$port);
if($type == "4") curl_setopt($ch, CURLOPT_PROXYTYPE, CURLPROXY_SOCKS4);
else if($type == "5") curl_setopt($ch, CURLOPT_PROXYTYPE, CURLPROXY_SOCKS5);

$mk_time = getmicrotime();

$SOCKGOOD = FALSE;
$html = curl_exec($ch);
if(stristr( trim($html) , $Response )) {
$SOCKGOOD = TRUE;
} else {
$SOCKGOOD = FALSE;
}


if ($SOCKGOOD == TRUE) {
$Proxy_Ping = trim(Round(((getmicrotime()-$mk_time) * 1000),0));
$res = "(".$port.") <font color=green>Open</font> : SOCK ".$type." Proxy Found <font color=";

if ($Proxy_Ping < 500) { $res .= 'green'; }
elseif ($Proxy_Ping < 1000) { $res .= 'orange'; }
else { $res .= 'red'; }

$res .= sprintf("> %s </font>ms<br>", $Proxy_Ping);
} else { $res = "(".$port.") <font color=green>Open</font> : No SOCK ".$type." Proxy Found<br>"; }

curl_close ($ch);
unset($ch);
return $res;
}


function HTTPProxy_Test($IP, $Port)
{
$Response = '..GOODCON..';

$fp = fsockopen($IP, (int)$Port, $errno, $errstr, 10);
if (!$fp) {
$res = "$errstr ($errno)<br />\n";
} else {
$mk_time = getmicrotime();

$out = "GET http://".$_SERVER['SERVER_NAME']."".$_SERVER['PHP_SELF']."?q=true HTTP/1.0\r\n";
$out .= "User-Agent: [DB]\r\n";
$out .= "Connection: Close\r\n";
$out .= "Pragma: no-cache\r\n";
$out .= "Accept-Charset: ISO-8859-1,UTF-8;q=0.7,*;q=0.7\r\n";
$out .= "Cache-Control: no\r\n";
$out .= "Accept-Language: en;q=0.7,en-us;q=0.3\r\n";
$out .= "\r\n";

fwrite($fp, $out);

$HTTPGOOD = FALSE;
while (!feof($fp)) {
$fptmp = fgets($fp, 128);

if( stristr( trim($fptmp) , $Response ) ) { $HTTPGOOD = TRUE; BREAK; }

}

if ($HTTPGOOD == TRUE) {
$Proxy_Ping = trim(Round(((getmicrotime()-$mk_time) * 1000),0));
$res = "(".$Port.") <font color=green>Open</font> : HTTP Proxy Found <font color=";

if ($Proxy_Ping < 500) { $res .= 'green'; }
elseif ($Proxy_Ping < 1000) { $res .= 'orange'; }
else { $res .= 'red'; }

$res .= sprintf("> %s </font>ms<br>", $Proxy_Ping);
} else { $res = "(".$Port.") <font color=green>Open</font> : No HTTP Proxy Found<br>"; }


fclose($fp);
}
return $res;
}


function scanPorts($host, $pfrom, $pto, $delay)
{
$res;
for ($i = $pfrom-1; $i <= $pto; $i++) {

$res[$i]['RES'] = 0;

if (Port_Check($host, $i)) {
$re[$i]['RES'] = 1;
$res[$i]['HTTP'] = HTTPProxy_Test($host, $i);
$res[$i]['SOCK4'] = Sockcheck($host, $i,4);
$res[$i]['SOCK5'] = Sockcheck($host, $i,5);
} else {
$res[$i]['RES'] = 0;
$res[$i]['C'] = '('.$i.') <font color=red>Closed</font> : Unable to test... <br>';
}

sleep($delay);
}
return $res;
}


if (isset($_ip)) {
if (isset($_scan)) {
$mk_time = getmicrotime();
$pt = scanPorts($_ip,80,65200,2);

echo "Scanning ".$_ip." .....<br>";

foreach($pt as $tport => $tres)
{
if ($tres['RES'] == 1) {

echo "-- ".$tres['HTTP'];
echo "-- ".$tres['SOCK4'];
echo "-- ".$tres['SOCK5'];

} //else { echo "- ".$tres['C']; } //uncomment to show closed ports as well
}

$Proxy_Ping = trim(Round(((getmicrotime()-$mk_time)),0));
echo "<br>Scanned in ".$Proxy_Ping."Secs<br>";

}
if (isset($_port)) {
if (Port_Check($_ip,$_port) == TRUE) {
echo "Scanning ".$_ip." .....<br>";
echo HTTPProxy_Test($_ip, $_port);
echo Sockcheck($_ip, $_port,4);
echo Sockcheck($_ip, $_port,5);
}
}
}

if (isset($Query)) {
$Response = '..GOODCON..';
echo $Response;
}


?>