import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_MainWindow


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.call_api_encrypt)
        self.ui.pushButton_2.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/encrypt"

        payload = {
            "plain_text": self.ui.plainTextEdit.toPlainText(),
            "key": self.ui.plainTextEdit_2.toPlainText()
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            self.ui.plainTextEdit_3.setPlainText(data["encrypted_message"])

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Encrypted Successfully")
            msg.setWindowTitle("Success")
            msg.exec_()
        else:
            print("Error while calling API")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/decrypt"

        payload = {
            "cipher_text": self.ui.plainTextEdit_3.toPlainText(),
            "key": self.ui.plainTextEdit_2.toPlainText()
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            self.ui.plainTextEdit.setPlainText(data["decrypted_message"])

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Decrypted Successfully")
            msg.setWindowTitle("Success")
            msg.exec_()
        else:
            print("Error while calling API")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
