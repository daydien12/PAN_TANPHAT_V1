import sys
import os
import glob
import json
import socket

from pdf2image import convert_from_path
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings, QPoint
from MQTT_TEST import Ui_MainWindow
from PyQt5.QtCore import QTime, QTimer
import paho.mqtt.client as mqtt
from numpy import random
import shutil
import pyautogui
import time

class MainWindow:
    def __init__(self, parent=None):
        super().__init__()
        # -----------(Khởi tao Class)-----------------#
        self.timer = QTimer()
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.uic.stackedWidget.setCurrentWidget(self.uic.HOME)
        self.mqtt_client = mqtt.Client()
        self.Sys_value_ChooseScreenTest = 0
        self.Sys_valute_TimeCountClearRemind = 0
        self.Sys_valute_FlagClearRemind_Learn = 0
        self.Sys_valute_FlagClearRemind_ChooseTest = 0
        # -----------(Lưu thông tin)-----------------#
        self.QSettingsSave_StrJsonAnswer = 'Json_Answer_Mqtt'
        self.QSettingsSave_StrPassword = 'Str_Password'
        self.QSettingsSave_StrIDDivice = 'Str_IDDivice'
        self.settings = QSettings('PAN','PAN')

        #self.settings.setValue(self.QSettingsSave_StrPassword, "1")
        print(self.settings.value(self.QSettingsSave_StrPassword))
        #settings.setValue('list_value', "25")
        #settings.setValue('dict_value', {'one': 1, 'two': 2})

        #print()
        #-----------(Biến đếm chuyển ảnh và biến lưu số lượng ảnh có trong file giao diện learn)-----------------#
        self.Count_next_image = 1
        self.Number_Image_Learn = 1
        # -----------(Biến MQTT)-----------------#
        self.Mqtt_Port = 1883

        self.TopicSub_PingMQTT = "check"
        self.TopicSub_GetTest = "send/id1"

        self.TopicPub_CkeckConnect = "res_check"
        self.TopicPub_SendAnswer = "res_answer"
        # -----------(Biến tên và đường dẫn giao diện learn)-----------------#
        self.Path_Image_Screen_Learn = 'Image_Learn'
        self.Name_image_Screen_Learn = 'output'
        self.Name_File_PDF = 'sample.pdf'
        self.Learn_Size_X_Image_PDF = 1024
        self.Learn_Size_Y_Image_PDF = 600

        # -----------(Biến tên giao diện Test)-----------------#
        self.ScreenTest_value_Qlabel_ArrayNameChoose = ["Chưa chọn","Hở mạch", "Chập chờn", "Chạm đất","Nối dương", "Bình thường"]
        self.ScreenTest_value_Qlabel_ArrayNumberChoose = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.ScreenTest_value_Qlabel_ArrayGetNumberChoose = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.ScreenTest_value_Qlabel_ArrayAnswerMqtt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.ScreenTest_value_ArrayInforAnswer = ["Chưa có", "Chưa có", "Chưa có", "Chưa có", "Chưa có"]
        self.ScreenTest_value_ArrayShowText = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        self.ScreenTest_value_Qlabel_FlagButtonClick = 0
        self.ScreenTest_value_NameStudent = ""
        self.ScreenTest_value_NameITStudent = ""
        self.ScreenTest_value_NameClassStudent = ""
        self.ScreenTest_value_TimeOut_M = 0
        self.ScreenTest_value_TimeOut_S = 0
        self.ScreenTest_value_Time_first = 0

        self.FlagStartTimeOut = 0
        self.FlagStopTimeOut = 0
        self.uic.screen_Test_Display_Choose_lineEdit.setEnabled(0)

        # -----------(Biến tên giao diện setting)-----------------#
        self.ScreenSetting_value_ArrayGetCurrentText = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        self.ScreenSetting_value_ArrayGetCurrentIndex = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]


        # Khối button của màn hình Home
        self.uic.Home_Button_Learn.clicked.connect(self.Show_Screen_Learn)
        self.uic.Home_Button_Test.clicked.connect(lambda:self.Show_Screen_Test(1))
        self.uic.Home_Button_Setting.clicked.connect(self.Show_Screen_Setting)
        self.uic.Home_Button_Information.clicked.connect(self.Show_Screen_Information)
        # Khối button của màn hình Learn
        self.uic.Learn_Button_Back.clicked.connect(self.Learn_Button_Back)
        self.uic.Learn_Button_Exit.clicked.connect(self.Show_Screen_Home)
        self.uic.Learn_Button_Next.clicked.connect(self.Learn_Button_Next)
        self.uic.Learn_Button_ChooseFile.clicked.connect(self.getfile)

        # self.Learn_convert_PDF_TO_IMAGE(self.Name_File_PDF)

        # Khối button của màn hình Test
        self.uic.screen_Test_Display_InputInfor_Button_Exit.clicked.connect(self.Show_Screen_Home) # nút quay lại(screen_Test)
        self.uic.screen_Test_Display_InputInfor_Button_Start.clicked.connect(self.screen_Test_Show_Display_Exam) # nút vào thi (screen_Test)

        #self.uic.screen_Test_Display_Exam_Exit.clicked.connect(lambda:self.Show_Screen_Test(self.Sys_value_ChooseScreenTest)) # nút quay lại(screen_Test_Display_Exam)
        self.uic.screen_Test_Display_Exam_Submit.clicked.connect(self.screen_Test_Display_Choose_ButtonSubmit) # nút Nộp bài (screen_Test_Display_Exam)

        #--------------------------------------------(Cụm nút PAN_01 -> PAN_24 (screen_Test_Display_Exam))---------------------------------------#
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

        self.uic.screen_Test_Display_Choose_ButtonChoose.clicked.connect(lambda:self.screen_Test_Display_Choose_radio_onClicked_and_Show_Display(self.ScreenTest_value_Qlabel_FlagButtonClick)) # nút Chọn (screen_Test_Display_Choose)
        self.uic.screen_Test_Display_Choose_radioButton_6.toggled.connect(lambda:self.screen_Test_Display_Choose_radio_onClicked(self.ScreenTest_value_Qlabel_FlagButtonClick)) #QRadioButton điện áp: đóng, Mở ô điền điện áp (screen_Test_Display_Choose)

        self.uic.screen_Test_Display_Answer_Exit.clicked.connect(self.screen_Test_SaveImageResult) # nút kết thúc (screen_Test_Display_Answer)

        # Khối button của màn hình Setting

        self.uic.screen_Setting_Home_ButtonCreatePractice.clicked.connect(self.screen_Setting_Show_Display_Practice) # Nút tạo bài thực hành (screen_Setting_Home)
        self.uic.screen_Setting_Home_ButtonCreateTest.clicked.connect(lambda:self.Show_Screen_Test(2)) # Nút tạo bài kiểm tra (screen_Setting_Home)
        self.uic.screen_Setting_Home_ButtonRamdom.clicked.connect(self.screen_Setting_RamdomExercise) # Nút tạo bài Ngẫu nhiên (screen_Setting_Home)
        self.uic.screen_Setting_Home_ButtonExit.clicked.connect(self.Show_Screen_Home) # Nút Quay lại (screen_Setting_Home)
        self.uic.screen_Setting_Home_ButtonLogin.clicked.connect(self.screen_Setting_Show_Login) # Cài đặt hệ thống: vào giao điện đặng nhập (screen_Setting_Home)

        # --------------------------------------------(Cụm ComboBox PAN_01 -> PAN_24 (screen_Setting_Home))---------------------------------------#
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

        self.uic.screen_Setting_practice_ButtonExit.clicked.connect(self.Show_Screen_Home) # Nút Quay lại (screen_Setting_practice)

        self.uic.screen_Setting_SettingSys_Button_LoginSYS.clicked.connect(self.screen_Setting_Show_SettingSYS) # Nút Đăng nhập (screen_Setting_Login)
        self.uic.screen_Setting_SettingSys_Button_Exit.clicked.connect(self.Show_Screen_Home) # Nút Quay lại (screen_Setting_Login)

        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)

    def Sys_Clear_Remind(self):
        self.uic.screen_Test_Display_Exam_label_Remind.setStyleSheet(" background-color: transparent;")
        self.uic.screen_Test_Display_Exam_label_Remind.setText("")

        self.uic.Screen_Learn_label_Remind.setStyleSheet("background-color: transparent;")
        self.uic.Screen_Learn_label_Remind.setText("")

    def Time(self):
        if(self.Sys_valute_FlagClearRemind_ChooseTest == 1 or self.Sys_valute_FlagClearRemind_Learn == 1):
            self.Sys_valute_TimeCountClearRemind = self.Sys_valute_TimeCountClearRemind + 1
            if(self.Sys_valute_TimeCountClearRemind >= 5): #chỉnh thời gian hiện thông báo
                self.Sys_valute_TimeCountClearRemind = 0
                self.Sys_valute_FlagClearRemind_Learn = 0
                self.Sys_valute_FlagClearRemind_ChooseTest = 0
                self.Sys_Clear_Remind()

        if (self.FlagStartTimeOut == 1):
            if self.ScreenTest_value_TimeOut_S > 0:
                self.ScreenTest_value_TimeOut_S -= 1
            else:
                if self.ScreenTest_value_TimeOut_M > 0:
                    self.ScreenTest_value_TimeOut_M = self.ScreenTest_value_TimeOut_M - 1
                    self.ScreenTest_value_TimeOut_S = 59
            min_sec_format = '{:02d}:{:02d}'.format(self.ScreenTest_value_TimeOut_M, self.ScreenTest_value_TimeOut_S)
            self.uic.screen_Test_Display_lcdNumber_TimeOut.display(min_sec_format)


    def show(self):
        self.main_win.show()

    # -----------------------------------------(Cấu hình MQTT)-----------------------------------------------------------------------------#
    def Mqtt_Get_IPAddr(self): # hàm lấy địa chỉ IP và địa chỉ MAC của máy, return: địa chỉ mac, địa chỉ IP
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        return hostname, IPAddr;

    def Mqtt_Run(self, Mqtt_Host): # Hàm chạy của mqtt, truyền tham số Mqtt_Host: địa chỉ host mqtt, địa chỉ IP server mqtt
        try: # kiểm tra kết nối với server nếu không kết nối được tránh bị treo(cần xem lại)
            self.mqtt_client.on_connect = self.Mqtt_connect
            self.mqtt_client.on_message = self.Mqtt_message
            self.mqtt_client.connect('Mqtt.mysignage.vn', self.Mqtt_Port, 60)
            #self.mqtt_client.connect('192.168.110.129', self.Mqtt_Port, 60)
            Flag = 1
        except Exception as e:
            Flag = 0
            pass
        if(Flag == 1):
            self.mqtt_client.loop_start()

    def Mqtt_connect(self, client, userdata, flags, rc): # hàm cài đặt Sub topic
        print("Connected with result code: " +str(rc))
        if(rc == 0):
            hostname,IPAddr  = self.Mqtt_Get_IPAddr()
            self.mqtt_client.subscribe(self.TopicSub_PingMQTT)
            self.mqtt_client.subscribe(self.TopicSub_GetTest)

    def Mqtt_message(self, client, userdata, message):# hàm nhận bản tin từ máy giao viên
        if(message.topic == self.TopicSub_PingMQTT):
            print(message.topic + " " + str(message.payload))
            if(len(self.ScreenTest_value_NameStudent) > 0 and len(self.ScreenTest_value_NameITStudent) > 0): # Kiểm tra xem sinh viên đã điền thông tin chưa
                self.Mqtt_PingServer(self.ScreenTest_value_NameStudent, self.ScreenTest_value_NameITStudent)
        if (message.topic == self.TopicSub_GetTest):
            if (self.Sys_value_ChooseScreenTest == 1):  # kiểm tra xem thi online thì kết nối với server và hiển thị giao diện chọn câu trả lời
                self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_Exam)
                print(message.topic + " " + str(message.payload))

    def Mqtt_PingServer(self, Name, IDStudent): # hàm ping kết nối khi máy giao viên gửi yêu cầu, truyền tham số name, IDIDStuden: tên sinh viên và Mã sinh viên
        id_device = 1
        TempJson = { "id": id_device, "received":'false', "name":Name, "msv":IDStudent}
        self.mqtt_client.publish(self.TopicPub_CkeckConnect, json.dumps(TempJson))

    def Mqtt_SendAnswer(self, Time_end): #Hàm gửi câu trả lời khi nhấn nộp bài hoặc hết thời gian, Tham số Time: thời gian làm bài
        id_device = 1
        arrAnswe = self.ScreenTest_value_Qlabel_ArrayAnswerMqtt # Mảng của 24 câu trả lời
        arrJson = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for x in range(1, 25):
            if (arrAnswe[x] == 0):
                arrJson[x-1] = 250
            else:
                arrJson[x - 1] = self.ScreenTest_value_Qlabel_ArrayAnswerMqtt[x] - 1
        TempJson = {"id": id_device, "received": 'true', "answer": arrJson, "Time_end": Time_end}
        temp = json.dumps(TempJson)
        print(temp)
        self.mqtt_client.publish(self.TopicPub_SendAnswer, temp)


    # ---------------------------------------------------(END)-----------------------------------------------------------------------------#

    # -----------------------------------------(Giao Diện HOME)-----------------------------------------------------------------------------#
    def Show_Screen_Home(self): # Hàm hiên thị giao diện đầu tiên
        self.FlagStartTimeOut = 0  #đặt biến cờ Start về 0
        self.FlagStopTimeOut = 0 #đặt biến cờ Stop về 0
        self.ScreenTest_value_Time_first = 0
        self.ScreenTest_value_TimeOut_M = 0 #đặt biên đếm phút về 0
        self.ScreenTest_value_TimeOut_S = 0 #đặt biên đếm giây về 0
        self.Sys_value_ChooseScreenTest = 0 #Đặt biến chọn thi online hay offline về 0
        min_sec_format = '{:02d}:{:02d}'.format(self.ScreenTest_value_TimeOut_M, self.ScreenTest_value_TimeOut_S)
        self.uic.screen_Test_Display_Answer_label_TimeOut.setText(min_sec_format)
        self.uic.screen_Test_Display_lcdNumber_TimeOut.display(min_sec_format)
        self.uic.stackedWidget.setCurrentWidget(self.uic.HOME)

    def Show_Screen_Learn(self): #hàm hiển thị giao diện học
        self.Count_next_image = 1 # (khởi tạo học) lại bộ đếm, Bộ đếm này để next hoặc back ảnh
        self.Learn_Get_Number_File()
        self.Learn_Show_Imgae_Learn()
        self.uic.stackedWidget.setCurrentWidget(self.uic.Screen_Learn)

    def Show_Screen_Test(self, stt): #hàm hiển thị giao diện điền thông tin của sinh viên khi bắt đầu vào bài kiểm tra, Tham số stt: 1 hoặc 2, 1 là kiểm tra online, 2 là tự tạo bài kiểm tra
        self.Sys_value_ChooseScreenTest = stt # lấy giá trị 1 hoặc 2, 1=online, 2=offline
        self.uic.screen_test_Qlineedit_Username.clear()
        self.uic.screen_test_Qlineedit_IDStudent.clear()
        self.uic.screen_Test_Display_InputInfor_label_Remind.setText("")
        #--------------------------------------------( (Khởi tạo kiểm tra) ) ------------------------------------------#
        self.ScreenTest_value_Qlabel_ArrayNumberChoose = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.ScreenTest_value_Qlabel_ArrayGetNumberChoose = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.screen_Setting_Get_Select_CreateExercise()
        self.screen_Test_Display_ClearChoose()
        if (self.Sys_value_ChooseScreenTest == 1):  # Nếu là kiểm tra online thì cho nhập mã lớp học
            self.Mqtt_Run('Mqtt.mysignage.vn')  # kiểm tra xem thi online thì kết nối với server và hiển thị giao diện chọn câu trả lời
        self.uic.stackedWidget.setCurrentWidget(self.uic.screen_Test)
        self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_InputInfor)

    def Show_Screen_Setting(self): # hiển thị giao diện cài đặt
        self.screen_Setting_Clear_CreateExercise(4) # (Khởi tạo cài đặt)
        self.uic.stackedWidget.setCurrentWidget(self.uic.screen_Setting)
        self.uic.stackedWidget_3.setCurrentWidget(self.uic.screen_Setting_Home)

    def Show_Screen_Information(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.screen_Information)


