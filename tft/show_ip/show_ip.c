#include <bcm2835.h>
#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include "tft.h"
#include "RAIO8870.h"
#include "bmp.h"
#include "examples.h"
#include <unistd.h>
#include <string.h> /* for strncpy */
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <netinet/in.h>
#include <net/if.h>
#include <arpa/inet.h>


int main( int argc, char **argv )
{
    int fd;
    struct ifreq ifr;

	if (!bcm2835_init())
	    return 1;

	TFT_init_board();
	TFT_hard_reset();
	RAIO_init();

    /* show IP address after a delay of 10 secs */
	delay(10000);

	fd = socket(AF_INET, SOCK_DGRAM, 0);

	/* get IPv4 IP address */
	ifr.ifr_addr.sa_family = AF_INET;

	/* get IP address attached to "eth0" */
	strncpy(ifr.ifr_name, "eth0", IFNAMSIZ-1);

	ioctl(fd, SIOCGIFADDR, &ifr);

	close(fd);

	example_WriteText( inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr) );

    /* show IP address for 5 secs */
	delay(5000);

    bcm2835_close();

   	return 0;
}
