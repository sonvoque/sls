#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <string.h>


#define MAXBUF 100
#define MAX_LENGTH 1024
#define DELIMS " \t\r\n"

// static    int s_sock;
static  int     rev_bytes;
static  struct  sockaddr_in6 rev_sin6;
static  int     rev_sin6len;
static  char    rev_buffer[MAXBUF];
static  int     port;
static  char    dst_ipv6addr[50];
static  char    str_port[5];
static  char    cmd[20];
static  char    arg[20];

int main(int argc, char* argv[])
{
  int sock;
  int status;
  struct addrinfo sainfo, *psinfo;
  struct sockaddr_in6 sin6;
  int sin6len;
  char buffer[MAXBUF];

  sin6len = sizeof(struct sockaddr_in6);

  sprintf(buffer,"led_off");
	port = 3000;
  sprintf(dst_ipv6addr,"aaaa::212:7401:1:101");
	
  if(argc < 4) {
    printf("Specify an IPv6 addr or port number or Cmd \n"), exit(1);
	}
	else if (argc==4) {
    sprintf(dst_ipv6addr,argv[1]);      
    strcpy(str_port,argv[2]);
    strcpy(cmd,argv[3]);  
    port = atoi(str_port);
    sprintf(buffer,cmd);
	}		
	else if (argc==5) {
    sprintf(dst_ipv6addr,argv[1]);      
    strcpy(str_port,argv[2]);
    sprintf(cmd,argv[3]);
    sprintf(arg,argv[4]);
		//sprintf(buffer,argv[2]);
    port = atoi(str_port);
   	sprintf(buffer,"%s %s",cmd,arg);
	}	

  strtok(buffer, "\n");

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
  status = getaddrinfo(dst_ipv6addr, str_port, &sainfo, &psinfo);

  status = sendto(sock, buffer, strlen(buffer), 0,
                     (struct sockaddr *)psinfo->ai_addr, sin6len);
  printf("send cmd to [%s] : %s, cmd = %s (len=%d)\n", dst_ipv6addr,str_port, buffer, status);

	rev_bytes = recvfrom(sock, rev_buffer,MAXBUF, 0,(struct sockaddr *)&rev_sin6, &rev_sin6len);

	if (rev_bytes<0) {
    perror("Problem in recvfrom \n");
    exit(1);
  }

  printf("Got back %d bytes: %s \n",rev_bytes, rev_buffer);		
  shutdown(sock, 2);
  close(sock); 

   // free memory
  freeaddrinfo(psinfo);
  psinfo = NULL;
  return 0;
}

/*
int main(int argc, char *argv[]) {
  char *cmd;
  char line[MAX_LENGTH];

  while (1) {
    printf("$ ");
    if (!fgets(line, MAX_LENGTH, stdin)) break;

    // Parse and execute command
    if ((cmd = strtok(line, DELIMS))) {
      // Clear errors
      errno = 0;

      if (strcmp(cmd, "led_on") == 0) {
        char *arg = strtok(0, DELIMS);  
      } else if (strcmp(cmd, "led_off") == 0)   {

      } else if (strcmp(cmd, "exit") == 0) {
        break;

      } else system(line);

      if (errno) perror("Command failed");
    }
  }

  return 0;
}
*/