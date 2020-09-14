#!/bin/sh
sudo systemctl restart bluetooth.service
sleep 1
#echo "discoverable on" | bluetoothctl #uncomment this to enable discovery - you WILL need to open bluetoothctl (or similar) to pair
sudo hciconfig hci0 class 0x000540 #emulate HID device
sudo hciconfig hci0 name "Bluetooth PC Keyboard" #device name
sudo hciconfig hci0 sspmode 1 #simple pairing mode

#Remove other SDPs, so that only the HID one remains (when hidclient is run)
#This is pretty naive, but it works
sudo sdptool del 0x10000
sudo sdptool del 0x10001
sudo sdptool del 0x10002
sudo sdptool del 0x10003
sudo sdptool del 0x10004
sudo sdptool del 0x10005
sudo sdptool del 0x10006
sudo sdptool del 0x10007
sudo sdptool del 0x10008
sudo sdptool del 0x10009
sudo sdptool del 0x1000a
sudo sdptool del 0x1000b
sudo sdptool del 0x1000c
sudo sdptool del 0x1000d
sudo sdptool del 0x1000e
sudo sdptool del 0x1000f

sudo sdptool del 0x10010
sudo sdptool del 0x10011
sudo sdptool del 0x10012
sudo sdptool del 0x10013
sudo sdptool del 0x10014
sudo sdptool del 0x10015
sudo sdptool del 0x10016
sudo sdptool del 0x10017
sudo sdptool del 0x10018
sudo sdptool del 0x10019
sudo sdptool del 0x1001a
sudo sdptool del 0x1001b
sudo sdptool del 0x1001c
sudo sdptool del 0x1001d
sudo sdptool del 0x1001e
sudo sdptool del 0x1001f

sudo ./hidclient -e3 -x & #start service, which should steal all your keypresses, so start in the background
echo "connect EC:0E:C4:AB:70:0E" | bluetoothctl #connect to your host device, this MAC is for my Ps4

# YOU MUST "sudo killall -9 hidtool" when this exits, or your CPU will catch file
