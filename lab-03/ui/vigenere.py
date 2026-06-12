# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Nút Encrypt
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(190, 520, 75, 23))
        self.pushButton.setObjectName("pushButton")
        
        # Tiêu đề
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 30, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        # Label Plain Text
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 90, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        
        # Plain Text Edit (Input ban đầu)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(160, 90, 501, 121))
        self.plainTextEdit.setObjectName("plainTextEdit")
        
        # Key Edit
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(160, 240, 501, 51))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        
        # Cipher Text Edit (Kết quả)
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(160, 320, 501, 121))
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        
        # Nút Decrypt
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 520, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        
        # Label Key
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 240, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        
        # Label Cipher Text
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 310, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")


        # Thông tin cá nhân
        self.studentInfo = QtWidgets.QLabel(self.centralwidget)
        self.studentInfo.setGeometry(QtCore.QRect(120, 455, 560, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.studentInfo.setFont(font)
        self.studentInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.studentInfo.setText("Tên: PHẠM NGUYỄN HOÀNG PHÚC    |    MSSV: 2380601746")
        self.studentInfo.setObjectName("studentInfo")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.studentInfo.setText(_translate("MainWindow", "Tên: PHẠM NGUYỄN HOÀNG PHÚC    |    MSSV: 2380601746"))
        self.pushButton.setText(_translate("MainWindow", "Encrypt"))
        self.label.setText(_translate("MainWindow", "vigenere cipher"))
        self.label_2.setText(_translate("MainWindow", "plain text:"))
        self.pushButton_2.setText(_translate("MainWindow", "Decrypt"))
        self.label_3.setText(_translate("MainWindow", "key:"))
        self.label_4.setText(_translate("MainWindow", "Cipher text:"))