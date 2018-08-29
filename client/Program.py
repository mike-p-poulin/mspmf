import os
import glob
import Logger
import time
import RPi.GPIO as GPIO
import ConfigurationLoader
import ThermometersController as ThermoController

class Program:

    def Run(self):
        try:   
            self.Initialize()
            self.DoX()

        except Exception as ex:                
            Logger.LogCritical(ex.message)


    def DoX(self):
        Logger.LogInfo("DoX:")
        Logger.LogInfo("/tConfiguring GPIO")
        GPIO.setmode(GPIO.BOARD)

        ledName = self.config.LEDs["13"].Name
        Logger.LogInfo("/tConfiguring " + ledName)        
        GPIO.setup(13, GPIO.OUT)

        while True:
            Logger.LogInfo("/tReading Temperatures")
            temps = self.thermoController.ReadTemperatures()
            targetId = self.config.Thermometers.values()[0].Id
            temp_c = temps[targetId]
            print (temp_c)
            if temp_c > 27.9:
                Logger.LogInfo("/tSetting '" + ledName + "' to On(High)")
                GPIO.output(13,GPIO.HIGH)
            else:                
                GPIO.output(13,GPIO.LOW)
                Logger.LogInfo("/tSetting '" + ledName + "' to Off(Low)")

            time.sleep(1) 

    def Initialize(self):
        Logger.Initialize()     
        Logger.LogInfo ("Loading configuration...")
        self.config = ConfigurationLoader.Load()
        Logger.LogInfo(str(self.config))
        Logger.LogInfo ("Configuration loaded\n-----------------------------------------------\n")

        Logger.LogInfo ("Initializaing Thermometers...")
        self.thermoController = ThermoController.ThermometersController(self.config)
        temps = self.thermoController.ReadTemperatures()
        for id, temp in temps.items():
            tempName = self.config.Thermometers[id].Name
            Logger.LogInfo(tempName + "(" + id + "):  " + str(temp))
        Logger.LogInfo ("Thermometers initialized\n-----------------------------------------------\n")

