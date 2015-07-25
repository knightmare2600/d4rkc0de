<?php

error_reporting(E_ALL);
set_time_limit('18000');

//Unix required (grep / logresolve must be present on system)

$logresolve_path = '/usr/sbin/logresolve'; //find / -name logresolve
$log_path = '../logs/access_log'; //location of Apache raw log file

system($logresolve_path.' < '.$log_path.' > access_log_resolved.log');
system("grep -e '\\.gov\\|\\.mil' access_log_resolved.log > access_log_resolved_special.log")

$hostnames = array();
$lines=file('access_log_resolved_special.log');
for($i=0;$i<count($lines);$i++){
	list($hostname) = split(' ', $lines[$i], 2);

	if (preg_match("/\.mil$|\.gov$|\.gov\.[a-z]+$/", $hostname)) {

		list($hn1, $hostnamep) = explode('.', $hostname, 2);

		if (preg_match("/^gov\.[a-z]+$/", $hostnamep)) {
			$hostnamep = $hostname;
		} else {
			$hostnamep = '.'.$hostnamep;
			//$toadd = strlen($hn1);
			//$hostnamep = str_repeat('*', $toadd) . '.' . $hostnamep;
		}

		$hostnames[] = $hostnamep;
	}
}

$hostnames_unique = array_unique($hostnames);

$hostnameslist = '';
foreach ($hostnames_unique as $hostname) {
	$hostnameslist .= $hostname."\r\n";
}

echo $hostnameslist;

$file = fopen("specialhitslist.log","w");
flock ($file,2);
fwrite($file,$hostnameslist);
fclose($file);

?>