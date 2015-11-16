#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "RAIO8870.h"
#include <string.h>


int main( int argc, char *argv[] )
{


        if( argc !=9 ){
                printf("\ntft_string: Error! Use 'tft_string fontsize pos_x pos_y textcolor backgroundcolor transparenz bold textstring'\n");
                exit(1);
        }


        char text[255];
        strcpy(text,argv[8]);
        int fsf=atoi(argv[1]);
        int  px=atoi(argv[2]);
        int py=atoi(argv[3]);
        int col_fg=atoi(argv[4]);
        int col_bg=atoi(argv[5]);
        int transparent=atoi(argv[6]);
        int bold=atoi(argv[7]);

        if (!bcm2835_init()){
                printf("tft_string: Error, check your display! \n");
                exit(1);
        }


        if( strlen(text) > 255){
                printf("tft_string: Error, string too long!  Limit: 255 chars \n");
                exit(1);
        }



        if( col_fg < 0 || col_fg > 255){
                printf("tft_string: Error,  foregroundcolor out of range! Use 0...255! \n");
                exit(1);
        }

        if(col_bg < 0 || col_bg > 255){
                printf("tft_string: Error, backgroundcolor out oft range! Use 0...255!\n");
                exit(1);
        }
if( px < 0 || px > 319){
                printf("tft_string: Error, pos_x out of range! pos_x: 0...319!\n");
                exit(1);
        }

        if ( py < 0 || py > 239){
                printf("tft_string: Error, pos_y out of range! pos_y: 0...239!\n");
                exit(1);
        }

        if ( fsf < 0 || fsf > 15){
                printf("tft_string: Error, bad fontsize! fs: 0...15!\n");
                exit(1);
        }

        if (transparent < 0 || transparent > 1){
                printf("Error! Tansparenz muss 0 oder 1 sein!");
                exit(1);
        }
        if (bold != 0 && bold !=1) {
                printf("Error! Bold muss 0 oder 1 sein!");
                exit(1);
        }


        //RAIO_SetFontSizeFactor ( fsf );
if(transparent == 0){
                fsf=fsf | 0x80;
        }
        else{

                fsf=fsf | 0xC0;
        }

        if( bold == 1 ){

                fsf=fsf |  0x20;
        }
        else {
                fsf=fsf & 0xDF;
        }

        RAIO_SetRegister( FNCR1, fsf);
        RAIO_print_text ( px, py, text, col_bg ,col_fg);

        return 0;
}
