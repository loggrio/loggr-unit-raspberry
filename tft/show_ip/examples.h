/*##############################################################*/
/* 																*/
/* File		: examples.h		    							*/
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
/* 	This file declared functions for the different examples in	*/
/*  example.c													*/
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

#ifndef EXAMPLES_H
#define EXAMPLES_H

#include <stdint.h>
#include <math.h>


// load and depict a BMP file
// ---------------------------------------------
void example_DepictBMP( char const *file_name );


// draw with RAIO
// ---------------------------------------------
void example_DrawWithRAIO( void );


// delete screen and write text
// ---------------------------------------------
void example_WriteText( unsigned char *text );


// draw function // -> see FUNCTIONS
// ---------------------------------------------
void example_DrawFunction( int16_t function );

// enumeration of drawing modes 
enum FUNCTIONS { SIN, COS, TAN, PARABOLA, EXPONENT, LOGN }; 


// transform real world data in TFT data
// ---------------------------------------------
uint16_t scale_x( float_t x );

uint16_t scale_y( float_t y );


// draw coordinate system and function points
// ---------------------------------------------
void draw_coords_line(float_t x1, float_t y1, float_t x2, float_t y2);

void set_point( float_t x_real, float_t y_real );


#endif

