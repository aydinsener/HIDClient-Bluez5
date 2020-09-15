#!/usr/bin/env python3

SERVICE_NAME = "hidclient" #what the host sees
CONNECT_TO = "EC:0E:C4:AB:70:0E" #mac address - this is my PS4
#CONNECT_TO = "" #set this to "" if you want to pair
ATTACH_DEVICES = ["AT Translated Set 2 keyboard".lower()] #This is my Thinkpad keyboard - lowercase checks leave less room for error(?)
#Use `./hidclient -l` to see the names of devices - if you connect/disconnect devices, their index may change, so this script gets the index programatically
#ATTACH_DEVICES = [] #leave blank for all devices (NOT RECOMMENDED) - Mouses don't seem to operate too great

import os, subprocess, shlex, time

if os.geteuid() != 0:
	exit("This must be run as root")

print("IF YOUR KEYBOARD HAS BEEN TAKEN, PRESS Ctrl+Alt+ScrLk TO EXIT\n") #this is the bind to exit hidclient

print("Will be connecting to: [%s]" % (CONNECT_TO) if CONNECT_TO else "Will be attempting to pair...\nRemember to add the MAC address of the connected device to this script!")
print("") #don't get drowned

print("Restarting bluetoothd") #get a clean bluetooth stack
subprocess.call(shlex.split("systemctl restart bluetooth.service"))
time.sleep(1) #naively wait for systemctl - there doesn't seem to be a easy solution that works better than this

if not CONNECT_TO: #pairing mode
	subprocess.check_output("bluetoothctl", input=b"discoverable on\nagent NoInputNoOutput\n") #do this here, so that it doesn't interfere with below

print("- Setting up bluetooth settings") #set up basic bluetooth settings
subprocess.call(shlex.split("hciconfig hci0 class 0x000540")) #emulate HID device
subprocess.call(shlex.split("hciconfig hci0 name \"%s\"" % (SERVICE_NAME)))
subprocess.call(shlex.split("hciconfig hci0 sspmode 1")) #simple pairing mode disable

print("- Removing unused SDPs")
rechandle_prefix = "Service RecHandle: "
for x in subprocess.check_output(shlex.split("sdptool browse local")).decode("utf-8").splitlines():
	if x.startswith(rechandle_prefix):
		subprocess.call(shlex.split( "sdptool del %s" % (x[len(rechandle_prefix):]) ), stdout=subprocess.PIPE)

print("Finding input device ids") #hidclient setup
device_ids = []
for x in subprocess.check_output(shlex.split("./hidclient -l")).decode("utf-8").splitlines():
	x = x.strip()
	x = shlex.split(x) #will keep the names intact as they are inside apostrophes
	if x[0].isdigit():
		if x[2].lower() in ATTACH_DEVICES:
			print("- Found \"%s\"" % (x[2]))
			device_ids.append("-e" + x[0])

print("Starting hidclient...")
hidclient = subprocess.Popen(shlex.split("./hidclient -x") + device_ids)

if CONNECT_TO: #NOT pairing mode
	subprocess.check_output("bluetoothctl", input=b"connect %s\n" % CONNECT_TO.encode("utf-8"))

hidclient.communicate() #wait for exit
print("Restarting bluetoothd")
subprocess.call(shlex.split("systemctl restart bluetooth.service")) #put the bluetooth stack back to normal
