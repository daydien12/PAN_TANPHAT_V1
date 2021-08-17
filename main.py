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
        self.ScreenTest_value_Qlabel_ArrayNumberChoose = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.ScreenTest_value_Qlabel_ArrayVChoose = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.ScreenTest_value_Qlabel_FlagButtonClick = 0
        self.ScreenTest_value_NameStudent = ""
        self.ScreenTest_value_NameITStudent = ""
        self.ScreenTest_value_NameClassStudent = ""
        self.uic.screen_Test_Display_Choose_lineEdit.setEnabled(0)


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
        self.uic.screen_Test_Display_Exam_Submit.clicked.connect(self.screen_Test_Display_Choose_ButtonSubmit)

        self.uic.SCreen_Test_Button_PAN_1.clicked.connect(self.Screen_Test_EvenButton_PAN_1)
        self.uic.SCreen_Test_Button_PAN_2.clicked.connect(self.Screen_Test_EvenButton_PAN_2)
        self.uic.SCreen_Test_Button_PAN_3.clicked.connect(self.Screen_Test_EvenButton_PAN_3)
        self.uic.SCreen_Test_Button_PAN_4.clicked.connect(self.Screen_Test_EvenButton_PAN_4)
        self.uic.SCreen_Test_Button_PAN_5.clicked.connect(self.Screen_Test_EvenButton_PAN_5)
        self.uic.SCreen_Test_Button_PAN_6.clicked.connect(self.Screen_Test_EvenButton_PAN_6)
        self.uic.SCreen_Test_Button_PAN_7.clicked.connect(self.Screen_Test_EvenButton_PAN_7)
        self.uic.SCreen_Test_Button_PAN_8.clicked.connect(self.Screen_Test_EvenButton_PAN_8)
        self.uic.SCreen_Test_Button_PAN_9.clicked.connect(self.Screen_Test_EvenButton_PAN_9)
        self.uic.SCreen_Test_Button_PAN_10.clicked.connect(self.Screen_Test_EvenButton_PAN_10)
        self.uic.SCreen_Test_Button_PAN_11.clicked.connect(self.Screen_Test_EvenButton_PAN_11)
        self.uic.SCreen_Test_Button_PAN_12.clicked.connect(self.Screen_Test_EvenButton_PAN_12)
        self.uic.SCreen_Test_Button_PAN_13.clicked.connect(self.Screen_Test_EvenButton_PAN_13)
        self.uic.SCreen_Test_Button_PAN_14.clicked.connect(self.Screen_Test_EvenButton_PAN_14)
        self.uic.SCreen_Test_Button_PAN_15.clicked.connect(self.Screen_Test_EvenButton_PAN_15)
        self.uic.SCreen_Test_Button_PAN_16.clicked.connect(self.Screen_Test_EvenButton_PAN_16)
        self.uic.SCreen_Test_Button_PAN_17.clicked.connect(self.Screen_Test_EvenButton_PAN_17)
        self.uic.SCreen_Test_Button_PAN_18.clicked.connect(self.Screen_Test_EvenButton_PAN_18)
        self.uic.SCreen_Test_Button_PAN_19.clicked.connect(self.Screen_Test_EvenButton_PAN_19)
        self.uic.SCreen_Test_Button_PAN_20.clicked.connect(self.Screen_Test_EvenButton_PAN_20)
        self.uic.SCreen_Test_Button_PAN_21.clicked.connect(self.Screen_Test_EvenButton_PAN_21)
        self.uic.SCreen_Test_Button_PAN_22.clicked.connect(self.Screen_Test_EvenButton_PAN_22)
        self.uic.SCreen_Test_Button_PAN_23.clicked.connect(self.Screen_Test_EvenButton_PAN_23)
        self.uic.SCreen_Test_Button_PAN_24.clicked.connect(self.Screen_Test_EvenButton_PAN_24)

        self.uic.screen_Test_Display_Choose_ButtonChoose.clicked.connect(lambda:self.screen_Test_Display_Choose_radio_onClicked_and_Show_Display(self.ScreenTest_value_Qlabel_FlagButtonClick))
        self.uic.screen_Test_Display_Choose_radioButton_6.toggled.connect(lambda:self.screen_Test_Display_Choose_radio_onClicked(self.ScreenTest_value_Qlabel_FlagButtonClick))


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
        self.ScreenTest_value_Qlabel_ArrayNumberChoose = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                          0, 0, 0, 0, 0, 0]
        self.ScreenTest_value_Qlabel_ArrayVChoose = [0, 0, 0, 0, 0, 0, 0, 0,
                                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                     0, 0, 0, 0, 0]

        self.screen_Test_Display_ClearChoose()
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

    def screen_Test_Show_Display_Choose(self, Number):
        self.uic.screen_Test_Display_Choose_Qlabel_PAN_Number.setText("PAN "+str(Number))
        self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_Choose)

    def Screen_Test_EvenButton_PAN_1(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 1
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_2(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 2
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_3(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 3
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_4(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 4
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_5(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 5
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_6(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 6
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_7(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 7
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_8(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 8
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_9(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 9
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_10(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 10
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_11(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 11
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_12(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 12
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_13(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 13
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_14(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 14
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_15(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 15
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_16(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 16
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_17(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 17
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_18(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 18
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_19(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 19
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_20(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 20
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_21(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 21
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_22(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 22
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_23(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 23
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def Screen_Test_EvenButton_PAN_24(self):
        self.ScreenTest_value_Qlabel_FlagButtonClick = 24
        self.screen_Test_Show_Display_Choose(self.ScreenTest_value_Qlabel_FlagButtonClick)

    def screen_Test_Display_Choose_radio_onClicked_and_Show_Display(self, Number_Button):
        self.screen_Test_Show_Display_Exam()
        self.screen_Test_Display_Choose_radio_onClicked(Number_Button)
        print(self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button])
        self.ScreenTest_value_Qlabel_ArrayVChoose[Number_Button] = self.uic.screen_Test_Display_Choose_lineEdit.text()
        self.screen_Test_Display_Choose_radio_SelectChoose(Number_Button)

    def screen_Test_Display_Choose_radio_SelectChoose(self, Number_Button):
        if(Number_Button == 1):
            if(self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_1.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_1.setText(self.uic.screen_Test_Display_Choose_lineEdit.text()+' V')
        if (Number_Button == 2):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_2.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_2.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 3):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_3.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_3.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 4):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_4.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_4.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 5):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_5.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_5.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 6):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_6.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_6.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 7):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_7.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_7.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 8):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_8.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_8.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 9):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_9.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_9.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 10):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_10.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_10.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 11):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_11.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_11.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 12):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_12.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_12.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 13):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_13.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_13.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 14):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_14.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_14.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 15):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_15.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_15.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 16):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_16.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_16.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 17):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_17.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_17.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 18):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_18.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_18.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 19):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_19.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_19.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 20):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_20.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_20.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 21):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_21.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_21.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 22):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_22.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_22.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 23):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_23.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_23.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 24):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_24.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[
                                                              self.ScreenTest_value_Qlabel_ArrayNumberChoose[
                                                                  Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_24.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')


    def screen_Test_Display_Choose_radio_onClicked(self, Number_Button):

        if self.uic.screen_Test_Display_Choose_radioButton_1.isChecked():
            self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] = 1

        if self.uic.screen_Test_Display_Choose_radioButton_2.isChecked():
            self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] = 2

        if self.uic.screen_Test_Display_Choose_radioButton_3.isChecked():
            self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] = 3

        if self.uic.screen_Test_Display_Choose_radioButton_4.isChecked():
            self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] = 4

        if self.uic.screen_Test_Display_Choose_radioButton_5.isChecked():
            self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] = 5

        if self.uic.screen_Test_Display_Choose_radioButton_6.isChecked():
            self.uic.screen_Test_Display_Choose_lineEdit.setEnabled(1)
            self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] = 6
        else:
            self.uic.screen_Test_Display_Choose_lineEdit.setEnabled(0)
            self.uic.screen_Test_Display_Choose_lineEdit.clear()

    def screen_Test_Display_Choose_ButtonSubmit(self):
        for x in range(1,25):
            if(self.ScreenTest_value_Qlabel_ArrayNumberChoose[x] >= 6):
                print(self.ScreenTest_value_Qlabel_ArrayVChoose[x]+' V')
            else:
                print(self.ScreenTest_value_Qlabel_ArrayNumberChoose[x])
    def screen_Test_Display_ClearChoose(self):
        for x in range(1, 25):
            self.screen_Test_Display_Choose_radio_SelectChoose(x)
#-----------------------------------------(END)-----------------------------------------------------------------------------#
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win =  MainWindow()
    main_win.show()
    sys.exit(app.exec())