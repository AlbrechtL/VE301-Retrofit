# see https://arduino-simple-rpc.readthedocs.io/en/latest/library.html#generic-interface
from simple_rpc import Interface

import time

interface = Interface('/dev/ttyUSB0', baudrate = 115200)

while True:
    cap0 = interface.getCap0()
    cap1 = interface.getCap1()

    print("cap0: {} cap1: {}".format(cap0, cap1))

    time.sleep(100/1000)