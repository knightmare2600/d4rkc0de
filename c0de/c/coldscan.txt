/*
COLD FUSION VULNERABILITY TESTER - Checks for the l0pht advisory
"Cold Fusion Application Server Advisory" dated 4.20.1999
you can find a copy of this advisory and all other
l0pht Security Advisories here:
http://www.l0pht.com/advisories.html
  
much of this program was blatently copied from the cgi scanner released about
a week ago, written by su1d sh3ll...  I just want to give credit where credit
is due...  this particular scanner was "written" (basically modified) by
hypoclear of lUSt - Linux Users Strike Today...  I know that it is trivial to
check to see if a server is vulnerable, but I had fun doing this so who the
heck cares if I want to waste my time...

while I'm here I minds well give shout outs to:
Phrozen Phreak (fidonet rules)
Special K (you will never get rid of my start button ;-)
		go powerpuff girls (he he) ;-)

compile:   gcc -o coldscan coldscan.c
usage:     coldscan host
tested on: IRIX Release 5.3 (this should compile on most *NIX systems though)
*/


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
 char cfbuff[1024];
 char *cfpage[5];
 char *cfname[5];


 cfpage[1] = "GET /cfdocs/expeval/openfile.cfm HTTP/1.0\n\n";
 cfpage[2] = "GET /cfdocs/expeval/displayopenedfile.cfm HTTP/1.0\n\n";
 cfpage[3] = "GET /cfdocs/expeval/exprcalc.cfm HTTP/1.0\n\n";
 

 cfname[1] = "openfile.cfm           ";
 cfname[2] = "displayopenedfile.cfm  ";
 cfname[3] = "exprcalc.cfm           ";


 if (argc<2)
   {
   printf("\n-=COLD FUSION VULNERABILITY TESTER=-");
   printf("\nusage - %s host \n",argv[0]);
   exit(0);
   }

 if ((he=gethostbyname(argv[1])) == NULL)
   {
   herror("gethostbyname");
   exit(0);
   }

 printf("\n-=COLD FUSION VULNERABILITY TESTER=-\n");
 printf("scanning...\n\n");
 start=inet_addr(argv[1]);
 counter=ntohl(start);

   sock=socket(AF_INET, SOCK_STREAM, 0);
   bcopy(he->h_addr, (char *)&sin.sin_addr, he->h_length);
   sin.sin_family=AF_INET;
   sin.sin_port=htons(80);

  if (connect(sock, (struct sockaddr*)&sin, sizeof(sin))!=0)
     {
     perror("connect");
     }


while(count++ < 3)
   {
   sock=socket(AF_INET, SOCK_STREAM, 0);
   bcopy(he->h_addr, (char *)&sin.sin_addr, he->h_length);
   sin.sin_family=AF_INET;
   sin.sin_port=htons(80);
   if (connect(sock, (struct sockaddr*)&sin, sizeof(sin))!=0)
     {
     perror("connect");
     }
   printf("Searching for %s : ",cfname[count]);

   for(numin=0;numin < 1024;numin++)
      {
      cfbuff[numin] = '\0';
      }
 
   send(sock, cfpage[count],strlen(cfpage[count]),0);
   recv(sock, cfbuff, sizeof(cfbuff),0);
   cgistr = strstr(cfbuff,foundmsg);
   if( cgistr != NULL)
       printf("Exists!\n");
   else
       printf("Not Found\n");
      
     close(sock);
   }
 }
