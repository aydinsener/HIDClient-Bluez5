# hidclient - Bluez 5 / Systemd
This specific fork is for compatibility with Bluez version 5. The target system is Ubuntu 18.04, but this may work for more recent versions. The program will remain almost identical to the original, but the instructions to run it will differ.

This setup specifically works for a Ps4, as you need the Pause key to act as the PS Button - this has been changed to Scroll Lock in this fork, check line `802` if you would like to edit it

## One time setup
1. Enable bluetoothd, probably via `sudo systemctl enable bluetooth` and ensure it's been started
2. Edit `/etc/systemd/system/dbus-org.bluez.service` and perform the following change:
```bash
ExecStart=/usr/lib/bluetooth/bluetoothd
                   |
                   V
ExecStart=/usr/lib/bluetooth/bluetoothd  --compat -P input
```
3. Restart the systemd daemon with `sudo systemctl daemon-reload`
4. Compile the hidclient with `make`, you may need to install `libbluetooth-dev`

#### Notes
- `--compat` enables the use of sdptool
- `-P input` seems to be the only way to disable the input plugin in Bluez 5

## Helper script
DEFINITELY use `launch.py` to automate connecting/pairing to your host - make sure to alter to your needs as it will NOT work ootb

## Pairing
Read `example.sh` to see an example of approximate steps to run this program and things that must happen on your Bluetooth stack for this to work. You must be able to run the program, while also having control of an input device so that you may pair either through `bluetoothctl` (`discoverable on` + `default-agent`), or something like `Blueman`

## Running
Use essentially the same steps as above, just instead of attempting to pair, manually connect. This is easy with `bluetoothctl`, and can be automated with `echo "xx:xx:xx:xx:xx:xx" | bluetoothctl`
