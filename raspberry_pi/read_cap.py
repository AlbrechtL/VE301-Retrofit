# see https://arduino-simple-rpc.readthedocs.io/en/latest/library.html#generic-interface
from simple_rpc import Interface

import numpy as np
import time

interface = Interface('/dev/ttyUSB0', baudrate = 115200)
N=20
cap1_list = np.zeros(N)

while True:
    cap0 = interface.getCap0()
    cap1 = interface.getCap1()
    cap1_list = np.roll(cap1_list, 1)
    cap1_list[0] = cap1
    cap1_filtered = np.convolve(cap1_list, np.ones(N)/N, mode='valid')
    #print("cap0: {:06.2f} cap1: {:06.2f} cap1_filtered: {:06.2f}".format(cap0, cap1, cap1_filtered[0]))
    print("cap1: {:06.2f} cap1_filtered: {:06.2f}".format(cap1, cap1_filtered[0]))

    time.sleep(0.1)
