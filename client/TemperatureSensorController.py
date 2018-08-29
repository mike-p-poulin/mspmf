import glob
import time

class TemperatureSensorController(object):

    def __init__(self, id, name):
        self.Id = id
        self.Name = name        
        deviceFolder = glob.glob('/sys/bus/w1/devices/' + id)[0]
        self.W1DeviceFile = deviceFolder + '/w1_slave'

    def Read(self):
        tempDataLines = self.ReadTemperatureData(self.W1DeviceFile)

        while tempDataLines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            tempDataLines = self.ReadTemperatureData(self.W1DeviceFile)

        temp = self.ParseTemperatureData(tempDataLines[1])
        return temp

    def ReadTemperatureData(self, deviceFile):
            f = open(deviceFile)
            lines = f.readlines()
            f.close
            return lines

    def ParseTemperatureData(self, tempData):
        equals_pos = tempData.find('t=')
        
        if equals_pos != -1:
            temp_string = tempData[equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32
            return temp_c