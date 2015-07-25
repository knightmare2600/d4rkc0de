code:
[ME@Machine]# cat mailer.php
<?php
$list = 'list';
$who = file($list);
$rep = array("\n" => "");
$msg = "\n
THis iS the OutGoing MEssAge
";

echo
"\n
E-mail List:$list
**********************
*SENDING MESSAGE
********************************
$msg
********************************\n
";

for($i = 0; $i <= 99999; $i++){
        if($who[$i] == ""){ $i = 99999; }else{
        echo ":\n:.\tSending to $who[$i]...\n";
        $to = strtr($who[$i], $rep);
        $headers = 'Return-Path: site.com' . "\r\n" . 'MIME-Version: 1.0' . "\r\n" . 'Content-type:
text/html; charset=iso-8859-1'  . "\r\n" . 'From: Robot_donotreply <Robot_donotreply@site.com>' . "\r\n" .
        'Reply-To: Robot_donotreply <Robot_donotreply@site.com>' . "\r\n" .
        'X-Mailer: smtpdx';
        mail($to, 'test mailer', $msg, $headers);
        }
}
echo "!Mail Sent!\n...\n";
?>
----------------------------------------------------
[ME@Machine]# php -q mailer.php


E-mail List:list
**********************
*SENDING MESSAGE
********************************


THis iS the OutGoing MEssAge

********************************

:
:.      Sending to email@email1.com
...
:
:.      Sending to email@email2.com
...
:
:.      Sending to email@email3.com
...
:
:.      Sending to email@email4.com
...
!Mail Sent!
... 