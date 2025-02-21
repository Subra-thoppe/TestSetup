import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from modules import util
import paho.mqtt.client as mqtt

class Mqtt():

    def __init__(self) -> None:
        if "station" not in util.config:
            raise Exception(util.Red("'station' is not defined in config", ret=True))
        
        ip = "pc.minhajungdom.no"
        port = 1883
        username = "Waqas"
        password = "JMPtaIZXQCFjDoJ"

        self.station = f"K{util.config['station']}"
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=self.station)
        self.client.username = username
        self.client.password = password
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(ip, port, 60)

    def on_connect(self, client, userdata, flags, reason_code, properties):
        util.Cyan(f"Connected with result code {reason_code}")
        #self.client.subscribe(f"scs/{self.station}/+")
        self.reset()

    def on_message(self, client, userdata, msg):
        util.Cyan(f"{msg.topic}: {str(msg.payload.decode())}")

    def publish(self, topic: str, message: str | float | int):
        if isinstance(message, float):
            self.client.publish(f"scs/{self.station}/{topic}", "{:0.2f}".format(message), 0, retain=True)
        else:
            self.client.publish(f"scs/{self.station}/{topic}", str(message), 0, retain=True)

    def reset(self):
        self.resetTemperature()
        self.publish("State", "-")

    def resetTemperature(self):
        self.publish("Temperature", "-")
        self.publish("Twait", "-")
        self.publish("Tloop", "-")
        self.publish("Pressure", "-")
        self.publish("Pwait", "-")
        self.publish("Ploop", "-")
        self.publish("Channel", "-")

    def resetPressure(self):
        self.publish("Pressure", "-")
        self.publish("Pwait", "-")
        self.publish("Ploop", "-")
        self.publish("Channel", "-")

    def __repr__(self):
        return "Connected to Mqtt Broker"

if __name__ == "__main__":
    util.setColor()

    mq = Mqtt()
    mq.publish("State", "Hanji 2.0")
    #mq.client.loop_forever()