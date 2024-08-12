# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 14:53:09 2024

@author: Marcus Edwards, biswas
"""
import MultiPyVu as mpv
import time
import numpy as np
from enum import Enum, auto
import utilities
from pymeasure.instruments.keithley import Keithley2400


utilities.instrument_ppmsmvu_setup()


with mpv.Client() as client:
    client.open()

    print('client accepted')

    # Set 5 K and 0 Oe
    print('Setting 5 K and -50,000 Oe')
    client.set_temperature(
        5,
        3,
        client.temperature.approach_mode.fast_settle
    )

    # configure the MultiVu columns
    data = mpv.DataFile()
    data.add_multiple_columns(['Time', 'Temperature', 'Field', 'Chamber Status', 'Resistance', 'Gate Voltage'])
    data.create_file_and_write_header('Resistance.dat', 'Hallbar data')

    # Configure resistivity measurement
    client.resistivity.bridge_setup(
        bridge_number=1,
        channel_on=True,
        current_limit_uA=50,
        power_limit_uW=500,
        voltage_limit_mV=1000
    )
    time.sleep(5)  # recommended time to sleep for config above to take place

    # set the current across the hallbar TODO: ref paper Sammak et. al.
    client.resistivity.set_current(bridge_number=1, current_uA=50)
    
    utilities.step_field_with_keithley(0, -50000, 5, client, data)

    # step_field_with_keithley already has a wait for field and temperature

    time.sleep(60 * 60)  # wait for dewar pressure to stabilize

    # step the field and sweep Vg at 5 steps between 0 and -50000 Oe
    utilities.step_field_with_keithley(-50000, 0, 5, client, data)

    time.sleep(60 * 60)  # wait for dewar pressure to stabilize

    # step the field and sweep Vg at 5 steps between 0 and 50000 Oe
    utilities.step_field_with_keithley(0, 50000, 5, client, data)

    time.sleep(60 * 60)  # wait for dewar pressure to stabilize

    # step the field and sweep Vg at 5 steps between 0 and 50000 Oe
    utilities.step_field_with_keithley(50000, 0, 5, client, data)

    time.sleep(60 * 60)  # wait for dewar pressure to stabilize

    # Set 300 K
    print('Setting 300 K')
    client.set_temperature(
        300,
        2,
        client.temperature.approach_mode.fast_settle
    )
    # Wait for 60 seconds after temperature and field are stable
    print('Waiting...')
    client.wait_for(
        60,
        timeout_sec=0,
        bitmask=client.temperature.waitfor | client.field.waitfor
    )