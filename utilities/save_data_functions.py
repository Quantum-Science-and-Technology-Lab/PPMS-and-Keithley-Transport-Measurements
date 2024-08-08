def save_temp_field_chamber_res_data(client, bridge=1):
    '''
    Returns
    -------
    T : temperature
    F : magnetic Field
    C : chamber status
    res : resistance of configured bridge
    '''
    T, sT = client.get_temperature()
    F, sF = client.get_field()
    C = client.get_chamber()
    res = client.resistivity.get_resistance(bridge_number=bridge)
    current = client.resistivity.get_current(bridge_number=bridge)
    

    print(f'{T:{7}.{3}f} {sT:{10}} {F:{7}} {sF:{20}} {C:{15}} {res}')
    return T, F, C, res, current