class Configuration:
    class SettingsConfiguration:
        def __init__(self):
            self.DeviceId = ''
            self.Season = '' 
        def __repr__(self):
            return "\tDeviceId = " + self.DeviceId + "\n\tSeason = " + self.Season

    class TemperatureSensorConfiguration:
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

    class MoistureSensorConfiguration:
        def __init__(self, pinNumber, name):
            self.PinNumber = pinNumber
            self.Name = name
        def __repr__(self):
            pin = self.PinNumber
            name = self.Name
            return "Pin = " + pin + ", Name = " + name


    def __init__(self):
        self.Settings = Configuration.SettingsConfiguration()
        self.TemperatureSensors = dict()
        self.MoistureSensors = dict()
        self.LEDs = dict()

    def __repr__(self):
        try:
            textLines = []

            textLines.append("Settings:\n" + str(self.Settings) + "\n")

            textLines.append("\nTemperature Sensors:\n")
            for tempSensor in self.TemperatureSensors.values():
                textLines.append("\t" + str(tempSensor) + "\n")

            textLines.append("\nLEDs:\n")
            for led in self.LEDs.values():
                textLines.append("\t" + str(led) + "\n")

            textLines.append("\nMoisture Sensors:\n")
            for moistureSensor in self.MoistureSensors.values():
                textLines.append("\t" + str(moistureSensor) + "\n")

            return ''.join(textLines)

        except Exception as ex:   
            return "Unable to build string representation (" + ex.message + ")"