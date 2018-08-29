import RPi.GPIO as GPIO
import time
import Logger

class MoistureSensorController:

    def __init__(self, pinNumber, name):
        self.PinNumber = int(pinNumber)
        self.Name = name
    
    def Read(self):
        GPIO.setup(self.PinNumber, GPIO.IN)
        return GPIO.input(self.PinNumber)
    
    
    def Initialize(self):
        Logger.LogInfo("Initializating Pin " + str(self.PinNumber) + " (" + self.Name + ")")
        moisture = self.Read()
       
