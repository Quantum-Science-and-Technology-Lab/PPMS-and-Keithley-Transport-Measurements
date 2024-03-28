import time
import numpy as np
from save_data_functions import save_temp_field_chamber_res_data
from pymeasure.instruments.keithley import Keithley2400

def scan_field_no_keithley(stop, rate, points, client, data):
    CurrentField, sF = client.get_field()
    set_point = stop
    wait = abs(CurrentField - set_point) / points / rate
    message = f'Set the field to {set_point} Oe and then collect data '
    message += 'while ramping'
    print('')
    print(message)
    print('')
    client.set_field(
        set_point,
        rate,
        client.field.approach_mode.linear,
        client.field.driven_mode.driven
    )
    
 
    for t in range(points):
        # chamber conditions
        start_time = time.time()
        T, F, C, res = save_temp_field_chamber_res_data()
        
        data.set_value('Time', t)
        
        data.set_value('Temperature', T)
        
        data.set_value('Field', F)
        
        data.set_value('Chamber Status', C)
        
        data.set_value('Resistance', res)
        data.write_data()
        
        end_time = time.time()
        time_diff = end_time - start_time

        if time_diff > wait:
            raise Exception('The inner sweep takes too long!')

        # poll data at roughly equal intervals based on points/ramp
        time.sleep(wait - time_diff)


def scan_field_with_keithley(
        field_stop, 
        field_rate, 
        points, 
        voltage_points,
        client,
        data,
        voltage_start = 0, 
        voltage_stop = 0.5, 
        GPIB_address_str = "GPIB0::5", 
        compliance_current = 0.1, 
        ):
    set_point = field_stop
    message = f'Set the field to {set_point} Oe and then collect data '
    message += 'while ramping'
    print('')
    print(message)
    print('')
    client.set_field(
        set_point,
        field_rate,
        client.field.approach_mode.linear,
        client.field.driven_mode.driven
    )

    try:
        # setup Keithley
        keithley = Keithley2400(GPIB_address_str)

        keithley.apply_voltage()
        keithley.compliance_current = compliance_current
        keithley.enable_source()

        for t in range(int(points/6)):

            start_time = time.time()

            # Keithley sweep
            v_list = np.linspace(voltage_start, voltage_stop, voltage_points)  # same range as Sammak et. al.

            for v in v_list:
                keithley.ramp_to_voltage(v, steps=10, pause=0.0001)  # ramp Keithley very quickly
                print(f'Vg: {keithley.voltage} ', end="")

                # chamber conditions
                T, F, C, res = save_temp_field_chamber_res_data()

                data.set_value('Time', t)
                data.set_value('Temperature', T)
                data.set_value('Field', F)
                data.set_value('Chamber Status', C)
                data.set_value('Resistance', res)
                data.set_value('Gate Voltage', keithley.voltage)
                data.write_data()

            print("done inner loop")

            end_time = time.time()
            time_diff = end_time - start_time
            
            
            if time_diff > 6:
                raise Exception('The inner sweep takes too long!')

            # poll data at roughly equal intervals based on points/ramp
            time.sleep(6 - time_diff)
        print("Done outer loop")
        keithley.shutdown()

    except Exception as e:
        # graceful shutdown of Keithley
        print(f'Encountered exception: {str(e)}')
        keithley.shutdown()


def _keithley_sweep(data):
    # setup Keithley
    keithley = Keithley2400("GPIB0::5")

    try:
        keithley.apply_voltage()
        keithley.compliance_current = 0.1
        keithley.enable_source()

        # Keithley sweep
        v_list = np.linspace(0, -2, 5)  # same range as Sammak et. al.

        for v in v_list:
            keithley.ramp_to_voltage(v, steps=10, pause=0.001)  # ramp Keithley very quickly
            print(f'Vg: {keithley.voltage} ', end="")

            # chamber conditions
            T, F, C, res = save_temp_field_chamber_res_data()

            data.set_value('Time', t)
            data.set_value('Temperature', T)
            data.set_value('Field', F)
            data.set_value('Chamber Status', C)
            data.set_value('Resistance', res)
            data.set_value('Gate Voltage', keithley.voltage)
            data.write_data()

        keithley.shutdown()

    except Exception as e:
        # graceful shutdown of Keithley
        print(f'Encountered exception: {str(e)}')
        keithley.shutdown()


def step_field_with_keithley(start, target, steps, client, data):
    points = np.linspace(start, target, steps)

    for point in points:
        client.set_field(
            point,
            20,
            client.field.approach_mode.linear,
            client.field.driven_mode.driven
        )
        client.wait_for(
            60,
            timeout_sec=0,
            bitmask=client.temperature.waitfor | client.field.waitfor
        )
        _keithley_sweep(data)