#-----------------------------------------(Giao Diện học lý thuyết)-----------------------------------------------------------------------------#
    def Learn_Button_Next(self): # Hàm chuyển ảnh tiếp theo
        if (self.Count_next_image < self.Number_Image_Learn):
            self.Count_next_image = self.Count_next_image + 1
        else:
            self.Count_next_image = 1
        self.Learn_Show_Imgae_Learn()

    def Learn_Button_Back(self): # Hàm quay lại ảnh trước
        if (self.Count_next_image > 1):
            self.Count_next_image = self.Count_next_image - 1
        else:
            self.Count_next_image = self.Number_Image_Learn
        self.Learn_Show_Imgae_Learn()

    def Learn_Show_Imgae_Learn(self): # Hàm Hiển thị ảnh
        str_name = self.Path_Image_Screen_Learn + '/' + self.Name_image_Screen_Learn + str(self.Count_next_image) + '.jpg'
        self.uic.show_image_learn.setPixmap(QtGui.QPixmap(str_name))

    def Learn_Get_Number_File(self): # hàm đếm số lượng file ảnh có trong thử mục chưa
        files = [f for f in glob.glob(self.Path_Image_Screen_Learn + '/' + "**/*.jpg", recursive=True)]
        self.Number_Image_Learn = len(files)

    def getfile(self):
        self.uic.Screen_Learn_label_Remind.setStyleSheet("background-color: #ffab03;")
        self.uic.Screen_Learn_label_Remind.setText("Đang xử lý file ....")
        fname = QFileDialog.getOpenFileName()
        if (fname != ('', '')):
            if ((fname[0].rfind('.pdf')) != -1 or (fname[0].rfind('.PDF')) != -1):
                self.Sys_valute_FlagClearRemind_Learn = 1
                self.Learn_convert_PDF_TO_IMAGE(fname[0])
            else:
                self.uic.Screen_Learn_label_Remind.setStyleSheet("background-color: red;")
                self.uic.Screen_Learn_label_Remind.setText("File bạn chọn không phải .pdf")

    def Learn_convert_PDF_TO_IMAGE(self, name): #hàm chuyển pdf-> image, tham số Name: là đường dẫn và tên file pdf
        #path = os.path.abspath(outputDir)
        #if (os.path.exists(path) != False):
            #shutil.rmtree(path)

        outputDir = self.Path_Image_Screen_Learn + '/'
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        else:
            shutil.rmtree(outputDir)
            os.makedirs(outputDir)
        pages = convert_from_path(name, 500, size=(self.Learn_Size_X_Image_PDF, self.Learn_Size_Y_Image_PDF))
        counter = 1
        for page in pages:
            myfile = outputDir + self.Name_image_Screen_Learn + str(counter) + '.jpg'
            counter = counter + 1
            page.save(myfile, "JPEG")
        self.Learn_Get_Number_File()

        self.Count_next_image = 1
        self.Learn_Show_Imgae_Learn()
