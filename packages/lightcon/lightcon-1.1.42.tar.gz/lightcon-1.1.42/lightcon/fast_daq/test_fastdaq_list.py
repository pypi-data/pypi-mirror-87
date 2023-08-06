# -*- coding: utf-8 -*-
"""
=== Light Conversion FastDaq API ===

Example: list connected FastDaq devices.

Author: Vytautas Butkus, Lukas Kontenis
Contact: vytautas.butkus@lightcon.com, lukas.kontenis@lightcon.com
Copyright 2019-2020 Light Conversion
"""
import time
from lightcon.fast_daq import FastDaqWrapper, list_fastdaq_devices

print("Listing fastdaq devices...")
start_t = time.time()

devices = list_fastdaq_devices()
print("Num fastdaq endpoints: {:d}".format(len(devices)))

print("ID\tName\tSerial")
for ind, device_name in enumerate(devices):
    try:
        daq = FastDaqWrapper(device_name, silent=True)
        serial_number = daq.daq.Device.SerialNumber
        print("{:d}:\t{:s}\t{:s}".format(ind, device_name, serial_number))
        daq.close()
    except Exception:
        print("{:d}:\t{:s}\t{:s}".format(ind, device_name, 'Not a fastdaq'))

print("Test completed in {:.1f} s".format(time.time() - start_t))
