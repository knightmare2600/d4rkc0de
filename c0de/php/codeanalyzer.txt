code:
<!--
*****************************************************
A source code analyzer. Searches through code in this case php files
and finds possible vulnerable syntax. This code uses (3) arrays to store
the strings to search for & one last function for custom on the fly
searches...you could even use it to search any file for any string
with minor mods.

SION
*****************************************************
-->
<html>
<title>PHP Source Analyzer</title>
<head>
<script language="JavaScript">
function mouseDown_Action(c_id) {
   var obj = document.getElementById(c_id);
   if (obj.style.visibility == 'hidden') {
      obj.style.visibility = 'visible';
      obj.style.position = 'static';
   } else {
      obj.style.visibility = 'hidden';
      obj.style.position = 'absolute';
   }
}
function mouseOver_Action(v_id, color) {
   var obj = document.getElementById(v_id);
   obj.style.backgroundColor = color;
}
function mouseOut_Action(v_id, color) {
   var obj = document.getElementById(v_id);
   obj.style.backgroundColor = color;
}

</script>
<style type="text/css">
a:link {text-decoration:none; color: #FFCCCC}
a:visited {text-decoration:none;color: #FFCCCC}
a:hover {text-decoration:none;color: #FFCCCC}
a:active {text-decoration:none;color: #FFCCCC}
a:focus {outline-style: none;}
body {background-color: #000; margin: 4; padding: 0;}
.main_window {
   width:99%;
   border-style:solid;
   border-color: #ccc;
   border-width: 1px;
   padding: 5 5 15 5;
   background-color: #000033;
}
.title_window {
   width: 90%; 
   height: auto;
   background-color: #330099;
   text-align: center;
   padding: 5 0 5 0;
   margin: 0 0 10 0;
   border-style: solid;
   border-color: #CCCCFF;
   border-width: 1px;
   font-family: impact;
   font-size: 30;
   color: #FFF;
}
.file_window {
   width: 88%; 
   background-color: #339933;
   text-align: left;
   padding: 1 0 1 10;
   margin: 10 0 3 0;
   border-style: solid;
   border-color: #66CC66;
   border-width: 1px;
   color: #CCFFCC;
}
.rfi_window {
   width: 84%; 
   background-color: #000   ;
   text-align: left;
   padding: 1 0 1 10;
   margin: 0 0 3 0;
   border-style: solid;
   border-color: #FF3366;
   border-width: 1px;
   color: #FFCCCC;
   text-decoration:none;
}
.sql_window {
   width: 84%; 
   background-color: #000   ;
   text-align: left;
   padding: 1 0 1 10;
   margin: 0 0 3 0;
   border-style: solid;
   border-color: #3399FF;
   border-width: 1px;
   color: #99CCFF;
   text-decoration:none;
}
.rce_window {
   width: 84%; 
   background-color: #000   ;
   text-align: left;
   padding: 1 0 1 10;
   margin: 0 0 3 0;
   border-style: solid;
   border-color: #FF9933;
   border-width: 1px;
   color: #FFCC99;
   text-decoration:none;
}
.code_window { 
   width: 80%;
   background-color: #333;
   text-align: left;
   padding: 10 10 10 10;
   margin: 5 0 10 0;
   border-style: solid;
   border-color: #003399;
   border-width: 1px;
   color: #CCCCFF;
   visibility:hidden;
   position: absolute;
}
INPUT.user_input {
   margin: 0 0 5 0;
   padding: 0 2 0 2;
   background-color: #333366;
   border-style: solid;
   border-color: #CCCCFF;
   border-width: 1px;
   color: #CCCCFF;
}
INPUT.button {
   margin: 0 0 5 0;
   background-color: #333366;
   border-style: solid;
   border-color: #CCCCFF;
   border-width: 1px;
   color: #CCCCFF;
}
LABEL.button {
   margin: 0 5 0 4;
   color: #CCCCFF;
}
SELECT.user_select {
   margin: 0 0 5 0;
   background-color: #333366;
   border-style: solid;
   border-color: #CCCCFF;
   border-width: 1px;
   color: #CCCCFF;
}
</style>
</head>
<body onload="makerequest('analyze.php', 'analyzing');return false;">
<center>
<div class="main_window">
<div class="title_window">PHP Source Analyzer</div>

<FORM name="user_form" action="index.php" method="get">
   <SELECT id="user_select" class="user_select" name="search_style" onmouseover="javascript:mouseOver_Action('user_select', '#333399');" onmouseout="javascript:mouseOut_Action('user_select', '#333366');">
      <OPTION <?php if($_GET["search_style"] == "Directory") { ?> selected="selected" <?php } ?>>Directory</OPTION>
      <OPTION <?php if($_GET["search_style"] == "File") { ?> selected="selected" <?php } ?>>File</OPTION>
   </SELECT>
   <INPUT id="user_input" class="user_input" value="" name="source_dir" size="80" onmouseover="javascript:mouseOver_Action('user_input', '#333399');" onmouseout="javascript:mouseOut_Action('user_input', '#333366');">
                                                             
   <INPUT id="analyze" class="button" value="Analyse" type="submit" onmouseover="javascript:mouseOver_Action('analyze', '#333399');" onmouseout="javascript:mouseOut_Action('analyze', '#333366');">
   <INPUT id="reset" class="button" type="reset" onmouseover="javascript:mouseOver_Action('reset', '#333399');" onmouseout="javascript:mouseOut_Action('reset', '#333366');"><BR>
   <INPUT class="button" type="checkbox" name="RFI"<?php if($_GET["RFI"] == "on") { echo "checked"; }?>><LABEL class="button">Remote File Inc.</LABEL>
   <INPUT class="button" type="checkbox" name="SQL"<?php if($_GET["SQL"] == "on") { echo "checked"; }?>><LABEL class="button">SQL</LABEL>
   <INPUT class="button" type="checkbox" name="RCE"<?php if($_GET["RCE"] == "on") { echo "checked"; }?>><LABEL class="button">Remote Command Execute</LABEL>


<FIELDSET style='color:#CCCCFF; border-width:1; border-color:#CCCCFF; width:50%;background-color:#333366; margin:0 0 5 0'>
<LEGEND>Custum Search</LEGEND>
<LABEL class="button">Search String: </LABEL><INPUT id="custom_search" class="user_input"  value="<?php if(isset($_GET['custom_search'])) { echo $_GET['custom_search']; } ?>"name="custom_search" size="80" onmouseover="javascript:mouseOver_Action('custom_search', '#333399');" onmouseout="javascript:mouseOut_Action('custom_search', '#333366');" style='margin:0;'>
</FIELDSET>
</FORM>
<?php

/*----------------------------------------------------------------------------------------------
DIRECTORY RECURSION FUNCTION
-------------------------------------------------------------------------------------------------*/
if((!isset($_GET["source_dir"])) or ($_GET["source_dir"] == "")) { ?><div class="sql_window">[INFO] Please enter a directory [INFO]</div><?php die; }
if(($_GET["search_style"] == "Directory") and (!is_dir($_GET["source_dir"]))) {
   ?><div class="rfi_window">[Error] <?php echo " " . $_GET["source_dir"] . " "?>does not exist or is not a directory [Error]</div><?php die;
} else if (($_GET["search_style"] == "File") and (!is_file($_GET["source_dir"]))) {
   ?><div class="rfi_window">[Error] <?php echo " " . $_GET["source_dir"] . " "?>does not exist or is not a file [Error]</div><?php die;
}

$base_dir = $_GET["source_dir"] . "\\";
$dir_listing = array(0 => $base_dir);               //Create array for holding dir_listing first entry is user argument
$php_listing = array();                           //Create array for holding php files found in search
$x = 0;                                       //set counter

if($_GET["search_style"] == "Directory") {
while($x < count($dir_listing)) {                     //Loop while the counter is less or equal to array count
$curr_directory = $dir_listing[$x];                     //set curr_directory
$dir_handle[$x] = opendir($curr_directory);               //set the directory handle for opening the dir. according to the counter
   while(false !== ($file = readdir($dir_handle[$x]))) {      //read directory listing and loop till the end
      $curr_file = $curr_directory . $file;
      if(is_dir($curr_file)) {            //check if its a directory
         if(($file != ".") && ($file != "..")) {         //check if its a hidden dire.
            $dir_listing[count($dir_listing)] = $curr_file . "\\";   //add to array . using count adds appends it count is not based on 0 start
         }
      }
      if(is_file($curr_file)) {               //Check if its a file
         if(substr_count($file, ".php")) {      //Check if its a php file
            $php_listing[count($php_listing)] = $curr_file;         //add to files found array php_listing
         }
      }
   }
   closedir($dir_handle[$x]);         //close handle
   $x++;                     //itterate count
}
} else {
   $php_listing[count($php_listing)] = $base_dir;
}
/*-------------------------------------------------------------------------------------------
SOURCE SYNTAX SEARCH FUNCTION
--------------------------------------------------------------------------------------------*/   
//Array holding all the strings to search for
if($_GET['custom_search'] <> NULL) {            //Check to see if custome search is set to something other than nothing
   $custom_search = "on";                     //Set custom search on
   $vuln_custom_syntax = $_GET['custom_search'];      //Get was custom search string contains
   $vuln_custom_syntax = explode(',',  $vuln_custom_syntax);      //seperate everything in custom search into an array
   }

//Arrays Containing the most common strings to search for
$vuln_rfi_syntax = array("require", "include", "empty", "readfile", "fread", "fwrite", "writefile", "fopen","_GET", "_POST", "_SESSION", "_REQUEST", "_USER", "eval");
$vuln_sql_syntax = array("sql", "dbquery", "query", "WHERE", "SELECT", "DELETE", "INSERT");
$vuln_rce_syntax = array("popen", "system", "eval", "passthru");
      
         
$vuln_count = 1;      //keeps track of the vulnerablities for the xhtml variables to pass to javascript
for($z=0; $z < count($php_listing); $z++) {               
   $vuln_found = array();            
   $filename = $php_listing[$z];      //holds the file to search
   $handle = fopen($filename, "r");                                 //opens file for reading only
   $contents = fread($handle, filesize($filename));                     //reads all content to $contents
   
?>
<!--New File Started-->
<div class='file_window'>Filename:<?php echo " " .  $filename ?></div>
<?php
   fclose($handle);                                             //closes file
   $exp_content = explode("\n", $contents);                           //seperate each line of the file into diff. array keys
   
   for($i=0; $i<= count($exp_content); $i++) {                           //loop until the end of the array
      if(($exp_content[$i] <> "")                                    //check to see if the line is empty, and for unwanted lines comments and such
         and (!strstr($exp_content[$i], "//"))                        //check to see if the line is a comment
         and (!strstr($exp_content[$i], "/*"))
         and (!strstr($exp_content[$i], "* "))
         ) {                                 
      $exp_content[$i] = strip_tags($exp_content[$i]);                  //strip all html tags before printing out
//#########################################################################################
// THIS FOLLOWING FOR LOOP CHECKS FOR CUSTOM SEARCH STRINGS PROVIDED BY THE USER
// It loops through each vulnerability for the current line of code from exp_content
// same loop as above with a different array. This seperates
//#########################################################################################
if($custom_search == "on") {
      for($x=0; $x < count($vuln_custom_syntax); $x++) {                     //loop through the vuln. array
            if(substr_count($exp_content[$i], $vuln_custom_syntax[$x])) {         //check and see if the vulnerable string is found
               $vuln_line = "line# " . $i . ":  " . $exp_content[$i] . "\n\r\n\r";   //hold vulnerable line found in syntax: Line$ code
               if (!array_search($vuln_line, $vuln_found)){            //check to see if it exists already or was already found
                  $vuln_found[count($vuln_found)] = $vuln_line;         //if not then add to vuln_found array for future checks
               ?>
                  <a border="0" onmouseover="javascript:mouseOver_Action('v<?php echo $vuln_count?>', '#CC6600');" onmouseout="javascript:mouseOut_Action('v<?php echo $vuln_count?>', '#000');" onmousedown="javascript:mouseDown_Action('c<?php echo $vuln_count?>');"><div id="v<?php echo $vuln_count?>" class="rce_window"><?php echo $vuln_line ?>
                  <div id="c<?php echo $vuln_count?>" class="code_window"  style="visibility:hidden">
               <?php
               for($y=0; $y <= 20; $y++) {                        //print the previous/ next 5 lines of code
                     echo strip_tags($exp_content[($i - 11) + $y]) . "<br>";         
                  }
?>
   </div></div></a>
<?php
}
$vuln_count++;
            }
         }
}
//#########################################################################################
// THIS FOLLOWING FOR LOOP CHECKS FOR REMOTE FILE INCLUSION VULNERABILITES
// It loops through each vulnerability for the current line of code from exp_content
//    it also adds it to vuln_found array to double check and see if its a duplicate line. sometimes more than one word is found in a line
//    after it finds a line it prints it out. or at least allows the html to do its thing with the xhtml in it.
//   At the end it prints out the next 20 and it increments the exp_content for not searching (since we already can see it)
//   Then it increments the vuln_count counter which designates the counts on the xhtml
//#########################################################################################
if($_GET["RFI"] == "on") {
      for($x=0; $x < count($vuln_rfi_syntax); $x++) {                     //loop through the vuln. array
            if(substr_count($exp_content[$i], $vuln_rfi_syntax[$x])) {         //check and see if the vulnerable string is found
               $vuln_line = "line# " . $i . ":  " . $exp_content[$i] . "\n\r\n\r";   //hold vulnerable line found in syntax: Line$ code
               if (!array_search($vuln_line, $vuln_found)){            //check to see if it exists already or was already found
                  $vuln_found[count($vuln_found)] = $vuln_line;         //if not then add to vuln_found array for future checks
               ?>
                  <a border="0" onmouseover="javascript:mouseOver_Action('v<?php echo $vuln_count?>', '#CC0000');" onmouseout="javascript:mouseOut_Action('v<?php echo $vuln_count?>', '#000');" onmousedown="javascript:mouseDown_Action('c<?php echo $vuln_count?>');"><div id="v<?php echo $vuln_count?>" class="rfi_window"><?php echo $vuln_line ?>
                  <div id="c<?php echo $vuln_count?>" class="code_window"  style="visibility:hidden">
               <?php
               for($y=0; $y <= 20; $y++) {                        //print the previous/ next 5 lines of code
                     echo strip_tags($exp_content[$i + $y]) . "<br>";         
                  }
?>
   </div></div></a>
<?php
}
$vuln_count++;
            }
         }
}
//#########################################################################################
// THIS FOLLOWING FOR LOOP CHECKS FOR SQL VULNERABILITES
// It loops through each vulnerability for the current line of code from exp_content
// same loop as above with a different array. This seperates
//#########################################################################################
if($_GET["SQL"] == "on") {
   for($x=0; $x < count($vuln_sql_syntax); $x++) {                     //loop through the vuln. array
            if(substr_count($exp_content[$i], $vuln_sql_syntax[$x])) {         //check and see if the vulnerable string is found
               $vuln_line = "line# " . $i . ":  " . $exp_content[$i] . "\n\r\n\r";   //hold vulnerable line found in syntax: Line$ code
               if (!array_search($vuln_line, $vuln_found)){            //check to see if it exists already or was already found
                  $vuln_found[count($vuln_found)] = $vuln_line;         //if not then add to vuln_found array for future checks
               ?>
                  <a border="0" onmouseover="javascript:mouseOver_Action('v<?php echo $vuln_count?>', '#666699');" onmouseout="javascript:mouseOut_Action('v<?php echo $vuln_count?>', '#000');" onmousedown="javascript:mouseDown_Action('c<?php echo $vuln_count?>');"><div id="v<?php echo $vuln_count?>" class="sql_window"><?php echo $vuln_line ?>
                  <div id="c<?php echo $vuln_count?>" class="code_window"  style="visibility:hidden">
               <?php
               for($y=0; $y <= 20; $y++) {                        //print the previous/ next 5 lines of code
                     echo strip_tags($exp_content[$i + $y]) . "<br>";         
                  }
?>
   </div></div></a>
<?php
}
$vuln_count++;
            }
         }
}
//#########################################################################################
// THIS FOLLOWING FOR LOOP CHECKS FOR REMOTE COMMAND EXECUTION VULNERABILITES
// It loops through each vulnerability for the current line of code from exp_content
// same loop as above with a different array. This seperates
//#########################################################################################
if($_GET["RCE"] == "on") {
      for($x=0; $x < count($vuln_rce_syntax); $x++) {                     //loop through the vuln. array
            if(substr_count($exp_content[$i], $vuln_rce_syntax[$x])) {         //check and see if the vulnerable string is found
               $vuln_line = "line# " . $i . ":  " . $exp_content[$i] . "\n\r\n\r";   //hold vulnerable line found in syntax: Line$ code
               if (!array_search($vuln_line, $vuln_found)){            //check to see if it exists already or was already found
                  $vuln_found[count($vuln_found)] = $vuln_line;         //if not then add to vuln_found array for future checks
               ?>
                  <a border="0" onmouseover="javascript:mouseOver_Action('v<?php echo $vuln_count?>', '#CC6600');" onmouseout="javascript:mouseOut_Action('v<?php echo $vuln_count?>', '#000');" onmousedown="javascript:mouseDown_Action('c<?php echo $vuln_count?>');"><div id="v<?php echo $vuln_count?>" class="rce_window"><?php echo $vuln_line ?>
                  <div id="c<?php echo $vuln_count?>" class="code_window"  style="visibility:hidden">
               <?php
               for($y=0; $y <= 20; $y++) {                        //print the previous/ next 5 lines of code
                     echo strip_tags($exp_content[($i - 11) + $y]) . "<br>";         
                  }
?>
   </div></div></a>
<?php
}
$vuln_count++;
            }
         }
}
      }
   }
}
?>
</div>
</center>
</body>
</html> 