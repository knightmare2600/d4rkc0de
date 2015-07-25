<?php 
 
	//extract proxy+port from url 
	//extracts proxies from site if in ip:port format 
	//optionally can use anon http proxy for request 
	//use: php proxy-extract.php site.com [-p proxy:port] 
	//extractor by int3 
 
	$use_proxy = false; 
	for ($i=0; $i<$argc; $i++) { 
		if ($argv[$i] == "-p") { 
			$i++; 
			$use_proxy = true; 
			$proxy = substr($argv[$i], 0, strpos($argv[$i], ":")); //get proxy server 
			$proxy_port = substr($argv[$i], strpos($argv[$i], ":")+1); //get proxy port 
		} 
		else 
			$url = $argv[1]; 
	} 
	$curl = curl_init(); 
	curl_setopt($curl, CURLOPT_URL, $url); 
	curl_setopt($curl, CURLOPT_USERAGENT, "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"); 
	curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1); 
	if ($use_proxy = true) { 
		curl_setopt($curl, CURLOPT_HTTPPROXYTUNNEL, true); 
		curl_setopt($curl, CURLOPT_PROXYTYPE, CURLPROXY_HTTP); 
		curl_setopt($curl, CURLOPT_PROXY, $proxy); 
		curl_setopt($curl, CURLOPT_PROXYPORT, $proxy_port); 
	} 
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1); //return site as string 
	$page = curl_exec($curl); 
	curl_close($curl); 
	preg_match_all("/[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\:[0-9]*/", $page, $match); 
	for ($i=0; $i<count($match[0]); $i++) { 
		echo $match[0][$i], "\n"; 
	} 
?> 

