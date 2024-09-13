from time import sleep
from umqtt.simple import MQTTClient
from config_manager import ConfigManager

class MQTTListener:
    def __init__(self):
       configManagerObj = ConfigManager()
       self.configDict = configManagerObj.readConfig()
    
    def publishMessage(self, topic, message):
        client = MQTTClient(self.configDict.get('deviceName'), self.configDict.get('mqttServer'), 1883)
        try:
            print('Connecting to MQTT Server')
            client.connect()
        except:
            print('Can\'t connect to MQTT Server')
        else:
            print('Connected to MQTT Server')
            numRetry = 1
            while numRetry <=3:
                try:
                    print('Trying to publish message to MQTT Server for '+str(numRetry)+' time')
                    client.publish(topic, message)
                except:
                    print('Can\'t publish to MQTT Server')
                    numRetry += 1
                    sleep(1)
                else:
                    print('Message published on MQTT server')
                    break
            else:
                print('Can\'t publish to MQTT Server after 3 times retry')
            client.disconnect()