#!/bin/bash
#
# Shell script to deploy raspi files to raspberry pi
#

if [ $# -eq 0 ]
  then
    echo "Missing argument"
    echo "Usage: ./deploy_raspi.sh <ip-address-of-your-raspi>"; exit 1
elif [ $# -gt 1 ]
  then
    echo "Too much arguments"
    echo "Usage: ./deploy_raspi.sh <ip-address-of-your-raspi>"; exit 2
fi

IP=$1
FOLDERS="/home/pi/Coding/loggr.io/raspi"
TARGET=pi@$IP:$FOLDERS

RASPI_DIR="../"
SENSORS="$RASPI_DIR/sensors/*.c $RASPI_DIR/sensors/Makefile $RASPI_DIR/sensors/*.py"
PYTHON_UTILS="$RASPI_DIR/raspi_loggr/"
CONFIG_SERVER="$RASPI_DIR/config_server/"
GENERAL="$RASPI_DIR/requirements.txt $RASPI_DIR/run.py"
TFT="$RASPI_DIR/tft/"
PIR="$RASPI_DIR/pir/"
STREAM="$RASPI_DIR/stream/"

echo "Shell script to copy raspi files to raspberry pi"
echo "Continue? [y/n]"
read ANSWER
if [ $ANSWER == "n" -o $ANSWER == "N" -o $ANSWER == "no" ]
  then exit 3
elif [ $ANSWER == "y" -o $ANSWER == "Y" -o $ANSWER == "yes" ]
  then
    ssh pi@$IP "mkdir -p $FOLDERS"
    echo "On which type of Raspberry Pi do you want to deploy?"
    echo "Sensor Pi = 1"
    echo "Streaming Pi = 2"
    echo "Viewer Pi = 3"
    read TYPE
    if [ $TYPE == "1" ]
      then
        scp -r $SENSORS $TARGET
        scp -r $PYTHON_UTILS $TARGET
        scp -r $GENERAL $TARGET
        scp -r $CONFIG_SERVER $TARGET
        exit 0
    elif [ $TYPE == "2" ]
      then
        scp -r $PIR $TARGET
        scp -r $PYTHON_UTILS $TARGET
        scp -r $STREAM $TARGET
        scp -r $GENERAL $TARGET
        exit 0
    elif [ $TYPE == "3" ]
      then
        scp -r $TFT $TARGET
        exit 0
    else echo "Invalid answer, exit."; exit 4
    fi
else echo "Invalid answer, exit."; exit 5
fi
