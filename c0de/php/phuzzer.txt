<?php

/*

I can detect = 

<RFI>
include();
include("$string");
include "$string";
include $string;
INCLUDE();
INCLUDE("$string");
INCLUDE "$string";
INCLUDE $string;
define('STRING',$string);
define('STRING',"$string");
DEFINE('STRING',$string);
DEFINE('STRING',"$string");
</RFI>

<RCE>
dl($string);
dl("$string");
system($string);
system("$string");
exec($string);
exec("$string");
passthru($string);
passthru("$string");
shell_exec($string);
shell_exec("$string");
</RCE>

<FS>
copy($string,'string');
copy('string',$string);
copy($string,$string);
unlink($string);
unlink("$string");
file_get_contents($string);
file_get_contents("$string");
file($string);
file("$string");
fopen($string,$string);
fopen("$string",'string');
fopen('string',"$string");
fwrite($string,$string);
fwrite("$string",'string');
fwrite('string',"$string");
fputs($string,$string);
fputs("$string",'string');
fputs('string',"$string");
popen($string,$string);
popen("$string",'string');
popen('string',"$string");
touch($string);
touch("$string");
mkdir($string,$string);
mkdir("$string",'string');
mkdir('string',"$string");
</FS>

*/

if($argv[1]!=NULL)#BLXK August 12, 4:59:34
{
$data = file_get_contents($argv[1]);
$data_tmp = explode(';',$data);

$holes[0] = "Fuzzed $argv[1]";


function vuln($vuln)
{
 global $holes;
 global $string;
 

 array_push($holes,'[Unset String] - '.$string);
 array_push($holes,$vuln);
}


for($i=0;$data_tmp[$i]!=NULL;$i++)
{
/*#######

INCLUDE();
INCLUDE("$string");
INCLUDE "$string";
INCLUDE $string;

#######*/


 #INCLUDE();
 $tmp = explode('INCLUDE(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);
 
 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote File Include] INCLUDE('.$string.')'); }#BLXK August 12, 4:59:34
 }

 #INCLUDE("$string");
 $tmp = explode('INCLUDE("',$data_tmp[$i]);
 $tmp = explode('")',$tmp[1]);
 
 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote File Include] INCLUDE("'.$string.'")');}
 }

 #INCLUDE "$string";
 $tmp = explode('INCLUDE "',$data_tmp[$i]);
 $tmp = explode('"',$tmp[1]);
 
 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote File Include] "'.$string.'"'); }
 }

 #INCLUDE $string;
 $tmp = explode('INCLUDE ',$data_tmp[$i]);
 $tmp = explode(' ',$tmp[1]);
 
 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote File Include] '.$string); }
 }

/*#######

include();
include("$string");
include "$string";
include $string;

#######*/


 #include();
 $tmp = explode('include(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);
 
 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote File Include] include('.$string.')'); }
 }

 #include("$string");
 $tmp = explode('include("',$data_tmp[$i]);
 $tmp = explode('")',$tmp[1]);
 
 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote File Include] include("'.$string.'")');}
 }

 #include "$string";
 $tmp = explode('include "',$data_tmp[$i]);
 $tmp = explode('"',$tmp[1]);
 
 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote File Include] include "'.$string.'"'); }
 }

 #include $string;
 $tmp = explode('include ',$data_tmp[$i]);
 $tmp = explode(' ',$tmp[1]);
 
 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote File Include] include '.$string); }
 }


/*#######

DEFINE('STRING',$string);
DEFINE('STRING',"$string");

#######*/


 #DEFINE('STRING',$string);
 $tmp = explode('DEFINE(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);
 $tmp = explode(',',$tmp[0]);

 $string = $tmp[1];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset Define] DEFINE(*,'.$string.')'); }
 }


 #DEFINE('STRING',"$string");
 $tmp = explode('DEFINE(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);
 $tmp = explode(',',$tmp[0]);
 $tmp = explode('"',$tmp[1]);

 $string = $tmp[1];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset Define] DEFINE(*,"'.$string.'")'); }
 }

/*#######

define('STRING',$string);
define('STRING',"$string");

#######*/


 #define('STRING',$string);
 $tmp = explode('define(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);
 $tmp = explode(',',$tmp[0]);

 $string = $tmp[1];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset Define] define(*,'.$string.')'); }
 }


 #define('STRING',"$string");
 $tmp = explode('define(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);
 $tmp = explode(',',$tmp[0]);
 $tmp = explode('"',$tmp[1]);

 $string = $tmp[1];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset Define] define(*,"'.$string.'")'); }
 }


/*#######

dl($string);
dl("$string");

#######*/


 #dl($string);
 $tmp = explode('dl(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote Extension Load] dl('.$string.')'); }
 }


 #dl("$string");
 $tmp = explode('dl("',$data_tmp[$i]);
 $tmp = explode('")',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote Extension Load] dl("'.$string.'")'); }
 }

