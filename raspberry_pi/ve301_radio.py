#!/usr/bin/python3

# Based on https://github.com/msz1337/piSingleSwitchRadio
# Copyright 2024 Albrecht Lohöfener <albrechtloh@gmx.de>
# License GPLv2 or newer

import os
import subprocess
import time
import threading
import json
import simple_rpc
import mpv

# Capacitor limits in pF
big_cap_lowest = 4
big_cap_highest = 90
vol_cap_lowest = 4
vol_cap_highest = 139

class GetCapThread(threading.Thread):

    big_cap_value = 0
    small_cap_value = 0

    CapInterface = simple_rpc.Interface('/dev/ttyUSB0', baudrate = 115200)

    def run(self):
        while True:
            # Read capacitor values from Arduino via serial
            GetCapThread.big_cap_value = GetCapThread.CapInterface.getCap1()
            GetCapThread.small_cap_value = GetCapThread.CapInterface.getCap0()

            #print("cap_value: {:06.2f} small_cap_value: {:06.2f}".format(GetCapThread.big_cap_value, GetCapThread.small_cap_value))
            time.sleep(0.1)


    @staticmethod
    def get_cap_value():
        big_cap_value = GetCapThread.big_cap_value
        small_cap_value = GetCapThread.small_cap_value
        return big_cap_value, small_cap_value


if __name__ == '__main__':
    config_file_path = os.path.join(os.path.dirname(__file__), 've301_radio.json')
    radio_index = -1
    espeak_process = False
    mpv_process = False
    current_station = {'name':'none', 'current_cap_value': -99}
    current_vol = 0

    # Start getting of capacitor values
    cap_thread = GetCapThread()
    cap_thread.start()

    # Load station list
    with open(config_file_path, 'r') as config_file:
                radio_arr = json.loads(config_file.read())

    # Announcement
    espeak_process = subprocess.Popen(
                ['espeak-ng', '-v', 'mb-de7', '"Radio ist gestartet"', '-s 140', '-a 50'],
                shell=False,
                stdin=None,
                stdout=None,
                stderr=None
            )
    espeak_process.wait()

    player = mpv.MPV(ytdl=False)
    player.audio_channels = 'mono'

    while True:
        # Get capacitor values
        big_cap, vol_cap = GetCapThread.get_cap_value()

        # Calc volume
        current_vol = vol_cap / (vol_cap_highest - vol_cap_lowest) * 100

        # Get the station with the closest cap_value
        new_current_station = min(radio_arr, key=lambda x:abs(x["cap_value"] - big_cap))
        new_current_station['current_cap_value'] = big_cap

        # Play new station if required, add some boundaries to avoid fast back and for switching
        if (new_current_station['name'] is not current_station['name']) and \
        abs(new_current_station['current_cap_value'] - current_station['current_cap_value']) > 2 :
            current_station = new_current_station
            if espeak_process:
                espeak_process.kill()
            
            player.stop()

            print("big_cap: {:06.2f} pF  current_station:{} pF  ".format(big_cap, current_station))

            # Announcement new station
            espeak_process = subprocess.Popen(
                ['espeak-ng', '-v', new_current_station['lang'], '"'+new_current_station['name']+'"', '-s 140', '-a', str(int(current_vol))],
                shell=False,
                stdin=None,
                stdout=None,
                stderr=None
            )
            espeak_process.wait()

            # Play station
            player.play(new_current_station['url'])

        # Set volume
        player.volume = current_vol

        print("station_cap_value: {:06.2f} pF  vol_cap_value: {:06.2f} pF  current_vol: {:06.2f}%".format(big_cap, vol_cap, current_vol))

        time.sleep(0.2)