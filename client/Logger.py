import os
import logging
import datetime
import time

def Initialize():
    timestr = time.strftime("%Y-%m-%d %H-%M-%S")
    logFilePath = os.path.dirname(os.path.abspath(__file__))
    logFile = logFilePath + '/logs/' + timestr + " output.txt"
    logging.basicConfig(filename=logFile, level=logging.INFO)

def LogInfo(message, includeTimestamp = True):
    timeNow = str(datetime.datetime.now())
    if (includeTimestamp):
        print("[" + timeNow + "] " + message)
        logging.info("[" + timeNow + "] " + message)
    else:
        print(message)
        logging.info(message)
    

def LogWarning(message):
    timeNow = str(datetime.datetime.now())
    print("[" + timeNow + "] " + message)
    logging.warning("[" + timeNow + "] " + message)

def LogError(message):
    timeNow = str(datetime.datetime.now())
    print("[" + timeNow + "] " + message)
    logging.error("[" + timeNow + "] " + message)

def LogCritical(message):
    timeNow = str(datetime.datetime.now())
    print("[" + timeNow + "] " + message)
    logging.critical("[" + timeNow + "] " + message)
    