/*#######

system($string);
system("$string");

#######*/


 #system($string);
 $tmp = explode('system(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote Code Execution] system('.$string.')'); }
 }


 #system("$string");
 $tmp = explode('system("',$data_tmp[$i]);
 $tmp = explode('")',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote Code Execution] system("'.$string.'")'); }
 }

/*#######

exec($string);
exec("$string");

#######*/


 #exec($string);
 $tmp = explode('exec(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote Code Execution] exec('.$string.')'); }
 }


 #exec("$string");
 $tmp = explode('exec("',$data_tmp[$i]);
 $tmp = explode('")',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote Code Execution] exec("'.$string.'")'); }
 }


/*#######

passthru($string);
passthru("$string");

#######*/


 #passthru($string);
 $tmp = explode('passthru(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote Code Execution] passthru('.$string.')'); }
 }


 #passthru("$string");
 $tmp = explode('passthru("',$data_tmp[$i]);
 $tmp = explode('")',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote Code Execution] passthru("'.$string.'")'); }
 }


/*#######

shell_exec($string);
shell_exec("$string");

#######*/


 #shell_exec($string);
 $tmp = explode('shell_exec(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote Code Execution] shell_exec('.$string.')'); }
 }


 #shell_exec("$string");
 $tmp = explode('shell_exec("',$data_tmp[$i]);
 $tmp = explode('")',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote Code Execution] shell_exec("'.$string.'")'); }
 }

/*#######

copy($string,$string);
copy("$string",'string');
copy('string',"$string");

#######*/

 #copy($string,$string);
 $tmp = explode('copy(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);
 $tmp = explode(',',$tmp[0]);


 for($ii=0;$tmp[$ii]!=NULL;$ii++)
 {
  $string = $tmp[$ii];

  if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
  {
   if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
   { NULL; }else{ 
    if($ii!=0){ vuln('[Unset File System Cmd] copy(*,'.$string.')');
    }else{
     vuln('[Unset File System Cmd] copy('.$string.',*)');
    }
   }
  }
 }

 #copy("$string",'string');
 $tmp = explode('copy("',$data_tmp[$i]);
 $tmp = explode('",',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] copy("'.$string.'",*)'); }
 }#BLXK August 12, 4:59:34

 #copy('string',"$string");
 $tmp = explode('copy(',$data_tmp[$i]);
 $tmp = explode(',"',$tmp[1]);
 $tmp = explode('"',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] copy(*,"'.$string.'")'); }
 }

/*#######

unlink($string);
unlink("$string");

#######*/

 #unlink($string);
 $tmp = explode('unlink(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote File Removal] unlink('.$string.')'); }
 }

 #unlink("$string");
 $tmp = explode('unlink("',$data_tmp[$i]);
 $tmp = explode('")',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {#BLXK August 12, 4:59:34
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Remote File Removal] unlink("'.$string.'")'); }
 }

/*#######

file_get_contents($string);
file_get_contents("$string");

#######*/

 #file_get_contents($string);
 $tmp = explode('file_get_contents(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] file_get_contents('.$string.')'); }
 }

 #file_get_contents("$string");
 $tmp = explode('file_get_contents("',$data_tmp[$i]);
 $tmp = explode('")',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] file_get_contents("'.$string.'")'); }
 }

/*#######

file($string);
file("$string");

#######*/

 #file($string);
 $tmp = explode('file(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] file('.$string.')'); }
 }

 #file("$string");
 $tmp = explode('file("',$data_tmp[$i]);
 $tmp = explode('")',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] file("'.$string.'")'); }
 }

/*#######

fopen($string,$string);
fopen("$string",'string');
fopen('string',"$string");

#######*/

 #fopen($string,$string);
 $tmp = explode('fopen(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);
 $tmp = explode(',',$tmp[0]);


 for($ii=0;$tmp[$ii]!=NULL;$ii++)
 {
  $string = $tmp[$ii];

  if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
  {
   if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
   { NULL; }else{ 
    if($ii!=0){ vuln('[Unset File System Cmd] fopen(*,'.$string.')');
    }else{
     vuln('[Unset File System Cmd] fopen('.$string.',*)');
    }
   }
  }
 }

 #fopen("$string",'string');
 $tmp = explode('fopen("',$data_tmp[$i]);
 $tmp = explode('",',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] fopen("'.$string.'",*)'); }
 }

 #fopen('string',"$string");
 $tmp = explode('fopen(',$data_tmp[$i]);
 $tmp = explode(',"',$tmp[1]);
 $tmp = explode('"',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] fopen(*,"'.$string.'")'); }
 }

/*#######

fwrite($string,$string);
fwrite("$string",'string');
fwrite('string',"$string");

#######*/

 #fwrite($string,$string);
 $tmp = explode('fwrite(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);
 $tmp = explode(',',$tmp[0]);


 for($ii=0;$tmp[$ii]!=NULL;$ii++)
 {
  $string = $tmp[$ii];

  if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
  {
   if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
   { NULL; }else{ 
    if($ii!=0){ vuln('[Unset File System Cmd] fwrite(*,'.$string.')');
    }else{
     vuln('[Unset File System Cmd] fwrite('.$string.',*)');
    }
   }
  }
 }

 #fwrite("$string",'string');
 $tmp = explode('fwrite("',$data_tmp[$i]);
 $tmp = explode('",',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] fwrite("'.$string.'",*)'); }
 }

 #fwrite('string',"$string");
 $tmp = explode('fwrite(',$data_tmp[$i]);
 $tmp = explode(',"',$tmp[1]);
 $tmp = explode('"',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] fwrite(*,"'.$string.'")'); }
 }

