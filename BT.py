
import paho.mqtt.client as mqtt  # pip install paho-mqtt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message
        self.btnLedOn = QPushButton('ON')
        self.btnLedOff = QPushButton('OFF')
        self.labelState = QLabel('State')
        #self.mqtt_client.username_pw_set(username="lee2002w", password="Lsh312453124%")
        self.mqtt_client.connect("192.168.110.129", 1883, 60)
        print("Connected with result code ")
        self.mqtt_client.loop_start()
        self.initLayout()
        self.initControls()

    def release(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

    def initLayout(self):
        wgt = QWidget()
        self.setCentralWidget(wgt)
        vbox = QVBoxLayout(wgt)
        vbox.addWidget(self.labelState)
        vbox.addWidget(self.btnLedOn)
        vbox.addWidget(self.btnLedOff)

    def initControls(self):
        self.btnLedOn.clicked.connect(lambda: self.mqtt_publish())
        self.btnLedOff.clicked.connect(lambda: self.mqtt_publish())

    def on_mqtt_connect(self, client, userdata, flags, rc):
        self.mqtt_client.subscribe('test')

    def on_mqtt_message(self, client, userdata, message):
        print( message.topic + " " + str(message.payload))

    def mqtt_publish(self):
        self.mqtt_client.publish('test', "xin chao")

if __name__ == '__main__':
    app = QApplication([])
    wnd = MyWindow()
    wnd.show()
    app.exec_()
    wnd.release()