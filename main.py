import sys
import os
from pdf2image import convert_from_path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from MQTT_TEST import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import glob
import json


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

        # -----------(Biến tên giao diện Test)-----------------#
        self.ScreenTest_value_Qlabel_ArrayNameChoose = ["Chưa chọn","Hở mạch", "Chập chờn", "Chạm đất","Nối dương", "Bình thường"]
        self.ScreenTest_value_Qlabel_FlagButtonClick = 0
        self.ScreenTest_value_NameStudent = ""
        self.ScreenTest_value_NameITStudent = ""
        self.ScreenTest_value_NameClassStudent = ""

        self.ScreenTest_value_Qlabel_PAN_1 = 0
        self.ScreenTest_value_Qlabel_PAN_2 = 0
        self.ScreenTest_value_Qlabel_PAN_3 = 0
        self.ScreenTest_value_Qlabel_PAN_4 = 0
        self.ScreenTest_value_Qlabel_PAN_5 = 0
        self.ScreenTest_value_Qlabel_PAN_6 = 0
        self.ScreenTest_value_Qlabel_PAN_7 = 0
        self.ScreenTest_value_Qlabel_PAN_8 = 0
        self.ScreenTest_value_Qlabel_PAN_9 = 0
        self.ScreenTest_value_Qlabel_PAN_10 = 0
        self.ScreenTest_value_Qlabel_PAN_11 = 0
        self.ScreenTest_value_Qlabel_PAN_12 = 0
        self.ScreenTest_value_Qlabel_PAN_13 = 0
        self.ScreenTest_value_Qlabel_PAN_14 = 0
        self.ScreenTest_value_Qlabel_PAN_15 = 0
        self.ScreenTest_value_Qlabel_PAN_16 = 0
        self.ScreenTest_value_Qlabel_PAN_17 = 0
        self.ScreenTest_value_Qlabel_PAN_18 = 0
        self.ScreenTest_value_Qlabel_PAN_19 = 0
        self.ScreenTest_value_Qlabel_PAN_20 = 0
        self.ScreenTest_value_Qlabel_PAN_21 = 0
        self.ScreenTest_value_Qlabel_PAN_22 = 0
        self.ScreenTest_value_Qlabel_PAN_23 = 0
        self.ScreenTest_value_Qlabel_PAN_24 = 0

        self.ScreenTest_value_Qlabel_V_PAN_1 = "0V"
        self.ScreenTest_value_Qlabel_V_PAN_2 = ""
        self.ScreenTest_value_Qlabel_V_PAN_3 = ""
        self.ScreenTest_value_Qlabel_V_PAN_4 = ""
        self.ScreenTest_value_Qlabel_V_PAN_5 = ""
        self.ScreenTest_value_Qlabel_V_PAN_6 = ""
        self.ScreenTest_value_Qlabel_V_PAN_7 = ""
        self.ScreenTest_value_Qlabel_V_PAN_8 = ""
        self.ScreenTest_value_Qlabel_V_PAN_9 = ""
        self.ScreenTest_value_Qlabel_V_PAN_10 = ""
        self.ScreenTest_value_Qlabel_V_PAN_11 = ""
        self.ScreenTest_value_Qlabel_V_PAN_12 = ""
        self.ScreenTest_value_Qlabel_V_PAN_13 = ""
        self.ScreenTest_value_Qlabel_V_PAN_14 = ""
        self.ScreenTest_value_Qlabel_V_PAN_15 = ""
        self.ScreenTest_value_Qlabel_V_PAN_16 = ""
        self.ScreenTest_value_Qlabel_V_PAN_17 = ""
        self.ScreenTest_value_Qlabel_V_PAN_18 = ""
        self.ScreenTest_value_Qlabel_V_PAN_19 = ""
        self.ScreenTest_value_Qlabel_V_PAN_20 = ""
        self.ScreenTest_value_Qlabel_V_PAN_21 = ""
        self.ScreenTest_value_Qlabel_V_PAN_22 = ""
        self.ScreenTest_value_Qlabel_V_PAN_23 = ""
        self.ScreenTest_value_Qlabel_V_PAN_24 = ""

        # Khối button của màn hình Home
        self.uic.Home_Button_Learn.clicked.connect(self.Show_Screen_Learn)
        self.uic.Home_Button_Test.clicked.connect(self.Show_Screen_Test)
        self.uic.Home_Button_Setting.clicked.connect(self.Show_Screen_Setting)
        self.uic.Home_Button_Information.clicked.connect(self.Show_Screen_Information)
        # Khối button của màn hình Learn
        self.uic.Learn_Button_Back.clicked.connect(self.Learn_Button_Back)
        self.uic.Learn_Button_Exit.clicked.connect(self.Show_Screen_Home)
        self.uic.Learn_Button_Next.clicked.connect(self.Learn_Button_Next)
        self.Learn_convert_PDF_TO_IMAGE(self.Name_File_PDF)
        # Khối button của màn hình Test
        self.uic.screen_Test_Display_InputInfor_Button_Exit.clicked.connect(self.Show_Screen_Home)
        self.uic.screen_Test_Display_InputInfor_Button_Start.clicked.connect(self.screen_Test_Show_Display_Exam)

        self.uic.screen_Test_Display_Exam_Exit.clicked.connect(self.Show_Screen_Test)
        self.uic.screen_Test_Display_Exam_Submit.clicked.connect(self.Show_Screen_Test)

        self.uic.SCreen_Test_Button_PAN_1.clicked.connect(self.Screen_Test_EvenButton_PAN_1)
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
        self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_InputInfor)

    def Show_Screen_Setting(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.screen_Setting)



    def Show_Screen_Information(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.screen_Information)


#-----------------------------------------(Giao Diện học lý thuyết)-----------------------------------------------------------------------------#
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

    def Learn_convert_PDF_TO_IMAGE(self, name):
        outputDir = self.Path_Image_Screen_Learn + '/'
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        pages = convert_from_path(name, 500, size=(self.Learn_Size_X_Image_PDF, self.Learn_Size_Y_Image_PDF))
        counter = 1
        for page in pages:
            myfile = outputDir + self.Name_image_Screen_Learn + str(counter) + '.jpg'
            counter = counter + 1
            page.save(myfile, "JPEG")
#-----------------------------------------(END)-----------------------------------------------------------------------------#

#-----------------------------------------(Giao Diện kiểm tra)-----------------------------------------------------------------------------#
    def screen_Test_Show_Display_Exam(self):
        self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_Exam)

        self.ScreenTest_value_NameStudent = self.uic.screen_test_Qlineedit_Username_3.text()
        self.ScreenTest_value_NameITStudent = self.uic.screen_test_Qlineedit_IDStudent_3.text()
        self.ScreenTest_value_NameClassStudent = self.uic.screen_test_Qlineedit_IDclass_3.text()

        print(self.ScreenTest_value_NameStudent)
        print(self.ScreenTest_value_NameITStudent)
        print(self.ScreenTest_value_NameClassStudent)

    def Screen_Test_EvenButton_PAN_1(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 1
        if(self.ScreenTest_value_Qlabel_PAN_1 < len(self.ScreenTest_value_Qlabel_ArrayNameChoose)):
            self.uic.SCreen_Test_Qlabel_PAN_1.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_PAN_1])
        else:
            self.uic.SCreen_Test_Qlabel_PAN_1.setText(self.ScreenTest_value_Qlabel_V_PAN_1)


#-----------------------------------------(END)-----------------------------------------------------------------------------#
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win =  MainWindow()
    main_win.show()
    sys.exit(app.exec())