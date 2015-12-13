#!/usr/bin/env bash

export LD_LIBRARY_PATH="/usr/local/lib"

PIC="pic.jpg"
PIC_DIR="/tmp/stream"
WWW_DIR="/usr/local/www"

# create dir
[ ! -d "$PIC_DIR" ] && mkdir "$PIC_DIR"

# kill running instances of raspistill
if pgrep raspistill > /dev/null 2>&1; then
    killall raspistill
fi

raspistill --nopreview -w 640 -h 480 -o $PIC_DIR/$PIC -tl 100 -t 0 > /dev/null 2>&1 &
mjpg_streamer -i "input_file.so -f $PIC_DIR -n $PIC" -o "output_http.so -w $WWW_DIR"
