"""
Created on Wed Feb 28 14:53:09 2024

@author: Marcus Edwards, Biswas
"""
import MultiPyVu as mpv
import time
import numpy as np
import utilities


#utilities.instrument_ppmsmvu_setup() -> don't think we need this


with mpv.Client() as client:
    client.open()

    print('client accepted')
    
    # Set 4 K and 0 Oe
    print('Setting 5 K and -50,000 Oe')
    client.set_temperature(
        4,
        3,
        client.temperature.approach_mode.fast_settle
    )
    client.set_field(
        -5000.0,
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
    
# SCAN FOR BRIDGE 1

    # Configure resistivity measurement
    client.resistivity.bridge_setup(
        bridge_number=1,
        channel_on=True,
        current_limit_uA=20,
        power_limit_uW=10,
        voltage_limit_mV=100
    )

    time.sleep(5)  # recommended time to sleep for config above to take place
    
    # set the current across the hallbar TODO: ref paper Sammak et. al.
    client.resistivity.set_current(bridge_number=1, current_uA=20)
    
    # configure the MultiVu columns
    data_b1 = mpv.DataFile()
    data_b1.add_multiple_columns(['Time_b1', 'Temperature_b1', 'Field_b1', 'Chamber Status_b1', 'Resistance_b1'])
    data_b1.create_file_and_write_header('Resistance_b1.dat', 'Van der pauw bridge 1 data')
    
    # during a field ramp from -50,000 to 0.0 Oe at 20 Oe/sec
    utilities.scan_field_no_keithley(0, 20, 2051, client, data_b1, bridge=1)
    
    print("waiting for dewar pressure (60 mins)")
    time.sleep(60 * 60)  # wait for dewar pressure to stabilize
    
    # During a field ramp from 0 to 50,000 Oe at 20 Oe/sec
    utilities.scan_field_no_keithley(5000, 20, 2051, client, data_b1, bridge=1)
    
    print("waiting for dewar pressure (60 mins)")
    time.sleep(60 * 60)  # wait for dewar pressure to stabilize
    
    # During a field ramp from 50,000 to 0 Oe at 20 Oe/sec
    utilities.scan_field_no_keithley(0, 20, 2051, client, data_b1, bridge=1)
    
    print("waiting for dewar pressure (60 mins)")
    time.sleep(60 * 60)  # wait for dewar pressure to stabilize
    
    # During a field ramp from 0 to -50,000 Oe at 20 Oe/sec
    utilities.scan_field_no_keithley(-5000, 20, 2051, client, data_b1, bridge=1)

## SCAN FOR BRIDGE 2
    client.resistivity.bridge_setup(
        bridge_number=2,
        channel_on=True,
        current_limit_uA=20,
        power_limit_uW=10,
        voltage_limit_mV=100
    )

# configure the MultiVu columns
    data_b2 = mpv.DataFile()
    data_b2.add_multiple_columns(['Time_b2', 'Temperature_b2', 'Field_b2', 'Chamber Status_b2', 'Resistance_b2'])
    data_b2.create_file_and_write_header('Resistance_b1.dat', 'Van der pauw bridge 2 data')

    client.resistivity.set_current(bridge_number=2, current_uA=20)
    utilities.scan_field_no_keithley(0, 20, 2051, client, data_b2, bridge=2)

    time.sleep(60 * 60)

    utilities.scan_field_no_keithley(5000, 20, 2051, client, data_b2, bridge=2)

    time.sleep(60 * 60)

    utilities.scan_field_no_keithley(0, 20, 2051, client, data_b2, bridge=1)

    time.sleep(60 * 60)

    utilities.scan_field_no_keithley(-5000, 20, 2051, client, data_b2, bridge=2)


    #waiting 60 mins for dewar pressure
    time.sleep(60*60)
    # Set 300 K and 0 Oe
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