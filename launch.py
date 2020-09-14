#!/usr/bin/env python3

SERVICE_NAME = "hidclient"
CONNECT_TO = "" #mac address - set this to "" if you want to pair

print("IF YOUR KEYBOARD HAS BEEN TAKEN, PRESS CTRL+ALT+PAUSE TO EXIT\n")

print("Connecting to: [%s]" % (CONNECT_TO) if CONNECT_TO else "Will be attempting to pair...\nRemember to add the MAC address of the connected device to this script!")
print("")

import os, subprocess, shlex, time

if os.geteuid() != 0:
	exit("This must be run as root.")

subprocess.call(shlex.split("systemctl restart bluetooth.service"))
time.sleep(1) #naively wait for systemctl

if not CONNECT_TO: #pairing mode
	subprocess.check_output("bluetoothctl", input=b"discoverable on\nagent NoInputNoOutput\n") #do this here, so that it doesn't interfere with below

subprocess.call(shlex.split("hciconfig hci0 class 0x000540")) #emulate HID device
subprocess.call(shlex.split("hciconfig hci0 name \"%s\"" % (SERVICE_NAME)))
subprocess.call(shlex.split("hciconfig hci0 sspmode 1")) #simple pairing mode disable

rechandle_prefix = "Service RecHandle: "
for x in subprocess.check_output(shlex.split("sdptool browse local")).decode("utf-8").splitlines():
	if x.startswith(rechandle_prefix):
		subprocess.call(shlex.split( "sdptool del %s" % (x[len(rechandle_prefix):]) ), stdout=subprocess.PIPE)

hidclient = subprocess.Popen(shlex.split("./hidclient -x -e3"))

if CONNECT_TO: #NOT pairing mode
	subprocess.check_output("bluetoothctl", input=b"connect %s\n" % CONNECT_TO.encode("utf-8"))

hidclient.communicate() #wait for exit
