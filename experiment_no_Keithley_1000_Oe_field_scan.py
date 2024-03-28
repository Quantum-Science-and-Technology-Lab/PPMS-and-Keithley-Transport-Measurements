# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 14:53:09 2024

@author: Marcus Edwards, Biswas
"""
import MultiPyVu as mpv
import time
import numpy as np
from enum import Enum, auto
import utilities

utilities.instrument_ppmsmvu_setup()

with mpv.Client() as client:
    client.open()
    
    print('client accepted')
    
    # Set 5 K and -1,000 Oe
    print('Setting 5 K and -1,000 Oe')
    client.set_temperature(
        5,
        3,
        client.temperature.approach_mode.fast_settle
    )
    client.set_field(
        -1000.0,
        20, 
        client.field.approach_mode.linear,
        client.field.driven_mode.driven
    )
    
    # Wait for 60 seconds after temperature and field are stable
    print('Waiting for Temp and Field')
    client.wait_for(
        60,
        timeout_sec=0,
        bitmask=client.temperature.waitfor | client.field.waitfor
    )

        # Wait for dewar pressure
    time.sleep(60 * 60) 
    
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
    
    # configure the MultiVu columns
    data = mpv.DataFile()
    data.add_multiple_columns(['Time', 'Temperature', 'Field', 'Chamber Status', 'Resistance'])
    data.create_file_and_write_header('Resistance.dat', 'Hallbar data')
    
    # Polling temperature/field and performing resistivity measurement 
    # during a field ramp from -1,000 to 0.0 Oe at 20 Oe/sec
    utilities.scan_field_no_keithley(0, 20, 51, client, data)  
    
    print("waiting for dewar pressure (60 mins)")
    time.sleep(60 * 60)  # wait for dewar pressure to stabilize
    
    # Polling temperature/field and performing resistivity measurement 
    # During a field ramp from 0 to 1,000 Oe at 20 Oe/sec
    utilities.scan_field_no_keithley(1000, 20, 51, client, data) 
    
    time.sleep(60 * 60)  # wait for dewar pressure to stabilize
    
    print('Setting 300 K and 0 Oe')
    client.set_field(
        0.0,
        20,
        client.field.approach_mode.oscillate,
        client.field.driven_mode.driven
    )
    client.set_temperature(
        300,
        2,
        client.temperature.approach_mode.fast_settle
    )
    print('Waiting...')
    client.wait_for(
        60,
        timeout_sec=0,
        bitmask=client.temperature.waitfor | client.field.waitfor
    )
print("Finished setting to 300 K and 0 Oe")