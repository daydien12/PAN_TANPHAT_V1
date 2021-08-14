import sys
import os
from pdf2image import convert_from_path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from MQTT_TEST import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import glob

class MainWindow:
    def __init__(self, parent=None):
        super().__init__()
        # -----------(Khởi tao Class)-----------------#
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.uic.stackedWidget.setCurrentWidget(self.uic.HOME)
        #-----------(Biến đếm chuyển ảnh và biến lưu số lượng ảnh có trong file giao diện learn)-----------------#
        self.Count_next_image = 1
        self.Number_Image_Learn = 1
        # -----------(Biến tên và đường dẫn giao diện learn)-----------------#
        self.Path_Image_Screen_Learn = 'Image_Learn'
        self.Name_image_Screen_Learn = 'output'
        self.Name_File_PDF = 'sample.pdf'
        self.Learn_Size_X_Image_PDF = 1024
        self.Learn_Size_Y_Image_PDF = 500

        # Khối button của màn hình Home
        self.uic.Home_Button_Learn.clicked.connect(self.Show_Screen_Learn)
        self.uic.Home_Button_Test.clicked.connect(self.Show_Screen_Test)
        self.uic.Home_Button_Setting.clicked.connect(self.Show_Screen_Setting)
        self.uic.Home_Button_Information.clicked.connect(self.Show_Screen_Information)
        # Khối button của màn hình Learn
        self.uic.Learn_Button_Back.clicked.connect(self.Learn_Button_Back)
        self.uic.Learn_Button_Exit.clicked.connect(self.Show_Screen_Home)
        self.uic.Learn_Button_Next.clicked.connect(self.Learn_Button_Next)
        self.convert(self.Name_File_PDF)

    def show(self):
        self.main_win.show()

    def Show_Screen_Home(self):
        Count_next_image = 1
        self.uic.stackedWidget.setCurrentWidget(self.uic.HOME)

    def Show_Screen_Learn(self):
        self.Learn_Get_Number_File()
        self.Learn_Show_Imgae_Learn()
        self.uic.stackedWidget.setCurrentWidget(self.uic.Screen_Learn)

    def Show_Screen_Test(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.screen_Test)

    def Show_Screen_Setting(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.screen_Setting)

    def Show_Screen_Information(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.screen_Information)

    def convert(self,name):
        outputDir = self.Path_Image_Screen_Learn + '/'
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        pages = convert_from_path(name, 500, size=(self.Learn_Size_X_Image_PDF,self.Learn_Size_Y_Image_PDF))
        counter = 1
        for page in pages:
            myfile = outputDir + self.Name_image_Screen_Learn + str(counter) + '.jpg'
            counter = counter + 1
            page.save(myfile, "JPEG")

#-----------------------------------------(điều khiển next hoặc back của giao diện learn)-----------------------------------------------------------------------------#
    def Learn_Button_Next(self):
        if( self.Count_next_image < self.Number_Image_Learn):
            self.Count_next_image = self.Count_next_image + 1
        else:
            self.Count_next_image = 1
        self.Learn_Show_Imgae_Learn()

    def Learn_Button_Back(self):
        if (self.Count_next_image > 1):
            self.Count_next_image = self.Count_next_image - 1
        else:
            self.Count_next_image = self.Number_Image_Learn
        self.Learn_Show_Imgae_Learn()

    def Learn_Show_Imgae_Learn(self):
        str_name = self.Path_Image_Screen_Learn + '/' + self.Name_image_Screen_Learn + str(self.Count_next_image) + '.jpg'
        self.uic.show_image_learn.setPixmap(QtGui.QPixmap(str_name))

    def Learn_Get_Number_File(self):
        files = [f for f in glob.glob(self.Path_Image_Screen_Learn + '/' + "**/*.jpg", recursive=True)]
        self.Number_Image_Learn = len(files)
#-----------------------------------------(END)-----------------------------------------------------------------------------#

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win =  MainWindow()
    main_win.show()

    sys.exit(app.exec())