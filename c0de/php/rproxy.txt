<?php
/*
 *
 * Name: RProxy
 * Credits: charles "real" F. <charlesfol[at]hotmail.fr>
 * Date: 26/04/08
 *
 * RProxy permits you to get an HIGH ANONYMOUS HTTP proxy
 * with a host that just supports an apache webserver.
 *
 *
 *       +-> Local Socket -> PHP file -+
 *       |                             |
 *     Client                      Remote Host
 *       |                             |
 *       +- Local Socket <- PHP File <-+
 *
 * When the local listening socket receives an http request,
 * it sends it to the remote PHP file, which execute it.
 * Then the PHP file sends the response to the local socket,
 * which transmit it to the client.
 *
 * The advantage of RProxy is that it's usable everywhere
 * and really discret :)
 * It just needs an apache server to work, because a PHPfile
 * exec your HTTP Request for you.
 *
 * howto:
 * 1. Host this script on a remote host, like a free.fr FTP
 * (eg http://server.com/proxy.php)
 * 2. Launch the script, on your own computer, in CLI:
 *  $ php proxy.php http://server.com/proxy.php
 *  RProxy ready, listening on port 8888
 * 3. Now use this proxy like a normal one, localhost:8888.
 *
 * I made a very precisely commented code, expecting you to
 * understand it.
 *
 *
 * [ Done ]
 *
 * 26/03: Boundary mode is now supported.
 *        No matter  the request size,  because
 *        it's now splited into pieces.
 *        ($header_max var)
 * 23/04: Modified  a little Local Socket code.
 *        PHP did not like  \r\n  concatenation
 *        but I don't know why.
 *        Remote Host headers are now used, in-
 *        stead of PHP file's headers.
 * 09/06: A little update to support FF post.
 *
 *
 */

/* Local Socket Configuration */
$port		= 8888; # Port of your local listening socket
$max_conn	= 10;	# Maximum number of connections to your local socket
$header_max	= 1000; # Max header size.

#
# Part #1 [] Local Socket
#

# Client -> HTTP Request -> Local Socket -> Remote PHP file -> Local Socket -> HTTP Response -> Client
if(isset($argc) && $argc>1)
{
	$url = $argv[1];
	
	$handle = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
	socket_bind($handle, '127.0.0.1', $port);
	socket_listen($handle,$max_conn);
	
	print "RProxy ready, listening on port $port";
	
	while(TRUE)
	{
		$packet = '';
		
		# Client -> HTTP Request -> Local Socket
		# The Local Socket receives an HTTP Request from Client
		
		if(!$_client = socket_accept($handle)) exit("socket_accept(): error ($handle).");
		
		$client_request = '';
		
		while( (eregi("Content-type.*boundary",$client_request) && !eregi("--[0-9]+--\r?\n",$client_request)) 
		    || (eregi("^POST",$client_request) && !ereg("\r\n\r\n.+",$client_request))
		    || !ereg("\r\n\r\n",$client_request) )
			{ $client_request .= socket_read($_client, 2048, PHP_BINARY_READ); }
			
		preg_match("#Host: +([^\t\r\n]+)#i",$client_request,$client_host) or exit();
		$client_host = $client_host[1];
			
		print "\n".d()." -> $client_host ".strlen($client_request);
		
		# Local Socket -> Remote PHP file
		# The Local Socket sends the HTTP Request to the PHP file
		
		$infos      = parse_url($url);
		$phpf_host  = $infos['host'];
		$phpf_port  = isset($infos['port']) ? $infos['port'] : 80;
		
		$total = str_split(base64_encode($client_request),$header_max);
		
		$request  = "GET $url HTTP/1.1\r\n";
		$request .= "Host: $phpf_host\r\n";
		$request .= "User-Agent: Mozilla Firefox 5.0\r\n";
		
		for($i=0;$i<sizeof($total);$i++)
			$request .= "HTTP-Request-$i: ".$total[$i]."\r\n";

		$request .= "Connection: Close\r\n";
		$request .= "\r\n";
		
		# Remote PHP file -> Local Socket
		# The Local Socket receives the HTTP Response from the PHP file
		
		$_phpf = fsockopen($phpf_host,80);
		fputs($_phpf,$request);
		
		# Local Socket -> Client
		# The HTTP Response is transmitted by the Local Socket to the Client
		
		$http_response = '';
		while(!feof($_phpf)) $http_response .= fgets($_phpf);
		fclose($_phpf);
		
		
		# Remove HTTP Headers from PHP file's HTTP Response
		$code = explode("\r\n\r\n",$http_response);
		$http_response = '';
		for($i=1;$i<sizeof($code);$i++)
			$http_response .= $code[$i]."\r\n\r\n";
			
		$http_response = preg_replace("#^.*[\r\n]*HTTP#i","HTTP",$http_response);
		$http_response = preg_replace('#0[\r\n]*$#','',$http_response);
		
		socket_write($_client,$http_response,strlen($http_response));
		
		print "\n".d()." <- $client_host ".strlen($http_response);
		
		socket_close($_client);
	}
	
	
	exit();
}

#
# Part #2 [] Remote PHP File
#

if(!isset($_SERVER['HTTP_HTTP_REQUEST_0']))
{
	header("Location: http://google.com/");
	exit();
}

# Local Socket -> Remote PHP file -> Remote Host -> Remote PHP file -> Local Socket

# Local Socket -> Remote PHP file
# The PHP File receive the HTTP Request he must do


$client_request = '';
for($i=0;isset($_SERVER["HTTP_HTTP_REQUEST_$i"]);$i++)
	$client_request .= $_SERVER["HTTP_HTTP_REQUEST_$i"];
	
$client_request = base64_decode($client_request);

preg_match("#Host: +([^\t\r\n]+)#i",$client_request,$rhostname) or exit();
$rhostname = $rhostname[1];

# Clear client request

$clearheaders = array('Keep-Alive','Proxy-Connection','Connection');
for($i=0;$i<sizeof($clearheaders);$i++) $clearheaders[$i] = '#'.$clearheaders[$i].':.+\r\n#i';

$client_request = preg_replace($clearheaders,'',$client_request);
$client_request = preg_replace("#(Host:.+\r\n)#i","$1Connection: close\r\n",$client_request);

# Remote PHP file -> Remote Host
# The PHP file sends the HTTP Request

$_rhost = fsockopen($rhostname,80);
fputs($_rhost,$client_request);

# Remote Host -> Remote PHP file
# The PHP file receives the HTTP Response

$rhost_response = '';
while(!feof($_rhost)) $rhost_response .= fgets($_rhost);
fclose($_rhost);

# Remote PHP file -> Local Socket
# The PHP file displays the HTTP Response,
# which is recovered by the Local Socket

print $rhost_response;

function d()
{
	return date("H:i:s");
}

?>