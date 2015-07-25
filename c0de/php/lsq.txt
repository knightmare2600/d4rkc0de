<?php
//Neutralisd - Excel data extractor.
define(db_host, "localhost");
define(db_user, "user");
define(db_pass, "password");
define(db_link, mysql_connect(db_host,db_user,db_pass)); 
define(db_name, "db-name");
define(db_table, "dk-table");
mysql_select_db(db_name); 


$select = "SELECT username, password, email FROM users";
$export = mysql_query($select);
$fields = mysql_num_fields($export);

for ($i = 0; $i < $fields; $i++) { 
    $header .= mysql_field_name($export, $i) . "\t"; 
} 

while($row = mysql_fetch_row($export)) {
    $line = ''; 
    foreach($row as $value) {                                             
        if ((!isset($value)) OR ($value == "")) { 
            $value = "\t"; 
        } else {
            $value = str_replace('"', '""', $value); 
            $value = '"' . $value . '"' . "\t"; 
        } 
        $line .= $value; 
    }
    $data .= trim($line)."\n"; 
} 
$data = str_replace("\r","",$data); 

if ($data == "") { 
    $data = "\n(0) Records Found!\n";                         
} 

header("Content-type: application/vnd.ms-excel "); 
header("Content-Disposition: attachment; filename=extraction.xls");
header("Pragma: no-cache"); 
header("Expires: 0");
print "$header\n$data";
?>
