#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as sudo"
   echo "Rerun it with sudo ./install.sh"
   exit 1
fi

# Install Dependencies
LIST_OF_APPS="ffmpeg"
add-apt-repository ppa:jonathonf/ffmpeg-4
apt-get update # latest package list
apt-get install -y $LIST_OF_APPS