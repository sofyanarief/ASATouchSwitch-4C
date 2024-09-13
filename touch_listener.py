from config_manager import ConfigManager
from machine import Pin, ADC
from time import sleep
from mqtt_listener import MQTTListener

class TouchListener:
    def __init__(self):
        configManagerObj = ConfigManager()
        self.configDict = configManagerObj.readConfig()
        self.S0 = Pin(self.configDict.get('s0Pin'), Pin.OUT)
        self.S1 = Pin(self.configDict.get('s1Pin'), Pin.OUT)
        self.EN = Pin(self.configDict.get('enPin'), Pin.OUT)
        self.SG = ADC(self.configDict.get('sgPin'))
        self.CN = 4
        self.LCN = [0,0,0,0]

    def selectChannel(self,channel):
        self.S0.value(channel & 0x01)
        self.S1.value((channel >> 1) & 0x01)
        self.EN.value(0)
        return str(str(self.S0.value())+str(self.S1.value())+str(self.EN.value()))
    
    def resetMux(self):
        self.EN.value(1)

    def detectChange(self):
        mqttListenerObj = MQTTListener()
        print('Ready to detect button')
        while True:
            #print("++++++++++++++++++++")
            #print("LCN: "+str(LCN))
            j = 0
            k = 0
            NCN = [0,0,0,0]
            while j < 4:
                i = 0
                while i < self.CN:
                    chan = self.selectChannel(i)
                    sleep(0.1)
                    val = self.SG.read()
                    #print("Channel "+str(chan)+" ---> "+str(i)+" ---> "+str(val))
                    self.resetMux()
                    NCN[i] = NCN[i]+val
                    NCN[i] = NCN[i]/2
                    i+=1
                j+=1
            #print("NCN: "+str(NCN))
            while k < 4:
                if k == 0:
                    topic = self.configDict.get('ch1Topic')
                elif k == 1:
                    topic = self.configDict.get('ch2Topic')
                elif k == 2:
                    topic = self.configDict.get('ch3Topic')
                elif k == 3:
                    topic = self.configDict.get('ch4Topic')

                if NCN[k] > 100:
                    if self.LCN[k] < 100:
                        print("Channel "+str(k)+": ON")
                        mqttListenerObj.publishMessage(topic, 'ON')
                else:
                    if self.LCN[k] > 100:
                        print("Channel "+str(k)+": OFF")
                        mqttListenerObj.publishMessage(topic, 'OFF')
                k+=1
            self.LCN = NCN
            #print("--------------------")