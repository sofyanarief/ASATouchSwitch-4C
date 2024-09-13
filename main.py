from machine import Pin
from config_manager import ConfigManager
from wifi_manager import WifiManager
from web_server import WebServer
from touch_listener import TouchListener
from time import sleep
import machine

resetFactoryButton = Pin(5, Pin.IN)

configManagerObj = ConfigManager()
wifiManagerObj = WifiManager()

configDict = configManagerObj.readConfig()

def restartMachine():
    restartTimer = 10
    while restartTimer > 0:
        print('Restarting Device in '+str(restartTimer))
        sleep(1)
        restartTimer -=1
    print('System Is Restarted')
    machine.reset()

def resetFactory():
    pressTimer = 1
    while pressTimer <= 5:
        if resetFactoryButton.value() == 1:
            print('Factory reset button pressed for '+str(pressTimer)+' seconds')
            pressTimer += 1
            sleep(1)
        else:
            break
    else:
        if pressTimer > 4:
            configManagerObj.resetConfig()
            restartMachine()

while True:
    resetFactory()

    if configDict.get('deviceName') != wifiManagerObj.deviceName:
        configManagerObj.updateConfig('deviceName', wifiManagerObj.deviceName)
        
    if configDict.get('deviceMode') == 'standalone':
        wifiManagerObj.activateApMode()
        webServerObj = WebServer()
    elif configDict.get('deviceMode') == 'infrastructure':
        if configDict.get('ssid') != None:
            wifiManagerObj.activateStaMode(configDict.get('ssid'), configDict.get('passwd'))
            if wifiManagerObj.staIf.isconnected() != True:
                configManagerObj.resetConfig()
                restartMachine()
            else:
                touchListenerObj = TouchListener()
                touchListenerObj.detectChange()
        else:
            configManagerObj.resetConfig()
            restartMachine()
    else:
        configManagerObj.resetConfig()
        restartMachine()
        
