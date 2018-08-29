import os
import json
import Configuration as Config

def Load():
    configData = LoadConfigData()    
    config = Config.Configuration()
    LoadSettings(config, configData)   
    LoadPeripherals(config, configData) 
    return config

def LoadConfigData():
    configFilePath = os.path.dirname(os.path.abspath(__file__))
    configFile = open(configFilePath + '/configuration.json','r')
    configData = json.loads(configFile.read())
    configFile.close()
    return configData

def LoadSettings(config, configData):
    settings = configData["settings"]
    for setting in settings:
        name = setting["name"] 
        if (name == "DeviceId"):
            config.Settings.DeviceId = setting["value"]
        elif (name == "Season"):
            config.Settings.Season = setting["value"]

def LoadPeripherals(config, configData):    
    peripherals = configData["peripherals"]
    
    for peripheral in peripherals:
        if "thermometers" in peripheral:
            for thermometer in peripheral["thermometers"]:
                thermometerConfig = Config.Configuration.ThermometerConfiguration(thermometer["id"],thermometer["name"])
                config.Thermometers[thermometer["id"]] = thermometerConfig

        if "LEDs" in peripheral:
            for led in peripheral["LEDs"]:
                ledConfig = Config.Configuration.LEDConfiguration(led["pinNumber"],led["name"])
                config.LEDs[led["pinNumber"]] = ledConfig              