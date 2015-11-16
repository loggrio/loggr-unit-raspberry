all: show_ip 

show_ip: show_ip.o tft.o RAIO8870.o bmp.o examples.o
	gcc show_ip.o tft.o RAIO8870.o bmp.o examples.o -lbcm2835 -lrt -lm -o show_ip 

tft.o: tft.c tft.h
	gcc -Os -c tft.c

show_ip.o: show_ip.c 
	gcc -Os -c show_ip.c
	
RAIO8870.o: RAIO8870.c RAIO8870.h
	gcc -Os -c RAIO8870.c

bmp.o: bmp.c bmp.h RAIO8870.h
	gcc -Os -c bmp.c
	
examples.o: examples.c examples.h RAIO8870.h bmp.h
	gcc -Os -c examples.c

clean:
	rm -rf *o show_ip

