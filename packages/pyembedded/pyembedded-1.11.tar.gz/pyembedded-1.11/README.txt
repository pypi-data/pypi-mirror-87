Python library to interface basic embedded modules like RFID, GPS, GSM, LCD (16x2), DC Motor

Usage:

Installation:
Package can be installed via pip:

pip3 install pyembedded

Verify if it is installed:

import pyembedded
pyembedded.__version__


RFID:

from pyembedded.rfid_module.rfid import RFID
rfid = RFID(port='COM3', baud_rate=9600)
print(rfid.get_id())