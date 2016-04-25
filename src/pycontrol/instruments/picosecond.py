from .instrument import Instrument, StringCommand, FloatCommand

class Picosecond10070A(Instrument):
    """Picosecond 10070A Pulser"""
    amplitude      = FloatCommand(scpi_string="amplitude?")
    delay          = FloatCommand(scpi_string="delay?")
    duration       = FloatCommand(scpi_string="duration?")
    level          = FloatCommand(scpi_string="level?")
    period         = FloatCommand(scpi_string="period?")
    frequency      = FloatCommand(scpi_string="frequency?")
    offset         = FloatCommand(scpi_string="offset?")
    trigger_source = StringCommand(scpi_string="trigger", allowed_values=["INT", "EXT", "GPIB"])

    def __init__(self, resource_name, *args, **kwargs):
        super(Picosecond10070A, self).__init__(resource_name, *args, **kwargs)
        self.name = "Picosecond 10070A Pulser"
        self.interface.write("header off")
        self.interface.write("trigger GPIB")
        self.interface._resource.read_termination = u"\n"

    # This command is syntactically screwy
    @property
    def output(self):
        return self.interface.query("enable?") == "YES"
    @output.setter
    def output(self, value):
        if value:
            self.interface.write("enable")
        else:
            self.interface.write("disable")

    def trigger(self):
        self.interface.write("*TRG")
