#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdlib.h>
#include <arpa/inet.h>

#define MAXBUF 100
static    int s_sock;
static   int s_status;
static struct sockaddr_in6 s_sin6;
static   int s_sin6len;
static   char s_buffer[MAXBUF];


int main(int argc, char* argv[])
{
   int sock, port;
   int status;
   struct addrinfo sainfo, *psinfo;
   struct sockaddr_in6 sin6;
   int sin6len;
   char buffer[MAXBUF], arg[MAXBUF];

   sin6len = sizeof(struct sockaddr_in6);

   sprintf(buffer,"led_off");
	 port = 3000;	//default
	
   if(argc < 2) {
     printf("Specify a port number\n"), exit(1);
		}
	 else if (argc==3) {
			port = atoi(argv[1]);
   		sprintf(buffer,argv[2]);
	}		
	else if (argc==4) {
			port = atoi(argv[1]);
		  //sprintf(buffer,argv[2]);
   		sprintf(buffer,"%s %s",argv[2],argv[3] );
	}	


   sock = socket(PF_INET6, SOCK_DGRAM,0);

   memset(&sin6, 0, sizeof(struct sockaddr_in6));
   sin6.sin6_port = htons(port);
   sin6.sin6_family = AF_INET6;
   sin6.sin6_addr = in6addr_any;

   status = bind(sock, (struct sockaddr *)&sin6, sin6len);

   if(-1 == status)
     perror("bind"), exit(1);

   memset(&sainfo, 0, sizeof(struct addrinfo));
   memset(&sin6, 0, sin6len);

   sainfo.ai_flags = 0;
   sainfo.ai_family = PF_INET6;
   sainfo.ai_socktype = SOCK_DGRAM;
   sainfo.ai_protocol = IPPROTO_UDP;
   status = getaddrinfo("aaaa::212:7402:2:202", argv[1], &sainfo, &psinfo);

   switch (status) 
     {
      case EAI_FAMILY: printf("family\n");
        break;
      case EAI_SOCKTYPE: printf("stype\n");
        break;
      case EAI_BADFLAGS: printf("flag\n");
        break;
      case EAI_NONAME: printf("noname\n");
        break;
      case EAI_SERVICE: printf("service\n");
        break;
     }

   status = sendto(sock, buffer, strlen(buffer), 0,
                     (struct sockaddr *)psinfo->ai_addr, sin6len);
   printf("buffer : %s \t%d\n", buffer, status);

	 s_status = recvfrom(sock, s_buffer,MAXBUF, 0,
                    (struct sockaddr *)&s_sin6, &s_sin6len);


	if (s_status<0) {
    perror("Problem in recvfrom \n");
    exit(1);
  }

  printf("Got back %d bytes: %s \n",s_status, s_buffer);		
   shutdown(sock, 2);
   close(sock); 

   // free memory
   freeaddrinfo(psinfo);
   psinfo = NULL;
   return 0;
}
