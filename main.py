import sys
import os
import glob
import json
import socket
from pdf2image import convert_from_path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings, QPoint
from MQTT_TEST import Ui_MainWindow
import paho.mqtt.client as mqtt  # pip install paho-mqtt
from numpy import random
class MainWindow:
    def __init__(self, parent=None):
        super().__init__()
        # -----------(Khởi tao Class)-----------------#
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.uic.stackedWidget.setCurrentWidget(self.uic.HOME)
        self.mqtt_client = mqtt.Client()
        self.Sys_value_ChooseScreenTest = 0
        # -----------(Lưu mật khẩu)-----------------#
        self.settings = QSettings('PAN','PAN')
        #settings.setValue('list_value', "25")
        #settings.setValue('dict_value', {'one': 1, 'two': 2})

        #-----------(Biến đếm chuyển ảnh và biến lưu số lượng ảnh có trong file giao diện learn)-----------------#
        self.Count_next_image = 1
        self.Number_Image_Learn = 1
        # -----------(Biến MQTT)-----------------#
        self.Mqtt_Port = 1883
        self.TopicSub = "test"
        self.TopicPub = "IP"
        # -----------(Biến tên và đường dẫn giao diện learn)-----------------#
        self.Path_Image_Screen_Learn = 'Image_Learn'
        self.Name_image_Screen_Learn = 'output'
        self.Name_File_PDF = 'sample.pdf'
        self.Learn_Size_X_Image_PDF = 1024
        self.Learn_Size_Y_Image_PDF = 500

        # -----------(Biến tên giao diện Test)-----------------#
        self.ScreenTest_value_Qlabel_ArrayNameChoose = ["Chưa chọn","Hở mạch", "Chập chờn", "Chạm đất","Nối dương", "Bình thường"]
        self.ScreenTest_value_Qlabel_ArrayNumberChoose = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.ScreenTest_value_Qlabel_FlagButtonClick = 0
        self.ScreenTest_value_NameStudent = ""
        self.ScreenTest_value_NameITStudent = ""
        self.ScreenTest_value_NameClassStudent = ""
        self.uic.screen_Test_Display_Choose_lineEdit.setEnabled(0)
        # -----------(Biến tên giao diện setting)-----------------#
        self.ScreenSetting_value_ArrayGetCurrentText = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.ScreenSetting_value_ArrayGetCurrentIndex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


        # Khối button của màn hình Home
        self.uic.Home_Button_Learn.clicked.connect(self.Show_Screen_Learn)
        self.uic.Home_Button_Test.clicked.connect(lambda:self.Show_Screen_Test(1))
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

        self.uic.screen_Test_Display_Answer_Exit.clicked.connect(self.Show_Screen_Home)
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
        # Khối button của màn hình Setting
        self.uic.screen_Setting_Home_ButtonCreatePractice.clicked.connect(self.screen_Setting_Show_Display_Practice)
        self.uic.screen_Setting_Home_ButtonCreateTest.clicked.connect(lambda:self.Show_Screen_Test(2))
        self.uic.screen_Setting_Home_ButtonRamdom.clicked.connect(self.screen_Setting_RamdomExercise)
        self.uic.screen_Setting_Home_ButtonExit.clicked.connect(self.Show_Screen_Home)

        self.uic.screen_Setting_practice_ButtonExit.clicked.connect(self.Show_Screen_Setting)

        self.uic.screen_setting_Home_ComboBox_1.activated.connect(self.screen_Setting_Check_selectVoltage_1)
        self.uic.screen_setting_Home_ComboBox_2.activated.connect(self.screen_Setting_Check_selectVoltage_2)
        self.uic.screen_setting_Home_ComboBox_3.activated.connect(self.screen_Setting_Check_selectVoltage_3)
        self.uic.screen_setting_Home_ComboBox_4.activated.connect(self.screen_Setting_Check_selectVoltage_4)
        self.uic.screen_setting_Home_ComboBox_5.activated.connect(self.screen_Setting_Check_selectVoltage_5)
        self.uic.screen_setting_Home_ComboBox_6.activated.connect(self.screen_Setting_Check_selectVoltage_6)
        self.uic.screen_setting_Home_ComboBox_7.activated.connect(self.screen_Setting_Check_selectVoltage_7)
        self.uic.screen_setting_Home_ComboBox_8.activated.connect(self.screen_Setting_Check_selectVoltage_8)
        self.uic.screen_setting_Home_ComboBox_9.activated.connect(self.screen_Setting_Check_selectVoltage_9)
        self.uic.screen_setting_Home_ComboBox_10.activated.connect(self.screen_Setting_Check_selectVoltage_10)
        self.uic.screen_setting_Home_ComboBox_11.activated.connect(self.screen_Setting_Check_selectVoltage_11)
        self.uic.screen_setting_Home_ComboBox_12.activated.connect(self.screen_Setting_Check_selectVoltage_12)
        self.uic.screen_setting_Home_ComboBox_13.activated.connect(self.screen_Setting_Check_selectVoltage_13)
        self.uic.screen_setting_Home_ComboBox_14.activated.connect(self.screen_Setting_Check_selectVoltage_14)
        self.uic.screen_setting_Home_ComboBox_15.activated.connect(self.screen_Setting_Check_selectVoltage_15)
        self.uic.screen_setting_Home_ComboBox_16.activated.connect(self.screen_Setting_Check_selectVoltage_16)
        self.uic.screen_setting_Home_ComboBox_17.activated.connect(self.screen_Setting_Check_selectVoltage_17)
        self.uic.screen_setting_Home_ComboBox_18.activated.connect(self.screen_Setting_Check_selectVoltage_18)
        self.uic.screen_setting_Home_ComboBox_19.activated.connect(self.screen_Setting_Check_selectVoltage_19)
        self.uic.screen_setting_Home_ComboBox_20.activated.connect(self.screen_Setting_Check_selectVoltage_20)
        self.uic.screen_setting_Home_ComboBox_21.activated.connect(self.screen_Setting_Check_selectVoltage_21)
        self.uic.screen_setting_Home_ComboBox_22.activated.connect(self.screen_Setting_Check_selectVoltage_22)
        self.uic.screen_setting_Home_ComboBox_23.activated.connect(self.screen_Setting_Check_selectVoltage_23)
        self.uic.screen_setting_Home_ComboBox_24.activated.connect(self.screen_Setting_Check_selectVoltage_24)

        #self.Mqtt_Run()



    def show(self):
        self.main_win.show()

    # -----------------------------------------(Cấu hình MQTT)-----------------------------------------------------------------------------#


    def Mqtt_Get_IPAddr(self):
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        return hostname, IPAddr;

    def Mqtt_Run(self, Mqtt_Host):
        try:
            self.mqtt_client.on_connect = self.Mqtt_connect
            self.mqtt_client.on_message = self.Mqtt_message
            self.mqtt_client.connect(Mqtt_Host, self.Mqtt_Port, 60)
            Flag = 1
        except Exception as e:
            Flag = 0
            pass
        if(Flag == 1):
            self.mqtt_client.loop_start()


    def Mqtt_connect(self, client, userdata, flags, rc):
        print("Connected with result code: " +str(rc))
        if(rc == 0):
            hostname,IPAddr  = self.Mqtt_Get_IPAddr()
            self.mqtt_client.subscribe(self.TopicSub)
            self.mqtt_client.publish(self.TopicPub, IPAddr)

    def Mqtt_message(self, client, userdata, message):

        print(message.topic + " " + str(message.payload))

    def Mqtt_publish(self):
        self.mqtt_client.publish(self.TopicPub, "xin chao")


    # ---------------------------------------------------(END)-----------------------------------------------------------------------------#

    # -----------------------------------------(Giao Diện HOME)-----------------------------------------------------------------------------#
    def Show_Screen_Home(self):
        Count_next_image = 1
        self.uic.stackedWidget.setCurrentWidget(self.uic.HOME)
    def Show_Screen_Learn(self):
        self.Learn_Get_Number_File()
        self.Learn_Show_Imgae_Learn()
        self.uic.stackedWidget.setCurrentWidget(self.uic.Screen_Learn)

    def Show_Screen_Test(self, stt):
        self.Sys_value_ChooseScreenTest = stt
        self.ScreenTest_value_Qlabel_ArrayNumberChoose = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.screen_Test_Display_ClearChoose()
        self.uic.stackedWidget.setCurrentWidget(self.uic.screen_Test)
        self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_InputInfor)

        if(self.Sys_value_ChooseScreenTest == 1):
            self.uic.screen_Test_Display_InputInfor_Button_Exit.setEnabled(True)
            self.uic.screen_test_Qlineedit_IDclass_3.setPlaceholderText("Mã lớp học")
            self.uic.screen_test_Qlineedit_IDclass_3.setEnabled(1)
            self.uic.screen_test_Qlineedit_IDclass_3.clear()
        else:
            print("vao")
            self.uic.screen_Test_Display_InputInfor_Button_Exit.setEnabled(False)
            self.uic.screen_test_Qlineedit_IDclass_3.setPlaceholderText("")
            self.uic.screen_test_Qlineedit_IDclass_3.setEnabled(0)
            self.uic.screen_test_Qlineedit_IDclass_3.clear()



    def Show_Screen_Setting(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.screen_Setting)
        self.uic.stackedWidget_3.setCurrentWidget(self.uic.screen_Setting_Home)
        self.screen_Setting_Clear_CreateExercise(4)

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
        self.ScreenTest_value_NameStudent = self.uic.screen_test_Qlineedit_Username_3.text()
        self.ScreenTest_value_NameITStudent = self.uic.screen_test_Qlineedit_IDStudent_3.text()
        self.ScreenTest_value_NameClassStudent = self.uic.screen_test_Qlineedit_IDclass_3.text()

        if(self.Sys_value_ChooseScreenTest == 1):
            self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_Exam)
            self.Mqtt_Run(self.ScreenTest_value_NameClassStudent)
        else:
            self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_Exam)




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

        if(self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] >= 6):
            self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] = self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] + float(self.uic.screen_Test_Display_Choose_lineEdit.text())
            print( self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button])
        self.screen_Test_Display_Choose_radio_SelectChoose(Number_Button)

    def screen_Test_Display_Choose_radio_SelectChoose(self, Number_Button):
        if(Number_Button == 1):
            if(self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_1.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_1.setText(self.uic.screen_Test_Display_Choose_lineEdit.text()+' V')
        if (Number_Button == 2):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_2.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_2.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 3):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_3.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_3.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 4):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_4.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_4.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 5):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_5.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_5.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 6):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_6.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_6.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 7):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_7.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_7.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 8):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_8.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_8.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 9):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_9.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_9.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 10):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_10.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_10.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 11):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_11.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_11.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 12):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_12.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_12.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 13):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_13.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_13.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 14):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_14.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_14.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 15):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_15.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_15.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 16):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_16.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[ self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_16.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 17):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_17.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_17.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 18):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_18.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_18.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 19):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_19.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_19.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 20):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_20.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_20.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 21):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_21.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_21.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 22):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_22.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_22.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 23):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_23.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_23.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')
        if (Number_Button == 24):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < 6):
                self.uic.SCreen_Test_Qlabel_PAN_24.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
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

        if(self.Sys_value_ChooseScreenTest == 1):
            self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_Answer)

            for x in range(1,25):
                if(self.ScreenTest_value_Qlabel_ArrayNumberChoose[x] >= 6):
                    print(str(format(float(self.ScreenTest_value_Qlabel_ArrayNumberChoose[x] - 6), '.1f'))+' V')
                else:
                    print(self.ScreenTest_value_Qlabel_ArrayNumberChoose[x])
        else:
            self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_Answer)
            print("da noi bai")
    def screen_Test_Display_ClearChoose(self):
        for x in range(1, 25):
            self.screen_Test_Display_Choose_radio_SelectChoose(x)

