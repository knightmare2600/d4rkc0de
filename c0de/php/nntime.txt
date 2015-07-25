<?
echo "<title>NNtime Proxy List</title>";
function proxylist($site){
$source=file_get_contents($site);
preg_match_all("/[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:[0-9]{2,4}/",$source,$matched);
return $matched[0];
}

$array=proxylist("http://www.nntime.com");
foreach($array as $tek){
$tek=str_replace("
","",$tek);
print $tek."<br>";
}
?> 