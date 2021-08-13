import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from MQTT_TEST import Ui_MainWindow


f = 'file:///C:/Users/nguye/Downloads/Documents/1.pdf'


class MainWindow:
    def __init__(self, parent=None):
        super().__init__()
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.uic.stackedWidget.setCurrentWidget(self.uic.HOME)
        # Khối button của màn hình Home
        self.uic.Home_Button_Learn.clicked.connect(self.Show_Screen_Learn)
        self.uic.Home_Button_Test.clicked.connect(self.Show_Screen_Test)
        self.uic.Home_Button_Setting.clicked.connect(self.Show_Screen_Setting)
        self.uic.Home_Button_Information.clicked.connect(self.Show_Screen_Information)
        # Khối button của màn hình Learn
        self.uic.Learn_Button_Back.clicked.connect(self.Show_Screen_Home)

        print("vao")
    def show(self):
        self.main_win.show()

    def Show_Screen_Home(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.HOME)



    def Show_Screen_Learn(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.Screen_Learn)
        self.uic.WebBrowser.dynamicCall('Navigate(const QString&)', f)

    def Show_Screen_Test(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.screen_Test)


    def Show_Screen_Setting(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.screen_Setting)

    def Show_Screen_Information(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.screen_Information)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win =  MainWindow()
    main_win.show()
    sys.exit(app.exec())