#-----------------------------------------(END)-----------------------------------------------------------------------------#

#-----------------------------------------(Giao Diện Setting)-----------------------------------------------------------------------------#

    def screen_Setting_Show_Display_Practice(self):
        #self.uic.stackedWidget_3.setCurrentWidget(self.uic.screen_Setting_practice)
        self.screen_Setting_Get_Select_CreateExercise()

    def screen_Setting_RamdomExercise(self):
        #self.screen_Setting_ArrRandomCreateExercise()
        items = ['Hở mạch', 'Chập chờn', 'Chạm đất', 'Nối dương', 'Bình thường', 'Điện áp']
        ArrRandom_setCurrentText,ArrRandom_voltage = self.screen_Setting_ArrRandomCreateExercise()

        self.uic.screen_setting_Home_ComboBox_1.setCurrentText(items[ArrRandom_setCurrentText[1]])
        if(ArrRandom_setCurrentText[1] >= 5):
            self.uic.screen_setting_Home_lineEdit_1.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_1.setText(str(format(ArrRandom_voltage[1], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_1.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_1.clear()

        self.uic.screen_setting_Home_ComboBox_2.setCurrentText(items[ArrRandom_setCurrentText[2]])
        if (ArrRandom_setCurrentText[2] >= 5):
            self.uic.screen_setting_Home_lineEdit_2.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_2.setText(str(format(ArrRandom_voltage[2], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_2.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_2.clear()

        self.uic.screen_setting_Home_ComboBox_3.setCurrentText(items[ArrRandom_setCurrentText[3]])
        if (ArrRandom_setCurrentText[3] >= 5):
            self.uic.screen_setting_Home_lineEdit_3.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_3.setText(str(format(ArrRandom_voltage[3], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_3.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_3.clear()

        self.uic.screen_setting_Home_ComboBox_4.setCurrentText(items[ArrRandom_setCurrentText[4]])
        if (ArrRandom_setCurrentText[4] >= 5):
            self.uic.screen_setting_Home_lineEdit_4.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_4.setText(str(format(ArrRandom_voltage[4], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_4.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_4.clear()

        self.uic.screen_setting_Home_ComboBox_5.setCurrentText(items[ArrRandom_setCurrentText[5]])
        if (ArrRandom_setCurrentText[5] >= 5):
            self.uic.screen_setting_Home_lineEdit_5.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_5.setText(str(format(ArrRandom_voltage[5], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_5.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_5.clear()

        self.uic.screen_setting_Home_ComboBox_6.setCurrentText(items[ArrRandom_setCurrentText[6]])
        if (ArrRandom_setCurrentText[6] >= 5):
            self.uic.screen_setting_Home_lineEdit_6.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_6.setText(str(format(ArrRandom_voltage[6], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_6.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_6.clear()

        self.uic.screen_setting_Home_ComboBox_7.setCurrentText(items[ArrRandom_setCurrentText[7]])
        if (ArrRandom_setCurrentText[7] >= 5):
            self.uic.screen_setting_Home_lineEdit_7.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_7.setText(str(format(ArrRandom_voltage[7], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_7.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_7.clear()

        self.uic.screen_setting_Home_ComboBox_8.setCurrentText(items[ArrRandom_setCurrentText[8]])
        if (ArrRandom_setCurrentText[8] >= 5):
            self.uic.screen_setting_Home_lineEdit_8.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_8.setText(str(format(ArrRandom_voltage[8], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_8.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_8.clear()

        self.uic.screen_setting_Home_ComboBox_9.setCurrentText(items[ArrRandom_setCurrentText[9]])
        if (ArrRandom_setCurrentText[9] >= 5):
            self.uic.screen_setting_Home_lineEdit_9.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_9.setText(str(format(ArrRandom_voltage[9], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_9.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_9.clear()

        self.uic.screen_setting_Home_ComboBox_10.setCurrentText(items[ArrRandom_setCurrentText[10]])
        if (ArrRandom_setCurrentText[10] >= 5):
            self.uic.screen_setting_Home_lineEdit_10.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_10.setText(str(format(ArrRandom_voltage[10], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_10.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_10.clear()

        self.uic.screen_setting_Home_ComboBox_11.setCurrentText(items[ArrRandom_setCurrentText[11]])
        if (ArrRandom_setCurrentText[11] >= 5):
            self.uic.screen_setting_Home_lineEdit_11.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_11.setText(str(format(ArrRandom_voltage[11], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_11.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_11.clear()

        self.uic.screen_setting_Home_ComboBox_12.setCurrentText(items[ArrRandom_setCurrentText[12]])
        if (ArrRandom_setCurrentText[12] >= 5):
            self.uic.screen_setting_Home_lineEdit_12.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_12.setText(str(format(ArrRandom_voltage[12], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_12.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_12.clear()

        self.uic.screen_setting_Home_ComboBox_13.setCurrentText(items[ArrRandom_setCurrentText[13]])
        if (ArrRandom_setCurrentText[13] >= 5):
            self.uic.screen_setting_Home_lineEdit_13.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_13.setText(str(format(ArrRandom_voltage[13], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_13.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_13.clear()

        self.uic.screen_setting_Home_ComboBox_14.setCurrentText(items[ArrRandom_setCurrentText[14]])
        if (ArrRandom_setCurrentText[14] >= 5):
            self.uic.screen_setting_Home_lineEdit_14.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_14.setText(str(format(ArrRandom_voltage[14], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_14.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_14.clear()

        self.uic.screen_setting_Home_ComboBox_15.setCurrentText(items[ArrRandom_setCurrentText[15]])
        if (ArrRandom_setCurrentText[15] >= 5):
            self.uic.screen_setting_Home_lineEdit_15.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_15.setText(str(format(ArrRandom_voltage[15], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_15.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_15.clear()

        self.uic.screen_setting_Home_ComboBox_16.setCurrentText(items[ArrRandom_setCurrentText[16]])
        if (ArrRandom_setCurrentText[16] >= 5):
            self.uic.screen_setting_Home_lineEdit_16.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_16.setText(str(format(ArrRandom_voltage[16], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_16.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_16.clear()

        self.uic.screen_setting_Home_ComboBox_17.setCurrentText(items[ArrRandom_setCurrentText[17]])
        if (ArrRandom_setCurrentText[17] >= 5):
            self.uic.screen_setting_Home_lineEdit_17.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_17.setText(str(format(ArrRandom_voltage[17], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_17.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_17.clear()

        self.uic.screen_setting_Home_ComboBox_18.setCurrentText(items[ArrRandom_setCurrentText[18]])
        if (ArrRandom_setCurrentText[18] >= 5):
            self.uic.screen_setting_Home_lineEdit_18.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_18.setText(str(format(ArrRandom_voltage[18], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_18.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_18.clear()

        self.uic.screen_setting_Home_ComboBox_19.setCurrentText(items[ArrRandom_setCurrentText[19]])
        if (ArrRandom_setCurrentText[19] >= 5):
            self.uic.screen_setting_Home_lineEdit_19.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_19.setText(str(format(ArrRandom_voltage[19], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_19.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_19.clear()

        self.uic.screen_setting_Home_ComboBox_20.setCurrentText(items[ArrRandom_setCurrentText[20]])
        if (ArrRandom_setCurrentText[20] >= 5):
            self.uic.screen_setting_Home_lineEdit_20.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_20.setText(str(format(ArrRandom_voltage[20], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_20.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_20.clear()

        self.uic.screen_setting_Home_ComboBox_21.setCurrentText(items[ArrRandom_setCurrentText[21]])
        if (ArrRandom_setCurrentText[21] >= 5):
            self.uic.screen_setting_Home_lineEdit_21.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_21.setText(str(format(ArrRandom_voltage[21], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_21.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_21.clear()

        self.uic.screen_setting_Home_ComboBox_22.setCurrentText(items[ArrRandom_setCurrentText[22]])
        if (ArrRandom_setCurrentText[22] >= 5):
            self.uic.screen_setting_Home_lineEdit_22.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_22.setText(str(format(ArrRandom_voltage[22], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_22.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_22.clear()

        self.uic.screen_setting_Home_ComboBox_23.setCurrentText(items[ArrRandom_setCurrentText[23]])
        if (ArrRandom_setCurrentText[23] >= 5):
            self.uic.screen_setting_Home_lineEdit_23.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_23.setText(str(format(ArrRandom_voltage[23], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_23.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_23.clear()

        self.uic.screen_setting_Home_ComboBox_24.setCurrentText(items[ArrRandom_setCurrentText[24]])
        if (ArrRandom_setCurrentText[24] >= 5):
            self.uic.screen_setting_Home_lineEdit_24.setEnabled(1)
            self.uic.screen_setting_Home_lineEdit_24.setText(str(format(ArrRandom_voltage[24], '.1f')))
        else:
            self.uic.screen_setting_Home_lineEdit_24.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_24.clear()



    def screen_Setting_ArrRandomCreateExercise(self):
        ArrRandom_setCurrentText = random.randint(6, size=(25))
        ArrRandom_voltage = random.uniform(0.0, 12.0, 25)
        return ArrRandom_setCurrentText, ArrRandom_voltage

    def screen_Setting_Get_Select_CreateExercise(self):
        value = 6

        if(self.uic.screen_setting_Home_ComboBox_1.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[1] = float(self.uic.screen_setting_Home_lineEdit_1.text()) + value
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[1] = self.uic.screen_setting_Home_ComboBox_1.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[1] = self.uic.screen_setting_Home_ComboBox_1.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_2.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[2] = float(
                self.uic.screen_setting_Home_lineEdit_2.text()) + value
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[2] = self.uic.screen_setting_Home_ComboBox_2.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[2] = self.uic.screen_setting_Home_ComboBox_2.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[] = float(
                self.uic.screen_setting_Home_lineEdit_.text()) + value
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[] = self.uic.screen_setting_Home_ComboBox_.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[] = self.uic.screen_setting_Home_ComboBox_.currentIndex()

        print(self.ScreenSetting_value_ArrayGetCurrentText)
        print( self.ScreenSetting_value_ArrayGetCurrentIndex)
        #print(self.uic.screen_setting_Home_ComboBox_1.currentIndex(),self.uic.screen_setting_Home_ComboBox_1.currentText())


    def screen_Setting_Check_selectVoltage_1(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_1.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_1.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_1.clear()

    def screen_Setting_Check_selectVoltage_2(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_2.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_2.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_2.clear()

    def screen_Setting_Check_selectVoltage_3(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_3.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_3.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_3.clear()

    def screen_Setting_Check_selectVoltage_4(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_4.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_4.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_4.clear()

    def screen_Setting_Check_selectVoltage_5(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_5.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_5.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_5.clear()

    def screen_Setting_Check_selectVoltage_6(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_6.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_6.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_6.clear()

    def screen_Setting_Check_selectVoltage_7(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_7.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_7.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_7.clear()

    def screen_Setting_Check_selectVoltage_8(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_8.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_8.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_8.clear()

    def screen_Setting_Check_selectVoltage_9(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_9.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_9.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_9.clear()

    def screen_Setting_Check_selectVoltage_10(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_10.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_10.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_10.clear()

    def screen_Setting_Check_selectVoltage_11(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_11.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_11.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_11.clear()

    def screen_Setting_Check_selectVoltage_12(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_12.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_12.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_12.clear()

    def screen_Setting_Check_selectVoltage_13(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_13.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_13.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_13.clear()

    def screen_Setting_Check_selectVoltage_14(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_14.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_14.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_14.clear()

    def screen_Setting_Check_selectVoltage_15(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_15.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_15.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_15.clear()

    def screen_Setting_Check_selectVoltage_16(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_16.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_16.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_16.clear()

    def screen_Setting_Check_selectVoltage_17(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_17.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_17.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_17.clear()

    def screen_Setting_Check_selectVoltage_18(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_18.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_18.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_18.clear()

    def screen_Setting_Check_selectVoltage_19(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_19.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_19.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_19.clear()

    def screen_Setting_Check_selectVoltage_20(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_20.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_20.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_20.clear()

    def screen_Setting_Check_selectVoltage_21(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_21.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_21.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_21.clear()

    def screen_Setting_Check_selectVoltage_22(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_22.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_22.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_22.clear()

    def screen_Setting_Check_selectVoltage_23(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_23.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_23.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_23.clear()

    def screen_Setting_Check_selectVoltage_24(self, i):
        if i >= 5:
            self.uic.screen_setting_Home_lineEdit_24.setEnabled(1)
        else:
            self.uic.screen_setting_Home_lineEdit_24.setEnabled(0)
            self.uic.screen_setting_Home_lineEdit_24.clear()

    def screen_Setting_Clear_CreateExercise(self, i):
        items = ['Hở mạch', 'Chập chờn', 'Chạm đất', 'Nối dương', 'Bình thường', 'Điện áp']
        self.uic.screen_setting_Home_ComboBox_1.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_1.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_2.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_2.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_3.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_3.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_4.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_4.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_5.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_5.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_6.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_6.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_7.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_7.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_8.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_8.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_9.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_9.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_10.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_10.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_11.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_11.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_12.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_12.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_13.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_13.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_14.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_14.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_15.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_15.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_16.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_16.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_17.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_17.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_18.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_18.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_19.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_19.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_20.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_20.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_21.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_21.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_22.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_22.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_23.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_23.setEnabled(0)

        self.uic.screen_setting_Home_ComboBox_24.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_24.setEnabled(0)







#-----------------------------------------(END)-----------------------------------------------------------------------------#
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win =  MainWindow()
    main_win.show()
    sys.exit(app.exec())

