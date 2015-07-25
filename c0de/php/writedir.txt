<?php

//If open basedir is on, search the closest directory possible, otherwise search "/"
//this will take a very long time to complete
//define('path', ini_get('open_basedir') ? ini_get('open_basedir') : DIRECTORY_SEPARATOR);

//One directory before the current directory:
define('path', '..');

//Maximum number of directories to find (to save time)
//define('maxdirs', 10);

set_time_limit(0);
$writable = array();

function finddir($d = path){
	global $writable;
	if(defined('maxdirs')){
		if(count(array_unique($writable)) >= maxdirs){
			printout();
		}
	}
	$tmp = array();
	if($x = scandir($d)){
		foreach($x as $y){
			if(@is_dir($d . DIRECTORY_SEPARATOR  . $y)){
				if($y != ".." && $y != "."){
					array_push($tmp, $y);
					$real = $d . DIRECTORY_SEPARATOR . $y;
				}
			}
			foreach($tmp as $t){
				if(@is_writable($d . DIRECTORY_SEPARATOR  .  $t)){
					array_push($writable, $d . DIRECTORY_SEPARATOR  . $t);
				}
				finddir($real);
			}
		}
  	}
}

function printout(){
	global $writable;
	?><p><b>Writable directories:</b></p>
	<textarea rows=<?php echo(count(array_unique($writable))); ?> cols=50><?php
	echo(($writable ? implode("\n", array_unique($writable)) : "No writable directories found.") . "\n</textarea>"); 
	die();
}
finddir();
printout();
?>