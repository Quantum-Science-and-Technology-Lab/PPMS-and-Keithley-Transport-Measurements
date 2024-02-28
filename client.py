# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:30:33 2024

@author: biswa
"""
import MultiPyVu as mpv
import time

with mpv.Client() as client:
    client.open()
    print('client accepted')

    # A basic loop that demonstrates communication between
    # client/server
    for t in range(5):
        # Polls MultiVu for the temperature, field, and their
        #  respective states
        T, sT = client.get_temperature()
        F, sF = client.get_field()

        # Relay the information from MultiVu
        message = f'The temperature is {T}, status is {sT}; '
        message += f'the field is {F}, status is {sF}. '
        print(message)

        # collect data at roughly 2s intervals
        time.sleep(2)