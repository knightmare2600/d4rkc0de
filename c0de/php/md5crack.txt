HTML TAGS

MD5 Hash<br>
<FIELDSET>
<form action="index.php" method="post">
<input type="text" name="thash" size="32" maxlength="32"/>
<input type="submit" name="crack" value="Crack"/>
</form>
</FIELDSET>

Submit word<br>
<FIELDSET>
<form action="index.php" method="post">
<input type="text" name="tword"size="32"/>
<input type="submit" name="swsubmit" value="Submit"/>
</form>
</FIELDSET>
<hr>
HTML TAGS

<?php

if(isset($_POST['thash'])){
$hash = $_POST['thash'];
$dfile = "passes.txt";
if(strlen($hash)==32){
   echo "Attempting crack of MD5 hash - " . $hash . "<br><br>";
$file = fopen($dfile,"r") or exit("unable to open file");
while(!feof($file)){
$password = fgets($file);
$password = trim($password);
if($hash == md5($password)){
   echo "<b>" . $hash . ":" . $password . "</b><br>";
}
}
   echo "<br><br><b>Finished<b><br>";
fclose($file);
}
else{
   echo "<b>Invalid MD5 hash</b><br>";
   exit();
}
}
if(isset($_POST['tword'])){
$word = $_POST['tword'];
$dfile = "passes.txt";
echo "<br>Submitting word - <b>" . $word . "</b><br>";
dupcheck($dfile,$word);
$file = fopen($dfile,"a") or exit("Couldn't open " . $dfile);
fwrite($file,$word . "\n");
fclose($file);
}
function dupcheck($lfile,$lword){
$rfile = fopen($lfile,"r") or exit("Couldn't open " . $lfile);
while(!feof($rfile)){
$rword = fgets($rfile);
$rword = trim($rword);
if($rword == $lword){
exit("<br><br><b>Duplicate found<b> - " . $lword);
}
}
fclose($rfile);
}
?> 