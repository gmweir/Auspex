from .instrument import Instrument, Command

class BOP2020M(Instrument):
    """For controlling the BOP2020M power supply via GPIB interface card"""
    output = Command("Output", get_string=":OUTP?", set_string=":OUTP {:s}", value_map={True: "ON", False: "OFF"})
    current = Command("Current", get_string=":CURR?", set_string=":CURR:LEV:IMM {:g}", value_range=(-20,20))
    voltage = Command("Voltage", get_string=":VOLT?", set_string=":VOLT:LEV:IMM {:g}", value_range=(-20,20))
    mode = Command("Mode", get_string="FUNC:MODE?", set_string="FUNC:MODE {:s}", value_map={'voltage': "VOLT", 'current': "CURR"})

    def __init__(self, name, resource_name, mode='current', **kwargs):
        super(BOP2020M, self).__init__(name, resource_name, **kwargs)
        self.interface._instrument.write_termination = u"\n"
        self.mode = 'current'
        self.interface._instrument.write('VOLT MAX')

    def shutdown(self):
        if self.output:
            if self.current != 0.0:
                for i in np.linspace(self.current, 0.0, 20):
                    self.current = i
            if self.voltage != 0.0:
                for v in np.linspace(self.voltage, 0.0, 20):
                    self.voltage = v
            self.output = False