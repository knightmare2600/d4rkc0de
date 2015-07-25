<?php



If ($action=="mysql"){

        #Grab email addresses from MySQL

        include "./mysql.info.php";

        if (!$sqlhost || !$sqllogin || !$sqlpass || !$sqldb || !$sqlquery){

        print "Please configure mysql.info.php with your MySQL information. All settings in this config file are required.";

        exit;

        }

        $db = mysql_connect($sqlhost, $sqllogin, $sqlpass) or die("Connection to MySQL Failed.");

        mysql_select_db($sqldb, $db) or die("Could not select database $sqldb");

        $result = mysql_query($sqlquery) or die("Query Failed: $sqlquery");

        $numrows = mysql_num_rows($result);



        for($x=0; $x<$numrows; $x++){

        $result_row = mysql_fetch_row($result);

        $oneemail = $result_row[0];

        $emaillist .= $oneemail."\n";

        }

        }



if ($action=="send"){

        $message = urlencode($message);

        $message = ereg_replace("%5C%22", "%22", $message);

        $message = urldecode($message);
        $message = stripslashes($message);
        $subject = stripslashes($subject);

}



?>
<?

if ($action=="send"){



        if (!$from && !$subject && !$message && !$emaillist){

        print "Please complete all fields before sending your message.";

        exit;

        }



        $allemails = split("\n", $emaillist);

        $numemails = count($allemails);



        #Open the file attachment if any, and base64_encode it for email transport

        If ($file_name){

                @copy($file, "./$file_name") or die("The file you are trying to upload couldn't be copied to the server");

                $content = fread(fopen($file,"r"),filesize($file));

                $content = chunk_split(base64_encode($content));

                $uid = strtoupper(md5(uniqid(time())));

                $name = basename($file);

        }



        for($x=0; $x<$numemails; $x++){

                $to = $allemails[$x];

                if ($to){

                $to = ereg_replace(" ", "", $to);

                $message = ereg_replace("&email&", $to, $message);

                $subject = ereg_replace("&email&", $to, $subject);

                print "Sending mail to $to.......";

                flush();

                $header = "From: $realname <$from>\r\nReply-To: $replyto\r\n";

                $header .= "MIME-Version: 1.0\r\n";

                If ($file_name) $header .= "Content-Type: multipart/mixed; boundary=$uid\r\n";

                If ($file_name) $header .= "--$uid\r\n";

                $header .= "Content-Type: text/$contenttype\r\n";

                $header .= "Content-Transfer-Encoding: 8bit\r\n\r\n";

                $header .= "$message\r\n";

                If ($file_name) $header .= "--$uid\r\n";

                If ($file_name) $header .= "Content-Type: $file_type; name=\"$file_name\"\r\n";

                If ($file_name) $header .= "Content-Transfer-Encoding: base64\r\n";

                If ($file_name) $header .= "Content-Disposition: attachment; filename=\"$file_name\"\r\n\r\n";

                If ($file_name) $header .= "$content\r\n";

                If ($file_name) $header .= "--$uid--";

                mail($to, $subject, "", $header);

                print "ok<br>";

                flush();

                }

                }



}

