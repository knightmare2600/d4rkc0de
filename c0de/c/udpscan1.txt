/* UDP scanner.
   Please dont go around scanning the planet it isnt polite.

   We try and identify open UDP ports by sending a bogus UDP packet
   then waiting for an ICMP message of "PORT UNREACHABLE".

   There are a few problems with this UDP scanner which I'll probably c0de up
   to bypass. One bieng the fact that both ICMP and UDP get lost. I thought of
   adding an RTT mechanism but that would be an overkill for a simple
   example like this one. In the long run your better off using RTT if your 
   doing it in a congested network.

   Since we're not using direct packet capturing on the
   interace itself the kernel may or may not drop the packets before
   passing them to all proccesses currently using SOCK_RAW and IPPROTO_ICMP.
   A better implementation would use libpcap.

   I honestly have no idea if its been done before in the same way.

   Fri Sep 20 01:47:48 1996

   Copyleft 1996 shadows@whitefang.com
                 shadows@kuwait.net

   Has been tested on FreeBSD 2.1.5
*/

#include <stdlib.h>
#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/time.h>

#include <netinet/in_systm.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <unistd.h>
#include <strings.h>
#include <errno.h>

/* Tweak these to make things faster. I've included getopt as well
   since I'm an option kinda guy ;) */

#define MAXPACKET 4096
#define DEFAULT_TIMEOUT 10
#define DEFAULT_RESEND 6
#define SPORT 1
#define EPORT 1024

extern char *optarg;
extern int optind;

void usage(char *string)
{
  fprintf(stderr,"usage: %s hostname|ipaddr [-s start port] [-e end port] [-t timeout]\n",string);
  exit(-1);
}

void start_scanning(unsigned short sport,unsigned short eport,struct in_addr myaddr,unsigned short timeout,int maxretry)
{
  struct sockaddr_in myudp;
  char buff[] = "This was a blatant UDP port scan.";
  int udpsock, rawsock, retry, retval,iplen;
  unsigned short port;
  fd_set r;
  struct timeval mytimeout;
  struct icmp *packet;
  struct ip *iphdr;
  struct servent *service;
  unsigned char recvbuff[MAXPACKET];

  if((udpsock = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)) < 0)
    {
      perror("socket()");
      exit(-1);
    }

  if((rawsock = socket(AF_INET,SOCK_RAW,IPPROTO_ICMP)) < 0)
    {
      perror("socket()");
      exit(-1);
    }

  if(!(sport))
    sport = SPORT;
  if(!(eport))
    eport = EPORT;
  if(!(timeout))
    timeout = DEFAULT_TIMEOUT;
  if(!(maxretry))
    maxretry = DEFAULT_RESEND;

  if(sport > eport)
    {
      fprintf(stderr,"Uh you've got the start-port at %u and the end-port at %u this doesnt look right.\n",sport,eport);
      exit(-1);
    }

  bcopy(&myaddr.s_addr,&myudp.sin_addr.s_addr,sizeof(myaddr.s_addr));

  myudp.sin_family = AF_INET;

  mytimeout.tv_sec = timeout;
  mytimeout.tv_usec = 0;

  for(port = sport;port < eport;port++)
    {
      
      myudp.sin_port = htons(port);
      
      retry = 0;
    
      while(retry++ < maxretry)
	{
	  
	  /* I'll use select to do the timeout. Its a bit more
	     'portable'. Than using a signal */
	  
	  if((sendto(udpsock,buff,sizeof(buff),0x0,(struct sockaddr *)&myudp,sizeof(myudp))) < 0)
	    {
	      perror("sendto");
	      exit(-1);
	    }
	

	  FD_ZERO(&r);
	  FD_SET(rawsock,&r);
	  
	  retval = select((rawsock+1),&r,NULL,NULL,&mytimeout);
	  
	  if(retval)
	    {
	      /* We got an answer lets check if its the one we want. */
      
	      if((recvfrom(rawsock,&recvbuff,sizeof(recvbuff),0x0,NULL,NULL)) < 0)
		{
		  perror("Recv");
		  exit(-1);
		}

	      /* Problem with getting back the address of the host
		 is that not all hosts will answer icmp unreachable
		 directly from thier own host. */

		  iphdr = (struct ip *)recvbuff;
		  iplen = iphdr->ip_hl << 2;
		  
		  packet = (struct icmp *)(recvbuff + iplen);

		  if((packet->icmp_type == ICMP_UNREACH) && (packet->icmp_code == ICMP_UNREACH_PORT))
		    break;
	    
	    }
	  else
	    continue;
	}

      if(retry >= maxretry)
	{
	  if((service = getservbyport(htons(port),"udp")) == NULL)
	      fprintf(stdout,"Unknown port %u, open.\n",port);
	  else
	    fprintf(stdout,"UDP service %s open.\n",service->s_name);
	  fflush(stdout);
	}
    }
}
	  
struct in_addr resolv(char *address)
{
  struct in_addr myaddr;
  struct hostent *host;

  if((myaddr.s_addr = inet_addr(address)) == INADDR_NONE)
    {
      if((host = gethostbyname(address)) == NULL)
	fprintf(stderr,"%s Invalid address\n",address);
      else
	{
	  bcopy((int *) * &host->h_addr,&myaddr.s_addr,host->h_length); 
	  return myaddr;
	}
    }

    return myaddr;
}



int main(int argc,char **argv)
{
  unsigned short sport = 0;
  unsigned short eport = 0;
  unsigned short timeout = 0;
  unsigned short maxretry = 0;
  struct in_addr myaddr;
  char c;
  
  if(argc < 2)
    {
      usage(argv[0]);
      exit(-1);
    }

  while((c = getopt(argc,argv,"s:e:t:r:")) != EOF)
    {
      switch(c)
	{
	case 's':
	  {
	    sport = (unsigned int)atoi(optarg);
	    break;
	  }
	case 'e':
	  {
	    eport = (unsigned int)atoi(optarg);
	    break;
	  }
	case 't':
	  {
	    timeout = (unsigned int)atoi(optarg);
	    break;
	  }
	case 'r':
	  {
	    maxretry = (unsigned int)atoi(optarg);
	    break;
	  }
	default:
	  {
	    usage(argv[0]);
	  }
	}
    }

  myaddr = resolv(argv[optind]);

  start_scanning(sport,eport,myaddr,timeout,maxretry);

  exit(0);
}
