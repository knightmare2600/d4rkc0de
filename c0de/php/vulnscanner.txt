#!/usr/bin/php -q 
<?php

/**
 *     Php Vulnerability Scanner by KingOfSka @ http://www.contropoterecrew.org
 *    still very early release, just for testing and coding purpose :)
 *    
 *    Changelog:
 *    
 *    12/09/06    Version 0.1 : First "working" version, should work on "almost" site, report any bug to help me :)
 *    25/09/06        0.2 : Better crawling, less bandwith/resource usage, speed improved, better vuln finding code
 *
**/

print_r('
-------------------------------------------------------------------------------
Php Vulnerability Scanner by KingOfska @ http://contropotere.netsons.org
    kingofska [at] gmail [dot] com
-------------------------------------------------------------------------------
');

if ($argc < 2) {
print_r('
Early release, please send bug report to help improving this script
--------------------------------------------------------------------------------
Usage: '.$argv[0].' host [start_path][port][debug]
host:      target server (ip/hostname)
path:      path from which to start scanning, if none entered starts from \'/\'
port:       port of the http server, default 80

Examples:
'.$argv[0].' localhost /folder/script.php 81

--------------------------------------------------------------------------------
');
die;
}
$host= $argv[1];  // Insert the host site i.e. : www.website.com
$start_page = $argv[2];     // Insert the start page for the scan, if empty will start from index.*
$port = 80 ;
$additional_vars = array('id','page');
$locator = array("123'",'\'\';!--"<XSS>=&{()}','some_inexisistent_file_to_include.php');  //XSS Locator from ha.ckers.org

$debug = TRUE;
/**    Compatibility for php < 5
 *    stripos() function made by rchillet at hotmail dot com
 *
 */
if (!function_exists("stripos")) {
  function stripos($str,$needle,$offset=0)
  {
     return strpos(strtolower($str),strtolower($needle),$offset);
  }
}
/**
 *    Do not edit below unless you know what you do...
 */
$reqmade = 0 ;
$time_start = getmicrotime();
set_time_limit(0);
error_reporting(E_ERROR);
$checkedpages[]='';
$result[] = '';
$links[] = '';
$checkedlinks[] = '' ;
echo "Starting scan on $host:\r\nStarting page: $start_page\r\n";
$site_links = index_site();
$count = count($site_links);
echo "Starting to scan $count pages...\r\n";

foreach($site_links as $cur){

echo "Testing: $cur \r\n";
test_page($cur);

}

$time_end = getmicrotime();
$result['time'] = substr($time_end - $time_start,0,4);
$result['connections'] = $reqmade;
$result['scanned'] = count($checkedpages);

echo "Report:";

foreach ($result['vuln'] as $type=> $url){
echo "\r\n$type vulnerability found:\r\n";
$url = array_unique($url);
foreach($url as $cur){
echo "$cur \r\n";
}
}
$server = get_server_info();
echo "\r\nAdditional infos:\r\n";
echo "Site running on: ".$server['software']."\r\n";
echo "Powered by: ".$server['powered']."\r\n";
echo "Scan took ".$result['time']." seconds to scan ".$result['scanned']." pages using ".$result['connections']." connections\r\n";



function index_site(){
global $start_page;
array($links);
$tmp = get_links($start_page,true);
    foreach($tmp as $cur){
    $tmp2 = get_links($cur,true);
    $links = array_merge_recursive($links,$tmp2);
    }
$links = array_unique(clean_array($links));
$links[] = $start_page;
sort($links);
return($links);
}


/**
 * Testes a form using global vuln locator, both GET and POST method, and print result to screen
 * @author KingOfSka <kingofska@gmail.com>
 * @param array $form Form to test
 * @return void
*/

function test_form($form){
$ret = '';
$tmp = '';
global $host,$port,$locator,$debug,$result ;
if($form['action'][0] != '/' AND stripos($form['action'],'http://') === FALSE ){$form['action'] = '/'.$form['action'];}
if ($form['method'] = 'get'){
foreach($form['vars'] as $current){
        foreach($locator as $testing){
        $testing = urlencode($testing);
        $conn =  fsockopen ("$host", $port, $errno, $errstr, 30);
            if (!$conn) {
                echo "$errstr ($errno)<br>\n";
            } else {
                if (!stripos('?',$data['action'])){
                $req = "GET ".$form['action']."?$current=$testing HTTP/1.0\r\nHost: $host\r\nConnection: Close\r\n\r\n";
                }else{
                $req=  "GET ".$form['action']."&$current=$testing HTTP/1.0\r\nHost: $host\r\nConnection: Close\r\n\r\n";
                }
                if ($debug == TRUE){echo $req;}
                fputs ($conn, $req);
                while (!feof($conn)) {
                $tmp .= fgets ($conn,128);
                
                }
            fclose ($conn);
                
                do_test($tmp,$form['action'],$current);
                
                $tmp = '';
            }
        }
    }

}else if ($form['method'] = 'post'){

foreach($form['vars'] as $current){
        foreach($locator as $testing){
        $testing = urlencode($testing);
        $conn =  fsockopen ("$host", $port, $errno, $errstr, 30);
            if (!$conn) {
                echo "$errstr ($errno)\r\n";
            } else {
                $req="POST ".$form['action']." HTTP/1.0\r\nHost: $host\r\nContent-Type: application/x-www-form-urlencoded\r\nConnection: Close\r\nContent-Length: ".strlen($postit)."\r\n\r\n$postit\r\n\r\n";
                $postit = "$current=$testing" ;
                if ($debug == TRUE){echo $req;}
                fputs ($conn, $req);
                while (!feof($conn)) {
                $tmp .= fgets ($conn,128);
                }
            fclose ($conn);

                do_test($tmp,$form['action'],"POST: $current");
                $tmp = '';
            }
        }
    }


}


}
/**
* Catches and Parses HTML forms 
* @author KingOfSka <kingofska@gmail.com>
* @param string $page   Page to scan for forms
* @return Array
**/

function catch_forms($page){
array($form);
$data = get($page);
preg_match_all('#<form .+?>.+?</form>#is',$data['content'],$matches);
foreach ($matches[0] as $data['content']){
preg_match('#<form (.+?)>(.+?)</form>#is',$data['content'],$matches);
$form['setup'] = $matches[1];
$form['content'] = $matches[2];
preg_match('#method\s?=\s?["\']?(get|post)["\']?#i',$form['setup'],$matches);
if (isset($matches[1])){
    $form['method'] = $matches[1];
    }else{ 
    $form['method'] = 'get';
}
preg_match('#action\s?=\s?["\']?([^"\']*)["\']?#i',$form['setup'],$matches);
$form['action'] = $matches[1];
preg_match_all('#<input (.*)>#i',$form['content'],$input);
foreach($input[0] as $cur){
preg_match('#name\s?=\s?["\']?(\w*)["\']?#i',$cur,$matches);
$form['vars'][] = $matches[1];
}
print_r($form);
test_form($form);
}
}

function get_server_info(){
global $site_links;
array($server);
foreach($site_links as $link){
if(stripos($link,'.php')){ 
$right = $link;
break;
}
}
$data = get($right);
preg_match('#Server:\s?(\w.*)#',$data['headers'],$matches);
$server['software'] = $matches[1];
preg_match('#X-Powered-By:\s?(\w.*)#',$data['headers'],$matches);
if (isset($matches[1])){
$server['powered'] = $matches[1];
}
return $server;
}

function test_page($page){
global $checkedpages;


if (in_array($page,$checkedpages)){
return;
}


catch_forms($page);
$plinks = get_links($page,true);
foreach ($plins as $cur){
    test_link($cur);
}
$checkedpages[] = $page ;

}

    /**
     * Perform a simple GET request,returning an array containing 
     * server-sent headers and content
     *
     * @author KingOfSka <kingofska@gmail.com>
     * @param string $path Path to the resource to request
     * @param string $cookie Cookie string to pass along with the request (still to implement....)
     * @return Array
     **/

    function get($path = '/',$cookie = ''){
        global $host,$port,$debug,$reqmade,$checkedlinks;
        
        array($ret);
        $tmp = '';
        $conn =  fsockopen ("$host", $port, $errno, $errstr, 30);
        $reqmade++;
        
        if($path[0] != '/' AND stripos($path,'http://') === FALSE){$path = '/'.$path;}
            if (!$conn) {
                echo "$errstr ($errno)<br>\n";
            } else {
                if ($debug == TRUE){echo "GET $path HTTP/1.0\r\nHost: $host\r\n\r\n";}
                fputs ($conn, "GET $path HTTP/1.0\r\nHost: $host\r\nConnection: Close\r\n\r\n");
                while (!feof($conn)) {
                $tmp .= fgets ($conn,128);
                }
            fclose ($conn);
            }

//echo $tmp;
        preg_match('#HTTP\/1\.\d (\d\d\d)#',$tmp,$matches);
        
        if ($matches[1]!= 200){
            $ret = "HTTP Error Code N°".$matches['1'];
            if ($debug == TRUE){echo "Debug:\r\n$tmp<br/>\r\n";}
        }
        if ($matches[1]== 302 OR $matches[1] == 301){
            preg_match('#Location:(.*)#',$tmp,$matches);
            if (!in_array($matches[1],$checkedlinks)){
            
            return get($matches[1]);
            }
        }        
        $b = preg_split('#Content-Type: text/html#',$tmp);
        
        $ret['headers'] = $b[0];
        $ret['content'] = $b[1];
        if ($debug == TRUE){echo "Debug:\r\n".$ret['headers']."\r\n";}
    return $ret;
    }

    /**
     * Catches all the links in a webpage, checking they are not pointing to
     * files external at the host being scanned.
     *
     * @author KingOfSka <kingofska@gmail.com>
     * @return Array
     **/

    function get_links($data,$getpage = FALSE){
    global $host,$links;
        if ($getpage == TRUE){
        $tmp = get($data);
        $data = $tmp['content'];    
        }
        
        preg_match_all('#<a href=[\'"].+?[\'"].+?>#i',$data,$matches);
        
        foreach ($matches[0] as $current){
            
                
                preg_match('#<a href=["\'](.+?)["\'].+?>#i',$current,$matches);
                
                $current = $matches[1];
                if (is_valid_url($current)){
                if (stripos($current,$host) != FALSE OR stripos($current,'http://') === FALSE ){
                
                if ($current[0] == '?'){
                $current= 'index.php'.$current;

                }
            
                if (stripos($current,$host) === FALSE OR stripos($current,'http://') === FALSE){
                
                $current = "http://$host/$current";
                
                }
                if (!in_array($current,$links)){
                $retlinks[] = $current ;
                }
                }
            }
        }
    return array_unique($retlinks) ;
    }

    /**
     * Parse a link returning an array with the name of the file which 
     * the link is pointing to, and the GET variables passed trhough it.
     *
     * @author KingOfSka <kingofska@gmail.com>
     * @return Array
     * @param string $link Link to parse
     **/

    function parse_link($link){
        array($ret);
        
        
        $matches = explode('?',$link);
        $ret['action'] = $matches[0] ;
        $matches = explode('&',$matches[1]);
            foreach($matches as $cur){
            $matches = explode('=',$cur);
            $vars[] = $matches[0];
            }
        
        $ret['vars'] = $vars;
        
        return $ret;
    }
/**
 * Tests a given link echoing found vulnerabilities
 *
 * @author KingOfSka <kingofska@gmail.com>
 * @return void
 * @param $link Link to test
**/

function test_link($link){
global $host,$port,$locator,$result;

$ret = '';
$tmp = '';
$data = parse_link($link);
//$data['vars'] = array_merge($data['vars'],$additional_vars);
    foreach($data['vars'] as $current){
        foreach($locator as $testing){
        $testing = urlencode($testing);
        $conn =  fsockopen ("$host", $port, $errno, $errstr, 30);
            if (!$conn) {
                echo "$errstr ($errno)\r\n";
            } else {
                if (!stripos('?',$data['action'])){
                $req = "GET ".$data['action']."?$current=$testing HTTP/1.0\r\nHost: $host\r\nConnection: Close\r\n\r\n";
                }else{
                $req=  "GET ".$data['action']."&$current=$testing HTTP/1.0\r\nHost: $host\r\nConnection: Close\r\n\r\n";
                }
                fputs ($conn, $req);
                
                while (!feof($conn)) {
                $tmp .= fgets ($conn,128);
                
                }
            
            fclose ($conn);
                do_test($tmp,$data['action'],$current);
                
                $tmp ='';
            }
        }
    }
return;
}

/**
 * Removes empty item from a given array
 * 
 * @return Array
 * @param $array array to clean
**/

function clean_array($array) {
   foreach ($array as $index => $value) {
       if(is_array($array[$index])) $array[$index] = clean_array($array[$index]);
       if (empty($value) OR !is_valid_url($value)) unset($array[$index]);
       }
   return $array;
}

function getmicrotime(){
   list($usec, $sec) = explode(" ",microtime());
   return ((float)$usec + (float)$sec);
   }

function clean_url_array($array){
    foreach ($array as $cur){
    echo $cur;
        if(!is_valid_url($cur)) unset ($array[$cur]);    
    }
return $array;
}

function is_valid_url($url){

if (!eregi("^(http|https)+(:\/\/)+[a-z0-9_-]+\.+[a-z0-9_-]",$url)){

return FALSE;
}else{
return TRUE;
}
}

function do_test($data,$path,$var){
global $result;
if (stripos($data,'\'\';!--"<XSS>=') OR stripos($data,"\'\';--\"<XSS>=") OR stripos($data,'<XSS>')){

                $result['vuln']['xss'][]=$path."?$var=[XSS]";
            }
            
                
if (stripos($data,'You have an error in your SQL syntax')){
                $result['vuln']['sql'][]=$path."?$var=[SQL]";

    }



if (stripos($data,'Failed opening \'some_inexisistent_file_to_include.php\' for inclusion')){
    $result['vuln']['rfi'][]=$path."?$var=[RFI]";
}


return;
}

?>