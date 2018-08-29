import os
import glob
import time
import Configuration as Config

class TemperatureSensorController:
  


    def __init__(self, config):

        self.W1DeviceFilesById = dict()
        base_dir ='/sys/bus/w1/devices/'

        for id, name in config.TemperatureSensors.items():
            deviceFolder = glob.glob(base_dir + id)[0]
            deviceFile = deviceFolder + '/w1_slave'
            self.W1DeviceFilesById[id] = deviceFile

    def ReadTemperatures(self):
        tempsById = dict()

        for w1DeviceId, w1DeviceFile in self.W1DeviceFilesById.items():
            
            tempDataLines = self.ReadTemperatureData(w1DeviceFile)

            while tempDataLines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                tempDataLines = self.ReadTemperatureData(w1DeviceFile)

            temp = self.ParseTemperatureData(tempDataLines[1])
            tempsById[w1DeviceId] = temp

        return tempsById

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