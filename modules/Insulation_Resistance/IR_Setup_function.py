def IR_Setupfunction():

    import pyvisa
    import time
    

    rm = pyvisa.ResourceManager()
    ir = rm.open_resource("ASRL7::INSTR")
    ir.read_termination = "\r\n"
    ir.write_termination= "\r\n"
    ir.baud_rate = 38400
    ir.timeout=5000
    # all setting
    print(ir.query("*IDN?"))
    #ir.clear()
    ir.write("LOWER 200E6,ON")  # setting resistance lower limit 
    time.sleep(1)
    ir.write("UPPER 5000E6,OFF") # setting resistance upper limit , OFF sets the "upper ON" light off 
    time.sleep(1)
    ir.write("TESTV 50") # setting test voltage to 50 V
    time.sleep(1)
    #ir.write("TIMER 1.5,ON") # setting testing time   #30,09,24
    ir.write("TIMER 10,ON") # setting testing time  # 10 i smimimum
    time.sleep(1)
    #ir.write("PASSHOLD ON") # SETTING PASS HOLD ON / OFF  #30,09,24

    ir.write("PASSHOLD ON") # SETTING PASS HOLD ON / OFF 
    time.sleep(1)
    ir.write("BVOL 10") # BUZZER VOLUME  MINIMUM 0 , MAXIMUM 5000
    time.sleep(1)

    #ir.write("WAITTIME 1.2") # waititme .. waitime should be less than test time  wait ime 1.2 , test time 1.5 seems tio be optimal to show pass fail result
    ir.write("WAITTIME 3") # waititme .. waitime should be less than test time  wait ime 1.2 , test time 1.5 seems tio be optimal to show pass fail result
    time.sleep(1)
    #ir.close()

