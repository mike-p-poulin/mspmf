import RPi.GPIO as GPIO
import time
import Logger

class LEDController:

    def __init__(self, pinNumber, name):
        self.PinNumber = int(pinNumber)
        self.Name = name
    
    def TurnOn(self):
        GPIO.setup(self.PinNumber, GPIO.OUT)
        GPIO.output(self.PinNumber,GPIO.HIGH)
        
    def TurnOff(self):
        GPIO.setup(self.PinNumber, GPIO.OUT)
        GPIO.output(self.PinNumber,GPIO.LOW)
    
    def Initialize(self):
        Logger.LogInfo("Initializating Pin " + str(self.PinNumber) + " (" + self.Name + ")")
        for i in range(1,4):
            self.TurnOn()
            time.sleep(.25)
            self.TurnOff()
            time.sleep(.25)

