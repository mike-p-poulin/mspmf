import os
import glob
import Logger
import time
from RPi import GPIO as GPIO
import ConfigurationLoader
import TemperatureSensorController as TempSensorController
import LEDController
import MoistureSensorController
#git config --global credential.helper "cache --timeout=3600"
class Program:

    def Run(self):
        try:   
            self.Initialize()
            #self.DoX()

            while True:
                moisture = self.MoistureSensorControllers.values()[0].Read()
                print(moisture)
                time.sleep(.5)

        except Exception as ex:           
            print(ex.message)     
            Logger.LogCritical(ex.message)            

    def DoX(self):
        Logger.LogInfo("DoX:")
        Logger.LogInfo("\tConfiguring GPIO")
        

        ledName = self.Config.LEDs["13"].Name
        Logger.LogInfo("\tConfiguring Pin 13 (" + ledName + ")")        
        GPIO.setup(13, GPIO.OUT)

        while True:
            Logger.LogInfo("\tReading Temperatures")
            temps = self.tempSensorController.ReadTemperatures()
            targetId = self.Config.TemperatureSensors.values()[0].Id
            temp_c = temps[targetId]
            Logger.LogInfo("\tTemperature " + str(temp_c))
            if temp_c > 27.9:
                Logger.LogInfo("\tSetting '" + ledName + "' to On(High)")
                GPIO.output(13,GPIO.HIGH)
            else:                
                GPIO.output(13,GPIO.LOW)
                Logger.LogInfo("\tSetting '" + ledName + "' to Off(Low)")

            time.sleep(1) 
     
    def Initialize(self):
        Logger.Initialize()     
        Logger.LogInfo ("Loading configuration...")
        self.Config = ConfigurationLoader.Load()
        Logger.LogInfo(str(self.Config), includeTimestamp=False)
        Logger.LogInfo ("Configuration loaded\n-----------------------------------------------\n")

        Logger.LogInfo ("Setting GPIO Mode to 'Board' (" + str(GPIO.BOARD) + ")")
        GPIO.setmode(GPIO.BOARD)
        Logger.LogInfo ("GPIO Mode Set\n-----------------------------------------------\n")

        Logger.LogInfo ("Disabling GPIO warnings")
        GPIO.setwarnings(False)
        Logger.LogInfo ("GPIO warnings disabled\n-----------------------------------------------\n")
        
        Logger.LogInfo ("Configuring 1-wire interface")
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        Logger.LogInfo ("1-wire interface configured\n-----------------------------------------------\n")

        Logger.LogInfo ("Initializaing Temperature Sensors...")
        self.TemperatureSensorControllers = dict()
        for tempSensorConfig in self.Config.TemperatureSensors.values():
            tempSensorController = TempSensorController.TemperatureSensorController(tempSensorConfig.Id, tempSensorConfig.Name)
            self.TemperatureSensorControllers[tempSensorConfig.Id] = tempSensorController
            tempSensorController.Initialize()            
        Logger.LogInfo ("Temperature Sensors initialized\n-----------------------------------------------\n")

        Logger.LogInfo("Initializing LEDs")
        self.LEDControllers = dict()
        for ledConfig in self.Config.LEDs.values():
            ledController = LEDController.LEDController(ledConfig.PinNumber, ledConfig.Name)
            self.LEDControllers[ledConfig.PinNumber] = ledController
            ledController.Initialize()            
        Logger.LogInfo("LEDs Initialized\n-----------------------------------------------\n")

        Logger.LogInfo("Initializing Moisture Sensors")
        self.MoistureSensorControllers = dict()
        for moistureSensorConfig in self.Config.MoistureSensors.values():
            moistureSensorController = MoistureSensorController.MoistureSensorController(moistureSensorConfig.PinNumber, moistureSensorConfig.Name)
            self.MoistureSensorControllers[moistureSensorConfig.PinNumber] = moistureSensorController
            moistureSensorController.Initialize()            
        Logger.LogInfo("Moisture Sensors Initialized\n-----------------------------------------------\n")
