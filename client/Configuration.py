class Configuration:
    class SettingsConfiguration:
        def __init__(self):
            self.DeviceId = ''
            self.Season = '' 
        def __repr__(self):
            return "\tDeviceId = " + self.DeviceId + "\n\tSeason = " + self.Season

    class ThermometerConfiguration:
        def __init__(self, id, name):
            self.Id = id
            self.Name = name
        def __repr__(self):
            name = self.Name
            id = self.Id
            return "Id = " + id + ", Name = " + name
    
    class LEDConfiguration:
        def __init__(self, pinNumber, name):
            self.PinNumber = pinNumber
            self.Name = name
        def __repr__(self):
            pin = self.PinNumber
            name = self.Name
            return "Pin = " + pin + ", Name = " + name

    def __init__(self):
        self.Settings = Configuration.SettingsConfiguration()
        self.Thermometers = dict()
        self.LEDs = dict()

    def __repr__(self):
        try:
            textLines = []

            textLines.append("Settings:\n" + str(self.Settings) + "\n")

            textLines.append("\nThermometers:\n")
            for thermometer in self.Thermometers.values():
                textLines.append("\t" + str(thermometer) + "\n")

            textLines.append("\nLEDs:\n")
            for led in self.LEDs.values():
                textLines.append("\t" + str(led) + "\n")

            return ''.join(textLines)

        except Exception as ex:   
            return "Unable to build string representation (" + ex.message + ")"