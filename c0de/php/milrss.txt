code:
<?php
#goast BHF

#modules
define('MILW0RM','10:milw0rm.com/rss.php:Milw0rm');
define('ZONEH','15:www.zone-h.org/index2.php?option=com_rss&no_html=1:ZONE-H');

function goast_rss($type,$i)
{
 $type = explode(':',$type);

 $xx = file_get_contents('http://'.$type[1]);

 if($type[0]>$i){'ERROR:The MAX listing of module '.$type[3].' is set to '.$type[0];}

 $CRUNCH = 0;

 while($CRUNCH<=$type[0])
 {
  $x[0] = explode('</item>',$xx);
  $x[1] = explode('<item>',$x[0][$CRUNCH]);
  $x[2] = explode('title',$x[1][1]);
  $x[3] = explode('link',$x[1][1]);

  $xtitle = substr($x[2][1],1);$xtitle = substr($xtitle,0,strlen($xtitle)-2);
  $xurl = substr($x[3][1],1);$xurl = substr($xurl,0,strlen($xurl)-2);

  $out = "<a href='$xurl'>$xtitle</a>";

  $CRUNCH+=1;
  $data[$CRUNCH] = $out;
 }

 return $data[$i];
}

echo goast_rss(MILW0RM,1).'<p />';
echo goast_rss(MILW0RM,2).'<p />';
echo goast_rss(ZONEH,3).'<p />';

?>