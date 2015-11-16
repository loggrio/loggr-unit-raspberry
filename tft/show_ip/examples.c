/*##############################################################*/
/* 																*/
/* File		: examples.c 										*/
/*																*/
/* Project	: TFT for Raspberry Pi Revision 2					*/
/* 																*/
/* Date		: 2014-03-01   	    last update: 2014-03-02			*/
/* 																*/
/* Author	: Hagen Ploog   									*/
/*		  	  Timo Pfander										*/
/* 																*/
/* IDE	 	: Geany 1.22										*/
/* Compiler : gcc (Debian 4.6.3-14+rpi1) 4.6.3					*/
/*																*/
/* Copyright (C) 2013 admatec GmbH								*/
/*																*/
/*																*/
/* Description  :												*/
/* 	Exmples.c includes the following functions to demonstrate 	*/
/*	some opportunities:											*/
/*		- depict one BMP file on the TFT 						*/
/*		- depict basic drawings which were created with the 	*/
/*		  RAIO graphic controller								*/
/*		- write some text on the TFT							*/
/*		- draw functions like sine, cosine, parabola, ...		*/
/*																*/
/*																*/
/* License:														*/
/*																*/
/*	This program is free software; you can redistribute it 		*/
/*	and/or modify it under the terms of the GNU General			*/
/*	Public License as published by the Free Software 			*/
/*	Foundation; either version 3 of the License, or 			*/
/*	(at your option) any later version. 						*/
/*    															*/
/*	This program is distributed in the hope that it will 		*/
/*	be useful, but WITHOUT ANY WARRANTY; without even the 		*/
/*	implied warranty of MERCHANTABILITY or 						*/
/*	FITNESS FOR A PARTICULAR PURPOSE. See the GNU General 		*/
/*	Public License for more details. 							*/
/*																*/
/*	You should have received a copy of the GNU General 			*/
/*	Public License along with this program; if not, 			*/
/*	see <http://www.gnu.org/licenses/>.							*/
/*																*/
/*																*/
/* Revision History:											*/
/*																*/
/*	Version 1.0 - Initial release								*/
/*																*/
/*																*/
/*																*/
/*##############################################################*/


#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include "RAIO8870.h"
#include "bmp.h"
#include "examples.h"


// load and depict a BMP file
// ---------------------------------------------
void example_DepictBMP( char const *file_name  )
{
	uint16_t picture[1][ PICTURE_PIXELS ];

	Read_bmp2memory ( file_name, &picture[0][ PICTURE_PIXELS-1 ] );
	RAIO_Write_Picture ( &picture[0][0], PICTURE_PIXELS );
}


// draw with RAIO
// ---------------------------------------------
void example_DrawWithRAIO( void )
{
	// rectangle
	Draw_Square (0, 0, 319, 239);
	Text_Foreground_Color ( COLOR_BLACK );
	RAIO_StartDrawing ( SQUARE_FILL );
	Text_Foreground_Color ( COLOR_BLUE );
	Draw_Square (210, 150, 260, 200);

	// line
	Draw_Line ( 10, 230, 310, 10 );
	Text_Foreground_Color ( COLOR_GREEN );
	RAIO_StartDrawing ( LINE );

	// circle
	Draw_Circle ( 90, 65, 25 );
	Text_Foreground_Color ( COLOR_RED );
	RAIO_StartDrawing ( CIRCLE_FILL );
}


// write text
// ---------------------------------------------
void example_WriteText( unsigned char *text )
{
	RAIO_clear_screen();

    RAIO_SetFontSizeFactor ( 5 );
    RAIO_print_text ( 10, 10, text, COLOR_BLACK , COLOR_WHITE );
}


// draw sinus
// ---------------------------------------------

// defines the x-intercept and y-intercept on the TFT
#define window_left 	-M_PI
#define window_right	 M_PI
#define window_up		 2
#define window_down		-2


//  				 	   windows_up
//
//							   ↑
//  				  _ _ _ _ _|_ _ _ _ _
//  				 |		   |		 |
//  				 |		   |		 |
//  				 | 		   |		 |
//   windows_left  --|---------|---------|--→  windows_right
//  				 |	 	   | 		 |
//  				 | 	 	   |		 |
//  			 	 |_ _ _ _ _|_ _ _ _ _|
//							   |
//
//  				      windows_down



void example_DrawFunction( int16_t function )
{
	float_t x_real, y_real;
	int16_t count;

	RAIO_clear_screen();

	// draw x-axis
	draw_coords_line ( window_left, 0, window_right, 0 );
	for( count = (int16_t)window_left; count < (int16_t)window_right; count++ )
	{
		Draw_Line ( scale_x( count ), scale_y( window_up*0.01 ), scale_x( count ), scale_y( window_down*0.01 ) );
		Text_Foreground_Color ( COLOR_WHITE );
		RAIO_StartDrawing ( LINE );
	}

	// draw y-axis
	draw_coords_line ( 0, window_up, 0, window_down );
	for( count = (int16_t)window_down; count < (int16_t)window_up; count++ )
	{
		Draw_Line ( scale_x( window_left*0.01 ), scale_y( count ), scale_x( window_right*0.01 ), scale_y( count ) );
		Text_Foreground_Color ( COLOR_WHITE );
		RAIO_StartDrawing ( LINE );
	}


	// draw function
	for( x_real = window_left; x_real < window_right; x_real=x_real+0.02 )
	{
		switch (function) // -> see FUNCTIONS
		{
			case SIN:      y_real = sin( x_real );   break;
			case COS:      y_real = cos( x_real );   break;
			case TAN:      y_real = tan( x_real );   break;
			case PARABOLA: y_real = x_real * x_real; break;
			case EXPONENT: y_real = exp( x_real );   break;
			case LOGN    : y_real = log( x_real );   break;
			default: break;
		};
		set_point( x_real, y_real);
	}
}


// transform real world data in TFT data
// ---------------------------------------------

// transform x-value
uint16_t scale_x ( float_t x )
{
	return ( (uint16_t) (( x - window_left ) * ( DISPLAY_WIDTH / (window_right-window_left))) );
}

// transform y-value
uint16_t scale_y ( float_t y )
{
	uint16_t temp_y;

	temp_y = DISPLAY_HEIGHT - (uint16_t) (( y - window_down) *  (DISPLAY_HEIGHT / (window_up-window_down)));
	if( temp_y > 239 ) { temp_y--; }

	return ( temp_y );
}


// draw coordinate system and function points
// ---------------------------------------------

// draw coordinate system
void draw_coords_line (float_t x1, float_t y1, float_t x2, float_t y2)
{
	Text_Foreground_Color( COLOR_WHITE );
	Draw_Line( scale_x( x1 ), scale_y( y1 ), scale_x( x2 ), scale_y( y2 ) );
	RAIO_StartDrawing( LINE );
}

// draw function point
void set_point ( float_t x_real, float_t y_real )
{
	if ((x_real> window_left) & (x_real < window_right) & (y_real > window_down) & (y_real <window_up))
	{
		Text_Foreground_Color( COLOR_WHITE );
		Draw_Line( scale_x( x_real ), scale_y( y_real ), scale_x( x_real ), scale_y( y_real ) );
		RAIO_StartDrawing( LINE );
	}
}
