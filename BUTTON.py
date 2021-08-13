import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from MQTT_TEST import Ui_MainWindow


f = 'file:///C:/Users/nguye/Downloads/Documents/1.pdf'
class BUTTON(object):

    def BUTTON_HOME(self, MainWindow):
        self.uic.Home_Button_Learn.clicked.connect(self.Show1)
    def BUTTON_LEARN(self):
        self.uic.Learn_Button_Back.clicked.connect(self.Show2)

    def Show1(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.Screen_Learn)
        self.uic.WebBrowser.dynamicCall('Navigate(const QString&)', f)

    def Show2(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.HOME)
