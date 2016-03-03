#!/bin/bash
sudo mkdir -p /media/iso/
sudo mount -o loop "iso/ubuntu-gnome-15.04-desktop-i386.iso" /media/iso
sudo mkdir -p /media/toBurn
sudo mount /dev/sdb /media/toBurn
sudo cp -a /media/iso/. /media/toBurn
# sudo apt-get install syslinux mtools
sudo syslinux -s /dev/sdb
mv /media/toBurn/isolinux /media/toBurn/syslinux
mv /media/toBurn/syslinux/isolinux.cfg /media/toBurn/syslinux/syslinux.cfg