#-----------------------------------------(END)-----------------------------------------------------------------------------#

#-----------------------------------------(Giao Diện kiểm tra)-----------------------------------------------------------------------------#
    def screen_Test_Show_Display_Exam(self): #hàm này để hiển thị giao diện chọn đáp án
        if (self.Sys_value_ChooseScreenTest == 2):
            if(self.FlagStartTimeOut == 0):
                self.FlagStartTimeOut = 1
        #----------------------------(Cụm lấy thông tin của sinh viên)----------------------------
        #self.ScreenTest_value_NameClassStudent = self.uic.screen_test_Qlineedit_IDclass_3.text()

        if(len(self.uic.screen_test_Qlineedit_Username.text()) > 0): #kiểm tra xem thí sinh đã nhập tên chưa
            self.ScreenTest_value_ArrayInforAnswer[0] = self.uic.screen_test_Qlineedit_Username.text()
            self.ScreenTest_value_NameStudent = self.uic.screen_test_Qlineedit_Username.text()

        if (len(self.uic.screen_test_Qlineedit_IDStudent.text()) > 0): #kiểm tra xem thí sinh đã nhập mã sinh viên chưa
            self.ScreenTest_value_ArrayInforAnswer[1] = self.uic.screen_test_Qlineedit_IDStudent.text()
            self.ScreenTest_value_NameITStudent = self.uic.screen_test_Qlineedit_IDStudent.text()

        if(len(self.uic.screen_test_Qlineedit_Username.text()) > 0 and len(self.uic.screen_test_Qlineedit_IDStudent.text()) > 0):
            self.uic.screen_Test_Display_InputInfor_label_Remind.setStyleSheet(" background-color: transparent;")
            self.uic.screen_Test_Display_InputInfor_label_Remind.setText("")
            if(self.Sys_value_ChooseScreenTest == 1):
                self.screen_Test_connectWait()
            elif(self.Sys_value_ChooseScreenTest == 2): #kiểm tra xem thi online thì kết nối với server và hiển thị giao diện chọn câu trả lời
                self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_Exam)

        else:
            self.uic.screen_Test_Display_InputInfor_label_Remind.setStyleSheet("background-color: red;")
            self.uic.screen_Test_Display_InputInfor_label_Remind.setText("Chưa điền thông tin")


    def screen_Test_connectWait(self):
        self.movie = QMovie("Icon/loading-animation_sand-timer.gif")
        self.uic.label_7.setMovie(self.movie)
        self.movie.start()
        self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Connect)

    def screen_Test_Show_Display_Choose(self, Number): # Hiển hị giao diện chọn câu trả lời, hiển thị chọn câu trả lời cho Pan nào, Tham số Number: truyền PAN số mấy đang chọn
        self.uic.screen_Test_Display_Choose_Qlabel_PAN_Number.setText("PAN "+str(Number))
        self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_Choose)
    #--------------------------(Cụm hàm sự kiện khi nhấn nút của PAN_01 -> PAN_24)--------------------------
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

    def Screen_Test_CheckInputString(self, StrNumber): #kiểm tra xem chuỗi đầu vào có phải là số int hay float hay không, Tham số StrNumber: truyền chuỗi số vào vd:"3.5"
        flag = 0
        try:
            int(StrNumber)
            flag = 1
        except ValueError:
            flag = 0

        try:
            float(StrNumber)
            flag = 1
        except ValueError:
            flag = 0

        return flag

    def screen_Test_Display_Choose_radio_onClicked_and_Show_Display(self, Number_Button):
        Flag = 0
        self.screen_Test_Display_Choose_radio_onClicked(Number_Button) # lấy đáp án từ 1->6  đã chọn của PAN đó
        if(self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] >= 6): # kiểm tra Nếu lớn hơn 6 là chọn điện áp
            if((self.Screen_Test_CheckInputString(self.uic.screen_Test_Display_Choose_lineEdit.text()) == 1) and (len(self.uic.screen_Test_Display_Choose_lineEdit.text()) > 0)): # kiểm tra xem đã nhập đúng là số hay chưa , kiểm tra xem có điền giá trị điển áp không
                Flag = 1
                self.ScreenTest_value_Qlabel_ArrayGetNumberChoose[Number_Button] = self.uic.screen_Test_Display_Choose_lineEdit.text() #mảng lấy giá trị điện áp học sinh điền
                self.ScreenTest_value_Qlabel_ArrayAnswerMqtt[Number_Button] = int((float(self.uic.screen_Test_Display_Choose_lineEdit.text()) * 10) + 4) # mảng kết quả đê gửi cho máy giáo viên
            else: # nếu chưa điền hoặc điền sai thì sẽ xóa chuỗi đã điền
                self.uic.screen_Test_Display_Choose_lineEdit.clear()
        else:
            Flag = 1
            self.ScreenTest_value_Qlabel_ArrayAnswerMqtt[Number_Button] = self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]
        if(Flag == 1): #nếu thoải mã hết các điểu kiện thì chuyển về giao diện chọn
            self.screen_Test_Show_Display_Exam()  # quay lại giao diện chọn PAN
            self.screen_Test_Display_Choose_radio_SelectChoose(Number_Button)
        print(self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button])

    def screen_Test_Display_Choose_radio_SelectChoose(self, Number_Button): # hiển thị đáp án đã chọn ở bên dưới button PAN
        value = 6
        if (Number_Button == 1):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_1.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_1.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 2):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_2.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_2.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 3):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_3.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_3.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 4):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_4.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_4.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 5):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_5.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_5.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == value):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_6.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_6.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 7):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_7.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[ self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_7.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 8):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_8.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_8.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 9):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_9.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_9.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 10):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_10.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_10.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 11):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_11.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[ self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_11.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 12):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_12.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_12.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 13):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_13.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_13.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 14):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_14.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_14.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 15):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_15.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_15.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 16):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_16.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_16.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 17):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_17.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[ self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_17.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 18):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_18.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_18.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 19):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_19.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_19.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 20):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_20.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_20.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 21):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_21.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_21.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 22):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_22.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_22.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 23):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_23.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_23.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

        if (Number_Button == 24):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button] < value):
                self.uic.SCreen_Test_Qlabel_PAN_24.setText(self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[Number_Button]])
            else:
                self.uic.SCreen_Test_Qlabel_PAN_24.setText(self.uic.screen_Test_Display_Choose_lineEdit.text() + ' V')

    def screen_Test_Display_Choose_radio_onClicked(self, Number_Button): # Hàm gán giá trị đã chọn (từ 1-6) vào mảng

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

    def screen_Test_Display_Choose_ButtonSubmit(self): # hàm Nộp bài và chấm điểm
        Flag = 0
        for x in range(1, 25):
            if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[x] == 0):
                Flag = 1
        if(Flag == 0):
            if(self.Sys_value_ChooseScreenTest == 1): #nếu là thi online thì gửi bài lên máy tính giáo viên
                self.Mqtt_SendAnswer(20)
                self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_Answer)
            elif (self.Sys_value_ChooseScreenTest == 2): #nếu là thi offline hiển thị giao diện kết quả
                #print(self.ScreenSetting_value_ArrayGetCurrentText)
                #print(self.ScreenSetting_value_ArrayGetCurrentIndex)
                #print(self.ScreenTest_value_Qlabel_ArrayNumberChoose)
                self.screen_Test_ShowText_QlabelAnswer1(self.Sys_value_ChooseScreenTest)
                self.screen_Test_ShowText_QlabelAnswer2(self.Sys_value_ChooseScreenTest)
                self.screen_Test_ShowText_QlabelAnswer3(self.Sys_value_ChooseScreenTest)
                self.screen_Test_Answer_Infor()
                self.uic.stackedWidget_2.setCurrentWidget(self.uic.screen_Test_Display_Answer)
        else:
            self.Sys_valute_FlagClearRemind_ChooseTest = 1
            self.uic.screen_Test_Display_Exam_label_Remind.setStyleSheet("background-color: red;")
            self.uic.screen_Test_Display_Exam_label_Remind.setText("Chưa chọn hết đáp án")

    def screen_Test_Display_ClearChoose(self): # hàm xóa giao diện chọn PAN về chưa chọn
        for x in range(1, 25):
            self.screen_Test_Display_Choose_radio_SelectChoose(x)

    def screen_Test_Answer_Infor(self): # hàm hiển thị câu trả lời
        self.uic.screen_Test_Display_Answer_label_Name.setText(self.ScreenTest_value_ArrayInforAnswer[0])
        self.uic.screen_Test_Display_Answer_label_ID.setText(self.ScreenTest_value_ArrayInforAnswer[1])
        self.uic.screen_Test_Display_Answer_label_AnswerTrue.setText(str(self.ScreenTest_value_ArrayInforAnswer[2]))
        self.uic.screen_Test_Display_Answer_label_AnswerFalse.setText(str(self.ScreenTest_value_ArrayInforAnswer[3]))
        self.uic.screen_Test_Display_Answer_label_AnswerNot.setText(str(self.ScreenTest_value_ArrayInforAnswer[4]))
        self.FlagStartTimeOut == 0

        min_sec_format = '{:02d}:{:02d}'.format((self.ScreenTest_value_Time_first - self.ScreenTest_value_TimeOut_M), (59 - self.ScreenTest_value_TimeOut_S))
        self.uic.screen_Test_Display_Answer_label_TimeOut.setText(min_sec_format)
    def screen_Test_ShowText_QlabelAnswer1(self, stt): # hàm hiển thị đề bài, tham số stt: truyền vào là làm bài online hay offline
        if(stt == 1):
            print("11")
        else:
            for x in range(1, 25):
                if(self.ScreenSetting_value_ArrayGetCurrentIndex[x] >= 5):
                    self.ScreenTest_value_ArrayShowText[x][0] = str(self.ScreenSetting_value_ArrayGetCurrentText[x]) + ' V'
                else:
                    self.ScreenTest_value_ArrayShowText[x][0] = self.ScreenSetting_value_ArrayGetCurrentText[x]

        self.uic.screen_test_Display_Answer_Qlabel_Answer0_1.setText(self.ScreenTest_value_ArrayShowText[1][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_2.setText(self.ScreenTest_value_ArrayShowText[2][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_3.setText(self.ScreenTest_value_ArrayShowText[3][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_4.setText(self.ScreenTest_value_ArrayShowText[4][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_5.setText(self.ScreenTest_value_ArrayShowText[5][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_6.setText(self.ScreenTest_value_ArrayShowText[6][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_7.setText(self.ScreenTest_value_ArrayShowText[7][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_8.setText(self.ScreenTest_value_ArrayShowText[8][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_9.setText(self.ScreenTest_value_ArrayShowText[9][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_10.setText(self.ScreenTest_value_ArrayShowText[10][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_11.setText(self.ScreenTest_value_ArrayShowText[11][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_12.setText(self.ScreenTest_value_ArrayShowText[12][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_13.setText(self.ScreenTest_value_ArrayShowText[13][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_14.setText(self.ScreenTest_value_ArrayShowText[14][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_15.setText(self.ScreenTest_value_ArrayShowText[15][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_16.setText(self.ScreenTest_value_ArrayShowText[16][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_17.setText(self.ScreenTest_value_ArrayShowText[17][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_18.setText(self.ScreenTest_value_ArrayShowText[18][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_19.setText(self.ScreenTest_value_ArrayShowText[19][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_20.setText(self.ScreenTest_value_ArrayShowText[20][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_21.setText(self.ScreenTest_value_ArrayShowText[21][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_22.setText(self.ScreenTest_value_ArrayShowText[22][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_23.setText(self.ScreenTest_value_ArrayShowText[23][0])
        self.uic.screen_test_Display_Answer_Qlabel_Answer0_24.setText(self.ScreenTest_value_ArrayShowText[24][0])

    def screen_Test_ShowText_QlabelAnswer2(self, stt): #hàm hiển thị bài làm đã chọn của Học sinh, tham số stt: truyền vào là làm bài online hay offline
        if (stt == 1):
            print("11")
        else:
            for x in range(1, 25):
                if (self.ScreenTest_value_Qlabel_ArrayNumberChoose[x] >= 6):
                    self.ScreenTest_value_ArrayShowText[x][1] = self.ScreenTest_value_Qlabel_ArrayGetNumberChoose[x] + ' V'
                else:
                    self.ScreenTest_value_ArrayShowText[x][1] = self.ScreenTest_value_Qlabel_ArrayNameChoose[self.ScreenTest_value_Qlabel_ArrayNumberChoose[x]]
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_1.setText(self.ScreenTest_value_ArrayShowText[1][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_2.setText(self.ScreenTest_value_ArrayShowText[2][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_3.setText(self.ScreenTest_value_ArrayShowText[3][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_4.setText(self.ScreenTest_value_ArrayShowText[4][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_5.setText(self.ScreenTest_value_ArrayShowText[5][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_6.setText(self.ScreenTest_value_ArrayShowText[6][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_7.setText(self.ScreenTest_value_ArrayShowText[7][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_8.setText(self.ScreenTest_value_ArrayShowText[8][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_9.setText(self.ScreenTest_value_ArrayShowText[9][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_10.setText(self.ScreenTest_value_ArrayShowText[10][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_11.setText(self.ScreenTest_value_ArrayShowText[11][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_12.setText(self.ScreenTest_value_ArrayShowText[12][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_13.setText(self.ScreenTest_value_ArrayShowText[13][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_14.setText(self.ScreenTest_value_ArrayShowText[14][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_15.setText(self.ScreenTest_value_ArrayShowText[15][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_16.setText(self.ScreenTest_value_ArrayShowText[16][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_17.setText(self.ScreenTest_value_ArrayShowText[17][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_18.setText(self.ScreenTest_value_ArrayShowText[18][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_19.setText(self.ScreenTest_value_ArrayShowText[19][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_20.setText(self.ScreenTest_value_ArrayShowText[20][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_21.setText(self.ScreenTest_value_ArrayShowText[21][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_22.setText(self.ScreenTest_value_ArrayShowText[22][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_23.setText(self.ScreenTest_value_ArrayShowText[23][1])
        self.uic.screen_test_Display_Answer_Qlabel_Answer1_24.setText(self.ScreenTest_value_ArrayShowText[24][1])

    def screen_Test_ShowText_QlabelAnswer3(self, stt): # hàm hiển thị PAN đó chọn đúng hay sai, tham số stt: truyền vào là làm bài online hay offline
        Count_True = 0
        Count_False = 0
        Count_NotChoose = 0
        if (stt == 1):
            print("11")
        else:
            for x in range(1, 25):
                if(self.ScreenTest_value_Qlabel_ArrayNumberChoose[x] != 0):
                    if (self.ScreenSetting_value_ArrayGetCurrentIndex[x] >= 5):
                        if (str(self.ScreenSetting_value_ArrayGetCurrentText[x]) == self.ScreenTest_value_Qlabel_ArrayGetNumberChoose[x]):
                            self.ScreenTest_value_ArrayShowText[x][2] = "Đúng"
                            Count_True = Count_True + 1
                        else:
                            self.ScreenTest_value_ArrayShowText[x][2] = "sai"
                            Count_False = Count_False + 1
                    else:
                        if (self.ScreenSetting_value_ArrayGetCurrentIndex[x] == (self.ScreenTest_value_Qlabel_ArrayNumberChoose[x] - 1)):
                            self.ScreenTest_value_ArrayShowText[x][2] = "Đúng"
                            Count_True = Count_True + 1
                        else:
                            self.ScreenTest_value_ArrayShowText[x][2] = "sai"
                            Count_False = Count_False + 1
                else:
                    self.ScreenTest_value_ArrayShowText[x][2] = "Chưa chọn"
                    Count_NotChoose = Count_NotChoose + 1

        self.ScreenTest_value_ArrayInforAnswer[2] = Count_True
        self.ScreenTest_value_ArrayInforAnswer[3] = Count_False
        self.ScreenTest_value_ArrayInforAnswer[4] = Count_NotChoose

        self.uic.screen_test_Display_Answer_Qlabel_Answer2_1.setText(self.ScreenTest_value_ArrayShowText[1][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_2.setText(self.ScreenTest_value_ArrayShowText[2][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_3.setText(self.ScreenTest_value_ArrayShowText[3][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_4.setText(self.ScreenTest_value_ArrayShowText[4][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_5.setText(self.ScreenTest_value_ArrayShowText[5][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_6.setText(self.ScreenTest_value_ArrayShowText[6][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_7.setText(self.ScreenTest_value_ArrayShowText[7][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_8.setText(self.ScreenTest_value_ArrayShowText[8][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_9.setText(self.ScreenTest_value_ArrayShowText[9][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_10.setText(self.ScreenTest_value_ArrayShowText[10][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_11.setText(self.ScreenTest_value_ArrayShowText[11][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_12.setText(self.ScreenTest_value_ArrayShowText[12][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_13.setText(self.ScreenTest_value_ArrayShowText[13][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_14.setText(self.ScreenTest_value_ArrayShowText[14][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_15.setText(self.ScreenTest_value_ArrayShowText[15][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_16.setText(self.ScreenTest_value_ArrayShowText[16][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_17.setText(self.ScreenTest_value_ArrayShowText[17][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_18.setText(self.ScreenTest_value_ArrayShowText[18][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_19.setText(self.ScreenTest_value_ArrayShowText[19][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_20.setText(self.ScreenTest_value_ArrayShowText[20][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_21.setText(self.ScreenTest_value_ArrayShowText[21][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_22.setText(self.ScreenTest_value_ArrayShowText[22][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_23.setText(self.ScreenTest_value_ArrayShowText[23][2])
        self.uic.screen_test_Display_Answer_Qlabel_Answer2_24.setText(self.ScreenTest_value_ArrayShowText[24][2])


    def screen_Test_SaveImageResult(self):
        #myScreenshot = pyautogui.screenshot(region=(0, 0, 300, 400))
        myScreenshot = pyautogui.screenshot()
        path = os.path.abspath('Icon') + "\\" + str(self.ScreenTest_value_NameStudent) + '_' + self.ScreenTest_value_NameITStudent + '.png'
        myScreenshot.save(path)
        self.Show_Screen_Home()

#-----------------------------------------(END)-----------------------------------------------------------------------------#

#-----------------------------------------(Giao Diện Setting)-----------------------------------------------------------------------------#
    def screen_Setting_Show_Display_Practice(self): #Hàm Hiển thị giao diện tao bài thực hành
        self.screen_Setting_Get_Select_CreateExercise()
        self.screen_Setting_Show_NameText_Practice()
        self.uic.stackedWidget_3.setCurrentWidget(self.uic.screen_Setting_practice)

    def screen_Setting_Show_NameText_Practice(self): #hiển thị giá trị PAN của bài thực hành
        self.uic.screen_Setting_practice_label_1.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[1]))
        self.uic.screen_Setting_practice_label_2.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[2]))
        self.uic.screen_Setting_practice_label_3.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[3]))
        self.uic.screen_Setting_practice_label_4.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[4]))
        self.uic.screen_Setting_practice_label_5.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[5]))
        self.uic.screen_Setting_practice_label_6.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[6]))
        self.uic.screen_Setting_practice_label_7.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[7]))
        self.uic.screen_Setting_practice_label_8.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[8]))
        self.uic.screen_Setting_practice_label_9.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[9]))
        self.uic.screen_Setting_practice_label_10.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[10]))
        self.uic.screen_Setting_practice_label_11.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[11]))
        self.uic.screen_Setting_practice_label_12.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[12]))
        self.uic.screen_Setting_practice_label_13.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[13]))
        self.uic.screen_Setting_practice_label_14.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[14]))
        self.uic.screen_Setting_practice_label_15.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[15]))
        self.uic.screen_Setting_practice_label_16.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[16]))
        self.uic.screen_Setting_practice_label_17.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[17]))
        self.uic.screen_Setting_practice_label_18.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[18]))
        self.uic.screen_Setting_practice_label_19.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[19]))
        self.uic.screen_Setting_practice_label_20.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[20]))
        self.uic.screen_Setting_practice_label_21.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[21]))
        self.uic.screen_Setting_practice_label_22.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[22]))
        self.uic.screen_Setting_practice_label_23.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[23]))
        self.uic.screen_Setting_practice_label_24.setText(str(self.ScreenSetting_value_ArrayGetCurrentText[24]))

    def screen_Setting_RamdomExercise(self): #Hàm tạo bài ngẫu nhiên
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

    def screen_Setting_ArrRandomCreateExercise(self): #hàm tạo giá trị ngẫu nhiên
        ArrRandom_setCurrentText = random.randint(6, size=(25))
        ArrRandom_voltage = random.uniform(0.0, 12.0, 25)
        return ArrRandom_setCurrentText, ArrRandom_voltage

    def screen_Setting_Get_Select_CreateExercise(self):# hàm lấy bài đã tạo đưa vào mảng, mảng ScreenSetting_value_ArrayGetCurrentText: là mảng lấy text, ScreenSetting_value_ArrayGetCurrentIndex: mảng lấy vị trí

        if (self.Sys_value_ChooseScreenTest == 2):
            if(self.FlagStartTimeOut == 0):
                self.ScreenTest_value_TimeOut_M = self.uic.screen_Setting_Home_spinBox_TimeOut.value()
                self.ScreenTest_value_TimeOut_S = 0
                self.ScreenTest_value_Time_first = self.uic.screen_Setting_Home_spinBox_TimeOut.value() - 1
        if (self.uic.screen_setting_Home_ComboBox_1.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[1] = (self.uic.screen_setting_Home_lineEdit_1.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[1] = self.uic.screen_setting_Home_ComboBox_1.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[1] = self.uic.screen_setting_Home_ComboBox_1.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_2.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[2] = (self.uic.screen_setting_Home_lineEdit_2.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[2] = self.uic.screen_setting_Home_ComboBox_2.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[2] = self.uic.screen_setting_Home_ComboBox_2.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_3.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[3] = (self.uic.screen_setting_Home_lineEdit_3.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[3] = self.uic.screen_setting_Home_ComboBox_3.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[3] = self.uic.screen_setting_Home_ComboBox_3.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_4.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[4] = (self.uic.screen_setting_Home_lineEdit_4.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[4] = self.uic.screen_setting_Home_ComboBox_4.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[4] = self.uic.screen_setting_Home_ComboBox_4.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_5.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[5] = (self.uic.screen_setting_Home_lineEdit_5.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[5] = self.uic.screen_setting_Home_ComboBox_5.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[5] = self.uic.screen_setting_Home_ComboBox_5.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_6.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[6] = (self.uic.screen_setting_Home_lineEdit_6.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[6] = self.uic.screen_setting_Home_ComboBox_6.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[6] = self.uic.screen_setting_Home_ComboBox_6.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_7.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[7] = (self.uic.screen_setting_Home_lineEdit_7.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[7] = self.uic.screen_setting_Home_ComboBox_7.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[7] = self.uic.screen_setting_Home_ComboBox_7.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_8.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[8] = (self.uic.screen_setting_Home_lineEdit_8.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[8] = self.uic.screen_setting_Home_ComboBox_8.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[8] = self.uic.screen_setting_Home_ComboBox_8.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_9.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[9] = (self.uic.screen_setting_Home_lineEdit_9.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[9] = self.uic.screen_setting_Home_ComboBox_9.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[9] = self.uic.screen_setting_Home_ComboBox_9.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_10.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[10] = (self.uic.screen_setting_Home_lineEdit_10.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[10] = self.uic.screen_setting_Home_ComboBox_10.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[10] = self.uic.screen_setting_Home_ComboBox_10.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_11.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[11] = (self.uic.screen_setting_Home_lineEdit_11.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[11] = self.uic.screen_setting_Home_ComboBox_11.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[11] = self.uic.screen_setting_Home_ComboBox_11.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_12.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[12] = (self.uic.screen_setting_Home_lineEdit_12.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[12] = self.uic.screen_setting_Home_ComboBox_12.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[12] = self.uic.screen_setting_Home_ComboBox_12.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_13.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[13] = (self.uic.screen_setting_Home_lineEdit_13.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[13] = self.uic.screen_setting_Home_ComboBox_13.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[13] = self.uic.screen_setting_Home_ComboBox_13.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_14.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[14] = (self.uic.screen_setting_Home_lineEdit_14.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[14] = self.uic.screen_setting_Home_ComboBox_14.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[14] = self.uic.screen_setting_Home_ComboBox_14.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_15.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[15] = (self.uic.screen_setting_Home_lineEdit_15.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[15] = self.uic.screen_setting_Home_ComboBox_15.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[15] = self.uic.screen_setting_Home_ComboBox_15.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_16.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[16] = (self.uic.screen_setting_Home_lineEdit_16.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[16] = self.uic.screen_setting_Home_ComboBox_16.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[16] = self.uic.screen_setting_Home_ComboBox_16.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_17.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[17] = (self.uic.screen_setting_Home_lineEdit_17.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[17] = self.uic.screen_setting_Home_ComboBox_17.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[17] = self.uic.screen_setting_Home_ComboBox_17.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_18.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[18] = (self.uic.screen_setting_Home_lineEdit_18.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[18] = self.uic.screen_setting_Home_ComboBox_18.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[18] = self.uic.screen_setting_Home_ComboBox_18.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_19.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[19] = (self.uic.screen_setting_Home_lineEdit_19.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[19] = self.uic.screen_setting_Home_ComboBox_19.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[19] = self.uic.screen_setting_Home_ComboBox_19.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_20.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[20] = (self.uic.screen_setting_Home_lineEdit_20.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[20] = self.uic.screen_setting_Home_ComboBox_20.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[20] = self.uic.screen_setting_Home_ComboBox_20.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_21.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[21] = (self.uic.screen_setting_Home_lineEdit_21.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[21] = self.uic.screen_setting_Home_ComboBox_21.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[21] = self.uic.screen_setting_Home_ComboBox_21.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_22.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[22] = (self.uic.screen_setting_Home_lineEdit_22.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[22] = self.uic.screen_setting_Home_ComboBox_22.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[22] = self.uic.screen_setting_Home_ComboBox_22.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_23.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[23] = (self.uic.screen_setting_Home_lineEdit_23.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[23] = self.uic.screen_setting_Home_ComboBox_23.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[23] = self.uic.screen_setting_Home_ComboBox_23.currentIndex()

        if (self.uic.screen_setting_Home_ComboBox_24.currentIndex() >= 5):
            self.ScreenSetting_value_ArrayGetCurrentText[24] = (self.uic.screen_setting_Home_lineEdit_24.text())
        else:
            self.ScreenSetting_value_ArrayGetCurrentText[24] = self.uic.screen_setting_Home_ComboBox_24.currentText()
        self.ScreenSetting_value_ArrayGetCurrentIndex[24] = self.uic.screen_setting_Home_ComboBox_24.currentIndex()

    #--------------(cụm hàm kiểm tra nếu chọn điện áp thì mở ô điền thông tin)
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

    def screen_Setting_Clear_CreateExercise(self, i): # hàm xóa  giao diện tạo bài về bình thường
        items = ['Hở mạch', 'Chập chờn', 'Chạm đất', 'Nối dương', 'Bình thường', 'Điện áp']
        self.uic.screen_Setting_Home_spinBox_TimeOut.setValue(30)
        self.uic.screen_setting_Home_ComboBox_1.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_1.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_1.clear()

        self.uic.screen_setting_Home_ComboBox_2.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_2.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_2.clear()

        self.uic.screen_setting_Home_ComboBox_3.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_3.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_3.clear()

        self.uic.screen_setting_Home_ComboBox_4.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_4.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_4.clear()

        self.uic.screen_setting_Home_ComboBox_5.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_5.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_5.clear()

        self.uic.screen_setting_Home_ComboBox_6.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_6.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_6.clear()

        self.uic.screen_setting_Home_ComboBox_7.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_7.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_7.clear()

        self.uic.screen_setting_Home_ComboBox_8.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_8.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_8.clear()

        self.uic.screen_setting_Home_ComboBox_9.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_9.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_9.clear()

        self.uic.screen_setting_Home_ComboBox_10.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_10.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_10.clear()

        self.uic.screen_setting_Home_ComboBox_11.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_11.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_11.clear()

        self.uic.screen_setting_Home_ComboBox_12.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_12.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_12.clear()

        self.uic.screen_setting_Home_ComboBox_13.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_13.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_13.clear()

        self.uic.screen_setting_Home_ComboBox_14.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_14.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_14.clear()

        self.uic.screen_setting_Home_ComboBox_15.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_15.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_15.clear()

        self.uic.screen_setting_Home_ComboBox_16.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_16.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_16.clear()

        self.uic.screen_setting_Home_ComboBox_17.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_17.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_17.clear()

        self.uic.screen_setting_Home_ComboBox_18.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_18.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_18.clear()

        self.uic.screen_setting_Home_ComboBox_19.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_19.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_19.clear()

        self.uic.screen_setting_Home_ComboBox_20.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_20.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_20.clear()

        self.uic.screen_setting_Home_ComboBox_21.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_21.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_21.clear()

        self.uic.screen_setting_Home_ComboBox_22.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_22.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_22.clear()

        self.uic.screen_setting_Home_ComboBox_23.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_23.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_23.clear()

        self.uic.screen_setting_Home_ComboBox_24.setCurrentText(items[i])
        self.uic.screen_setting_Home_lineEdit_24.setEnabled(0)
        self.uic.screen_setting_Home_lineEdit_24.clear()

    def screen_Setting_Show_Login(self):
        self.uic.screen_Setting_SettingSys_Qlineedit_Password.clear()
        self.uic.stackedWidget_3.setCurrentWidget(self.uic.screen_Setting_Login)

    def screen_Setting_Show_SettingSYS(self):
        if(len(self.uic.screen_Setting_SettingSys_Qlineedit_Password.text()) > 0):
            if(self.settings.value(self.QSettingsSave_StrPassword) == self.uic.screen_Setting_SettingSys_Qlineedit_Password.text()):
                self.uic.screen_Setting_SettingSys_label_Remind.setStyleSheet("background-color: transparent;")
                self.uic.screen_Setting_SettingSys_label_Remind.setText("")
                self.uic.stackedWidget_3.setCurrentWidget(self.uic.screen_Setting_SettingSys)
            else:
                self.uic.screen_Setting_SettingSys_Qlineedit_Password.clear()
                self.uic.screen_Setting_SettingSys_label_Remind.setStyleSheet("background-color: red;")
                self.uic.screen_Setting_SettingSys_label_Remind.setText("Sai mật khẩu")



#-----------------------------------------(END)-----------------------------------------------------------------------------#
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win =  MainWindow()
    main_win.show()
    sys.exit(app.exec())

