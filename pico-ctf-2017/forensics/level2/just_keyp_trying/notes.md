# Just Keyp Trying
(Forensics, Level 2, 80pts)

PCAP file. Consists of URB_INTERRUPT data?
We can extract out the "Leftover Capture Data" pretty easily with Scapy.

This site explains how the data can be interpreted:
https://docs.mbed.com/docs/ble-hid/en/latest/api/md_doc_HID.html

Basically, the data is sent as a string of 8 bytes. Byte 0 is a "control" byte which says if any modifier keys were pressed. Byte 2 is the actual key.
Between each keypress, it sends all null bytes.

The following GitHub gives the mapping from byte to which key:
https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2

The code in `extract_data.py` implements enough of this to parse the keypresses. It spells out a flag, followed by Ctrl-C.
