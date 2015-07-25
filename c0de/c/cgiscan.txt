/* ---------------------------------------------------------------------- */
/* CGI scanner v1.34, m0dify and recode by su1d sh3ll //UnlG 1999         */
/* Tested on Slackware linux with kernel 2.0.35;RH 5.2(2.0.36);           */
/*           FreeBSD 2.2.2-3.1;IRIX 5.3                                   */
/* Source c0de by [CKS & Fdisk]                                           */
/* gr33tz to: Packet St0rm and Ken, ADM crew, ech0 security and CKS, ch4x,*/
/*            el8.org users, #c0de, rain.forest.puppy/[WT], MnemoniX ,    */
/*            hypoclear of lUSt,codex ;-) , K.A.L.U.G.                    */
/* fuck to: www.hackzone.ru , HDT...  CHC fuck u 2 llamaz-scr1pt k1dd1ez  */
/*          NATO and bill klinton  <---- double fuck! :-) huh             */
/* c0ming s00n: add-on for CGI scanner - for scan "C" class subnet & logs */
/* -----------------------------------------------[12:00 13.05.99  UnlG]- */

#include <fcntl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <netdb.h>
#include <ctype.h>
#include <arpa/nameser.h>
#include <sys/stat.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>

void main(int argc, char *argv[])
{
 int sock,debugm=0;
 struct in_addr addr;
 struct sockaddr_in sin;
 struct hostent *he;
 unsigned long start;
 unsigned long end;
 unsigned long counter;
 char foundmsg[] = "200";
 char *cgistr;
 char buffer[1024];
 int count=0;
 int numin;
 char cgibuff[1024];
 char *buff[100];    /* Don't u think 100 is enought?  ;-)*/
 char *cginame[100]; /* Don't u think 100 is enought? */

 buff[1] = "GET /cgi-bin/unlg1.1 HTTP/1.0\n\n";

 /* v0rt-fu when u modify source, check this first line.... that's my 8-)   */

 buff[2] = "GET /cgi-bin/rwwwshell.pl HTTP/1.0\n\n";
 buff[3] = "GET /cgi-bin/phf HTTP/1.0\n\n";    
 buff[4] = "GET /cgi-bin/Count.cgi HTTP/1.0\n\n";
 buff[5] = "GET /cgi-bin/test-cgi HTTP/1.0\n\n";
 buff[6] = "GET /cgi-bin/nph-test-cgi HTTP/1.0\n\n";
 buff[7] = "GET /cgi-bin/php.cgi HTTP/1.0\n\n";
 buff[8] = "GET /cgi-bin/handler HTTP/1.0\n\n";
 buff[9] = "GET /cgi-bin/webgais HTTP/1.0\n\n";
 buff[10] = "GET /cgi-bin/websendmail HTTP/1.0\n\n";
 buff[11] = "GET /cgi-bin/webdist.cgi HTTP/1.0\n\n";
 buff[12] = "GET /cgi-bin/faxsurvey HTTP/1.0\n\n";
 buff[13] = "GET /cgi-bin/htmlscript HTTP/1.0\n\n";
 buff[14] = "GET /cgi-bin/pfdispaly.cgi HTTP/1.0\n\n";
 buff[15] = "GET /cgi-bin/perl.exe HTTP/1.0\n\n";
 buff[16] = "GET /cgi-bin/wwwboard.pl HTTP/1.0\n\n";
 buff[17] = "GET /cgi-bin/www-sql HTTP/1.0\n\n";
 buff[18] = "GET /cgi-bin/view-source HTTP/1.0\n\n";
 buff[19] = "GET /cgi-bin/campas HTTP/1.0\n\n";
 buff[20] = "GET /cgi-bin/aglimpse HTTP/1.0\n\n";
 buff[21] = "GET /cgi-bin/glimpse HTTP/1.0\n\n";
 buff[22] = "GET /cgi-bin/man.sh HTTP/1.0\n\n";
 buff[23] = "GET /cgi-bin/AT-admin.cgi HTTP/1.0\n\n";
 buff[24] = "GET /cgi-bin/filemail.pl HTTP/1.0\n\n";
 buff[25] = "GET /cgi-bin/maillist.pl HTTP/1.0\n\n";
 buff[26] = "GET /cgi-bin/jj HTTP/1.0\n\n";
 buff[27] = "GET /cgi-bin/info2www HTTP/1.0\n\n";
 buff[28] = "GET /cgi-bin/files.pl HTTP/1.0\n\n"; 
 buff[29] = "GET /cgi-bin/finger HTTP/1.0\n\n";
 buff[30] = "GET /cgi-bin/bnbform.cgi HTTP/1.0\n\n";
 buff[31] = "GET /cgi-bin/survey.cgi HTTP/1.0\n\n";
 buff[32] = "GET /cgi-bin/AnyForm2 HTTP/1.0\n\n";
 buff[33] = "GET /cgi-bin/textcounter.pl HTTP/1.0\n\n";
 buff[34] = "GET /cgi-bin/classifieds.cgi HTTP/1.0\n\n";
 buff[35] = "GET /cgi-bin/environ.cgi HTTP/1.0\n\n";
 buff[36] = "GET /cgi-bin/wrap HTTP/1.0\n\n";
 buff[37] = "GET /cgi-bin/cgiwrap HTTP/1.0\n\n";
 buff[38] = "GET /cgi-bin/guestbook.cgi HTTP/1.0\n\n";
 buff[39] = "GET /_vti_pvt/service.pwd HTTP/1.0\n\n";
 buff[40] = "GET /_vti_pvt/users.pwd HTTP/1.0\n\n";
 buff[41] = "GET /_vti_pvt/authors.pwd HTTP/1.0\n\n";
 buff[42] = "GET /_vti_pvt/administrators.pwd HTTP/1.0\n\n";
 buff[43] = "GET /_vti_pvt/shtml.dll HTTP/1.0\n\n";
 buff[44] = "GET /_vti_pvt/shtml.exe HTTP/1.0\n\n";
 buff[45] = "GET /cgi-dos/args.bat HTTP/1.0\n\n";
 buff[46] = "GET /cgi-win/uploader.exe HTTP/1.0\n\n";
 buff[47] = "GET /cgi-bin/rguest.exe HTTP/1.0\n\n";
 buff[48] = "GET /cgi-bin/wguest.exe HTTP/1.0\n\n";
 buff[49] = "GET /scripts/issadmin/bdir.htr HTTP/1.0\n\n";
 buff[50] = "GET /scripts/CGImail.exe HTTP/1.0\n\n";
 buff[51] = "GET /scripts/tools/newdsn.exe HTTP/1.0\n\n";
 buff[52] = "GET /scripts/fpcount.exe HTTP/1.0\n\n";
 buff[53] = "GET /cfdocs/expelval/openfile.cfm HTTP/1.0\n\n";
 buff[54] = "GET /cfdocs/expelval/exprcalc.cfm HTTP/1.0\n\n";
 buff[55] = "GET /cfdocs/expelval/displayopenedfile.cfm HTTP/1.0\n\n";
 buff[56] = "GET /cfdocs/expelval/sendmail.cfm HTTP/1.0\n\n";
 buff[57] = "GET /iissamples/exair/howitworks/codebrws.asp HTTP/1.0\n\n"; 
 buff[58] = "GET /iissamples/sdk/asp/docs/codebrws.asp HTTP/1.0\n\n";
 buff[59] = "GET /search97.vts HTTP/1.0\n\n";
 buff[60] = "GET /carbo.dll HTTP/1.0\n\n"; /* we have at archive about 70 CGi ,
                                                                   rule? ;-) */

 cginame[1] = "UnlG - backd00r ";
 cginame[2] = "THC - backd00r  ";
 cginame[3] = "phf..classic :) ";
 cginame[4] = "Count.cgi       ";
 cginame[5] = "test-cgi        ";
 cginame[6] = "nph-test-cgi    ";
 cginame[7] = "php.cgi         ";
 cginame[8] = "handler         ";
 cginame[9] = "webgais         ";
 cginame[10] = "websendmail     ";
 cginame[11] = "webdist.cgi     ";
 cginame[12] = "faxsurvey       ";
 cginame[13] = "htmlscript      ";
 cginame[14] = "pfdisplay       ";
 cginame[15] = "perl.exe        ";
 cginame[16] = "wwwboard.pl     ";
 cginame[17] = "www-sql         ";
 cginame[18] = "view-source     ";
 cginame[19] = "campas          ";
 cginame[20] = "aglimpse        ";
 cginame[21] = "glimpse         ";
 cginame[22] = "man.sh          ";
 cginame[23] = "AT-admin.cgi    ";
 cginame[24] = "filemail.pl     ";
 cginame[25] = "maillist.pl     ";
 cginame[26] = "jj              ";
 cginame[27] = "info2www        ";
 cginame[28] = "files.pl        ";
 cginame[29] = "finger          ";
 cginame[30] = "bnbform.cgi     ";
 cginame[31] = "survey.cgi      ";
 cginame[32] = "AnyForm2        ";
 cginame[33] = "textcounter.pl  ";
 cginame[34] = "classifields.cgi";
 cginame[35] = "environ.cgi     ";
 cginame[36] = "wrap            ";
 cginame[37] = "cgiwrap         ";
 cginame[38] = "guestbook.cgi   ";
 cginame[39] = "service.pwd     ";
 cginame[40] = "users.pwd       ";
 cginame[41] = "authors.pwd     ";
 cginame[42] = "administrators  ";
 cginame[43] = "shtml.dll       ";
 cginame[44] = "shtml.exe       ";
 cginame[45] = "args.bat        ";
 cginame[46] = "uploader.exe    ";
 cginame[47] = "rguest.exe      ";
 cginame[48] = "wguest.exe      ";
 cginame[49] = "bdir - samples  ";
 cginame[50] = "CGImail.exe     ";
 cginame[51] = "newdsn.exe      ";
 cginame[52] = "fpcount.exe     ";
 cginame[53] = "openfile.cfm    ";
 cginame[54] = "exprcalc.cfm    ";
 cginame[55] = "dispopenedfile  ";
 cginame[56] = "sendmail.cfm    ";
 cginame[57] = "codebrws.asp    ";
 cginame[58] = "codebrws.asp 2  ";
 cginame[59] = "search97.vts    ";
 cginame[60] = "carbo.dll       ";

 if (argc<2)
   {
   printf("\n [-- CGI Checker 1.34. Modified by su1d sh3ll //UnlG --]");
   printf("\nusage : %s host ",argv[0]);
   printf("\n   Or : %s host -d   for debug mode\n\n",argv[0]); 
   exit(0);
   }

 if (argc>2)
   {
   if(strstr("-d",argv[2]))
     {
     debugm=1;
     }
   }

 if ((he=gethostbyname(argv[1])) == NULL)
   {
   herror("gethostbyname");
   exit(0);
   }

 printf("\n\n\t [CKS & Fdisk]'s CGI Checker - modify by su1d sh3ll 13.05.99\n\n\n");
 start=inet_addr(argv[1]);
 counter=ntohl(start);

   sock=socket(AF_INET, SOCK_STREAM, 0);
   bcopy(he->h_addr, (char *)&sin.sin_addr, he->h_length);
   sin.sin_family=AF_INET;
   sin.sin_port=htons(80);    /* <--- if u want scan another port change it  */
                              /* codex when u again change this code pls call 
                                 proggi like this 1.34.1 or 1.34.[a..z] ;-)  */

  if (connect(sock, (struct sockaddr*)&sin, sizeof(sin))!=0)
     {
     perror("connect");
     }
   printf("\n\n\t [ Press any key to check out the httpd version...... ]\n");
   getchar();     /* CKS  sorry, but ur new piece of code don't work :-( */
   send(sock, "HEAD / HTTP/1.0\n\n",17,0);
   recv(sock, buffer, sizeof(buffer),0);
   printf("%s",buffer);
   close(sock); 
  
   printf("\n\t [ Press any key to search 4 CGI stuff...... ]\n");
   getchar();
   
while(count++ < 60)    /* huh! 60 cgi..... no secur1ty in th1s w0rld ;-)*/
   {
   sock=socket(AF_INET, SOCK_STREAM, 0);
   bcopy(he->h_addr, (char *)&sin.sin_addr, he->h_length);
   sin.sin_family=AF_INET;
   sin.sin_port=htons(80);
   if (connect(sock, (struct sockaddr*)&sin, sizeof(sin))!=0)
     {
     perror("connect");
     }
   printf("Searching for %s : ",cginame[count]);
  
   for(numin=0;numin < 1024;numin++)
      {
      cgibuff[numin] = '\0';
      } 
  
   send(sock, buff[count],strlen(buff[count]),0);
   recv(sock, cgibuff, sizeof(cgibuff),0);
   cgistr = strstr(cgibuff,foundmsg);
   if( cgistr != NULL)
       printf("Found !! ;)\n");
   else
       printf("Not Found\n");
      
  if(debugm==1)
    { 
    printf("\n\n ------------------------\n %s \n ------------------------\n",cgibuff); 
    printf("Press any key to continue....\n");         getchar();
    }  
   close(sock);
   }
   printf("...have a nice hack... ;-)\n");
 }
