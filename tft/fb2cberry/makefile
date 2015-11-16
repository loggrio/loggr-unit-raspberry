
#include the Broadcom hardware interface library
XINCDIR +=-I$(ROOTDIR)/opt/vc/include
XINCDIR +=-I$(ROOTDIR)/opt/vc/include/interface/vmcs_host/linux
XINCDIR +=-I$(ROOTDIR)/opt/vc/include/interface/vcos/pthreads -DRPI=1
XLIBS += -L/opt/vc/lib/ -lbcm_host


all: fb2cberry


fb2cberry: fb2cberry.o
	gcc $(XLIBS) $(XINCDIR) $(LIBS) fb2cberry.o tft.o RAIO8870.o -lbcm2835 -lrt -lm -o fb2cberry
 

fb2cberry.o: fb2cberry.c 
	gcc $(XLIBS) $(XINCDIR) $(LIBS) -Os -c fb2cberry.c
	
clean:
	rm -rf *o fb2cberry

