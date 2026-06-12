from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        # Tiêu đề
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 20, 300, 51))
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setText("Playfair Cipher")

        # Plain Text Label
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 80, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setText("Plain Text:")

        # Plain Text Box
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(170, 80, 501, 121))

        # Key Label
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 230, 50, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setText("Key:")

        # Key Box
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(170, 230, 501, 51))

        # Cipher Text Label
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 300, 120, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setText("Cipher Text:")

        # Cipher Text Box
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(170, 310, 501, 121))

        # Encrypt Button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 500, 100, 40))
        self.pushButton.setText("Encrypt")

        # Decrypt Button
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(500, 500, 100, 40))
        self.pushButton_2.setText("Decrypt")


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