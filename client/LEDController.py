import RPi.GPIO as GPIO
import time
import Logger

class LEDController:

    def __init__(self, pinNumber, name):
        self.PinNumberText = pinNumber
        self.PinNumber = int(pinNumber)
        self.Name = name
    
    def TurnOn(self):
        Logger.LogInfo("LED: Turning on '" + self.Name + "' (at pin " + self.PinNumberText + ")")
        GPIO.setup(self.PinNumber, GPIO.OUT)
        GPIO.output(self.PinNumber,GPIO.HIGH)
        Logger.LogInfo("LED: Turned on '" + self.Name + "' (at pin " + self.PinNumberText + ")")
        
    def TurnOff(self):
        Logger.LogInfo("LED: Turning off '" + self.Name + "' (at pin " + self.PinNumberText + ")")
        GPIO.setup(self.PinNumber, GPIO.OUT)
        GPIO.output(self.PinNumber,GPIO.LOW)
        Logger.LogInfo("LED: Turned off '" + self.Name + "' (at pin " + self.PinNumberText + ")")
    
    def Initialize(self):
        Logger.LogInfo("LED: Initializaing '" + self.Name + "' (at pin " + self.PinNumberText + ")")
        self.TurnOn()
        time.sleep(.5)
        self.TurnOff()
        Logger.LogInfo("LED: Initialized '" + self.Name + "' (at pin " + self.PinNumberText + ")")