/*#######

fputs($string,$string);
fputs("$string",'string');
fputs('string',"$string");

#######*/

 #fputs($string,$string);
 $tmp = explode('fputs(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);
 $tmp = explode(',',$tmp[0]);


 for($ii=0;$tmp[$ii]!=NULL;$ii++)
 {
  $string = $tmp[$ii];

  if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
  {
   if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
   { NULL; }else{ 
    if($ii!=0){ vuln('[Unset File System Cmd] fputs(*,'.$string.')');
    }else{
     vuln('[Unset File System Cmd] fputs('.$string.',*)');
    }
   }
  }
 }

 #fputs("$string",'string');
 $tmp = explode('fputs("',$data_tmp[$i]);
 $tmp = explode('",',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] fputs("'.$string.'",*)'); }
 }

 #fputs('string',"$string");
 $tmp = explode('fputs(',$data_tmp[$i]);
 $tmp = explode(',"',$tmp[1]);
 $tmp = explode('"',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] fputs(*,"'.$string.'")'); }
 }

/*#######

popen($string,$string);
popen("$string",'string');
popen('string',"$string");

#######*/

 #popen($string,$string);
 $tmp = explode('popen(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);
 $tmp = explode(',',$tmp[0]);


 for($ii=0;$tmp[$ii]!=NULL;$ii++)
 {
  $string = $tmp[$ii];

  if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
  {
   if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
   { NULL; }else{ 
    if($ii!=0){ vuln('[Unset File System Cmd] popen(*,'.$string.')');
    }else{
     vuln('[Unset File System Cmd] popen('.$string.',*)');
    }
   }
  }
 }

 #popen("$string",'string');
 $tmp = explode('popen("',$data_tmp[$i]);
 $tmp = explode('",',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] popen("'.$string.'",*)'); }
 }

 #popen('string',"$string");
 $tmp = explode('popen(',$data_tmp[$i]);
 $tmp = explode(',"',$tmp[1]);
 $tmp = explode('"',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] popen(*,"'.$string.'")'); }
 }

/*#######

touch($string);
touch("$string");

#######*/


 #touch($string);
 $tmp = explode('touch(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] touch('.$string.')'); }
 }


 #touch("$string");
 $tmp = explode('touch("',$data_tmp[$i]);
 $tmp = explode('")',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] touch("'.$string.'")'); }
 }

/*#######

mkdir($string,$string);
mkdir("$string",'string');
mkdir('string',"$string");

#######*/

 #mkdir($string,$string);
 $tmp = explode('mkdir(',$data_tmp[$i]);
 $tmp = explode(')',$tmp[1]);
 $tmp = explode(',',$tmp[0]);


 for($ii=0;$tmp[$ii]!=NULL;$ii++)
 {
  $string = $tmp[$ii];

  if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
  {
   if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
   { NULL; }else{ 
    if($ii!=0){ vuln('[Unset File System Cmd] mkdir(*,'.$string.')');
    }else{
     vuln('[Unset File System Cmd] mkdir('.$string.',*)');
    }
   }
  }
 }

 #mkdir("$string",'string');
 $tmp = explode('mkdir("',$data_tmp[$i]);
 $tmp = explode('",',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] mkdir("'.$string.'",*)'); }
 }

 #mkdir('string',"$string");
 $tmp = explode('mkdir(',$data_tmp[$i]);
 $tmp = explode(',"',$tmp[1]);
 $tmp = explode('"',$tmp[1]);

 $string = $tmp[0];
 if(strstr($string,'$')!=NULL && strstr($string,'"')==NULL && strstr($string,'\'')==NULL)
 {
  if(strstr($data,$string.' =')!=NULL||strstr($data,$string.' = ')!=NULL||strstr($data,$string.'= ')!=NULL)
  { NULL; }else{ vuln('[Unset File System Cmd] mkdir(*,"'.$string.'")'); }
 }

}

strtr(print_r($holes),'Array','VULNS');

}else{
 if(is_file('fuzz.sh')){ unlink('fuzz.sh');}

 touch('fuzz.sh');
 #BLXK August 12, 4:59:34
 echo "Building Database -R\n";

 $files= explode("\n",shell_exec('find ./ | egrep \'*.php\''));
 for($i=0;$files[$i]!=NULL;$i++)
 {
  if(strstr($files[$i],$argv[0])==NULL)
  {
   echo "db_add->$files[$i]\n";
   shell_exec("echo \"php $argv[0] $files[$i]\n\" >> fuzz.sh");
  }
 }

 echo "Fuzzing started!\n";

 system('sh fuzz.sh');
}
?>