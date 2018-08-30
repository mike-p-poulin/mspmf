import os
import sys
import select
import traceback
import glob
import Logger
import time
from RPi import GPIO as GPIO
import ConfigurationLoader
import TemperatureSensorController as TempSensorController
import LEDController
import PinAssignments

#git config --global credential.helper "cache --timeout=3600"
class Program:

    def Run(self):
        try:   
            self.Initialize()
            Logger.LogInfo("Entering main loop")

            exitRequested = False
            while not exitRequested: 
                self.IndicateHearbeat()

                if select.select([sys.stdin,],[],[],2.0)[0]:
                    Logger.LogInfo("Exit requested by user")
                    exitRequested = True
                else:
                    x=1

        except Exception as ex:           
            Logger.LogCritical(ex.message + "\n" + traceback.format_exc()) 
            Logger.LogCritical("Indicating System Problem")
            self.IndicateSystemProblem()        
        finally:
            Logger.LogInfo("Cleaning up GPIO")
            GPIO.cleanup()          

     
    def Initialize(self):
        try:
            Logger.Initialize()             
            Logger.LogInfo ("Loading configuration")
            self.Config = ConfigurationLoader.Load()
            Logger.LogInfo(str(self.Config), includeTimestamp=False)
            Logger.LogInfo ("Configuration loaded\n-----------------------------------------------\n")

            Logger.LogInfo("Starting Initialization\n-----------------------------------------------\n")

            Logger.LogInfo ("Setting GPIO Mode to 'Board' (" + str(GPIO.BOARD) + ")")
            GPIO.setmode(GPIO.BOARD)
            Logger.LogInfo ("GPIO Mode Set\n-----------------------------------------------\n")

            Logger.LogInfo ("Disabling GPIO warnings")
            GPIO.setwarnings(False)
            Logger.LogInfo ("GPIO warnings disabled\n-----------------------------------------------\n")

            Logger.LogInfo("Initializing LEDs")
            self.LEDControllers = dict()
            for ledConfig in self.Config.LEDs.values():
                ledController = LEDController.LEDController(ledConfig.PinNumber, ledConfig.Name)
                self.LEDControllers[ledConfig.PinNumber] = ledController
                ledController.Initialize()   
                Logger.LogInfo("", includeTimestamp = False)        
            Logger.LogInfo("LEDs Initialized\n-----------------------------------------------\n")


            Logger.LogInfo ("Configuring 1-wire interface")
            os.system('modprobe w1-gpio')
            os.system('modprobe w1-therm')
            Logger.LogInfo ("1-wire interface configured\n-----------------------------------------------\n")

            Logger.LogInfo ("Initializaing Temperature Sensors")
            self.TemperatureSensorControllers = dict()
            for tempSensorConfig in self.Config.TemperatureSensors.values():
                tempSensorController = TempSensorController.TemperatureSensorController(tempSensorConfig.Id, tempSensorConfig.Name)
                self.TemperatureSensorControllers[tempSensorConfig.Id] = tempSensorController
                tempSensorController.Initialize()            
                Logger.LogInfo("", includeTimestamp = False)
            Logger.LogInfo ("Temperature Sensors initialized\n-----------------------------------------------\n")
                    
            self.LEDControllers[PinAssignments.PinNumbers.LED_SystemOK.value].TurnOn()
            Logger.LogInfo("Initialization Complete\n-----------------------------------------------\n")
        
        except Exception as ex:           
            Logger.LogCritical(ex.message + "\n" + traceback.format_exc()) 
            Logger.LogCritical("Indicating System Problem")
            self.IndicateSystemProblem()
           

    def IndicateSystemProblem(self):
        self.LEDControllers[PinAssignments.PinNumbers.LED_SystemOK.value].TurnOff(silent=True)

        exitRequested = False
        while not exitRequested:     
            if select.select([sys.stdin,],[],[],.1)[0]:
                exitRequested = True
            
            self.LEDControllers[PinAssignments.PinNumbers.LED_SystemProblem.value].TurnOn(silent=True)
            time.sleep(.5)
            self.LEDControllers[PinAssignments.PinNumbers.LED_SystemProblem.value].TurnOff(silent=True)
            time.sleep(.5)

    def IndicateHearbeat(self):
        self.LEDControllers[PinAssignments.PinNumbers.LED_SystemOK.value].TurnOff(silent=True)
        time.sleep(.3)
        self.LEDControllers[PinAssignments.PinNumbers.LED_SystemOK.value].TurnOn(silent=True)
        time.sleep(.3)
        self.LEDControllers[PinAssignments.PinNumbers.LED_SystemOK.value].TurnOff(silent=True)
        time.sleep(.3)
        self.LEDControllers[PinAssignments.PinNumbers.LED_SystemOK.value].TurnOn(silent=True)

