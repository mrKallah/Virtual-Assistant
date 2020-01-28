#!/usr/bin/env bash

#any "sudo apt-get", "wget" and "rm" command are linux only
# only tested on windows 10 and ubuntu 18 and 19

# a lot of this is for audio recording and playback libraries
sudo apt-get update
sudo apt-get upgrade
sudo apt-get build-essential
sudo apt-get pkg-config
sudo apt-get install python-qt4-phonon
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-dev gstreamer1.0-tools gstreamer1.0-doc
sudo apt-get install gstreamer1.0-plugins-base gstreamer1.0-plugins-good
sudo apt-get install gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
sudo apt-get install gstreamer1.0-libav
sudo apt-get install gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
sudo apt-get install mpg321
sudo apt-get install libssl-dev
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install ffmpeg
sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0




sudo pip install pyaudio SpeechRecognition pycairo PyGObject



# this installs the playersctl files
# https://github.com/altdesktop/playerctl

sudo apt-get install playerctl

wget http://ftp.nl.debian.org/debian/pool/main/p/playerctl/libplayerctl2_2.0.2-1_amd64.deb
wget http://ftp.nl.debian.org/debian/pool/main/p/playerctl/playerctl_2.0.2-1_amd64.deb
wget http://ftp.uk.debian.org/debian/pool/main/p/playerctl/gir1.2-playerctl-2.0_2.0.2-1_amd64.deb
sudo dpkg -i libplayerctl2_2.0.2-1_amd64.deb playerctl_2.0.2-1_amd64.deb gir1.2-playerctl-2.0_2.0.2-1_amd64.deb && echo "INSTALL OK"

rm libplayerctl2_2.0.2-1_amd64.deb
rm playerctl_2.0.2-1_amd64.deb
rm gir1.2-playerctl-2.0_2.0.2-1_amd64.deb