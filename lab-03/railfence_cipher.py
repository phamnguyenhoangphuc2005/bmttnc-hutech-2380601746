import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_MainWindow


class RailFenceLogic:

    @staticmethod
    def encrypt(text, key):

        if key < 2 or key > len(text):
            raise ValueError(
                f"Key phải thỏa mãn 2 ≤ key ≤ {len(text)}"
            )

        rail = [['\n' for _ in range(len(text))]
                for _ in range(key)]

        dir_down = False
        row = 0
        col = 0

        for char in text:

            if row == 0 or row == key - 1:
                dir_down = not dir_down

            rail[row][col] = char
            col += 1

            if dir_down:
                row += 1
            else:
                row -= 1

        result = []

        for i in range(key):
            for j in range(len(text)):
                if rail[i][j] != '\n':
                    result.append(rail[i][j])

        return "".join(result)

    @staticmethod
    def decrypt(cipher, key):

        if key < 2 or key > len(cipher):
            raise ValueError(
                f"Key phải thỏa mãn 2 ≤ key ≤ {len(cipher)}"
            )

        rail = [['\n' for _ in range(len(cipher))]
                for _ in range(key)]

        dir_down = None
        row = 0
        col = 0

        for i in range(len(cipher)):

            if row == 0:
                dir_down = True

            if row == key - 1:
                dir_down = False

            rail[row][col] = '*'
            col += 1

            if dir_down:
                row += 1
            else:
                row -= 1

        index = 0

        for i in range(key):
            for j in range(len(cipher)):
                if rail[i][j] == '*' and index < len(cipher):
                    rail[i][j] = cipher[index]
                    index += 1

        result = []

        row = 0
        col = 0

        for i in range(len(cipher)):

            if row == 0:
                dir_down = True

            if row == key - 1:
                dir_down = False

            result.append(rail[row][col])
            col += 1

            if dir_down:
                row += 1
            else:
                row -= 1

        return "".join(result)


class RailFenceApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.encrypt)
        self.ui.pushButton_2.clicked.connect(self.decrypt)

    def encrypt(self):

        text = self.ui.plainTextEdit.toPlainText().strip()
        key_text = self.ui.plainTextEdit_2.toPlainText().strip()

        if not text or not key_text:
            QMessageBox.warning(
                self,
                "Warning",
                "Vui lòng nhập Text và Key"
            )
            return

        try:
            key = int(key_text)
        except ValueError:
            QMessageBox.warning(
                self,
                "Warning",
                "Key phải là số nguyên"
            )
            return

        if key < 2 or key > len(text):
            QMessageBox.warning(
                self,
                "Warning",
                f"Key phải thỏa mãn 2 ≤ key ≤ {len(text)}"
            )
            return

        cipher = RailFenceLogic.encrypt(text, key)

        self.ui.plainTextEdit_3.setPlainText(cipher)

        QMessageBox.information(
            self,
            "Success",
            "Encrypted Successfully"
        )

    def decrypt(self):

        cipher = self.ui.plainTextEdit_3.toPlainText().strip()
        key_text = self.ui.plainTextEdit_2.toPlainText().strip()

        if not cipher or not key_text:
            QMessageBox.warning(
                self,
                "Warning",
                "Vui lòng nhập Cipher Text và Key"
            )
            return

        try:
            key = int(key_text)
        except ValueError:
            QMessageBox.warning(
                self,
                "Warning",
                "Key phải là số nguyên"
            )
            return

        if key < 2 or key > len(cipher):
            QMessageBox.warning(
                self,
                "Warning",
                f"Key phải thỏa mãn 2 ≤ key ≤ {len(cipher)}"
            )
            return

        plain = RailFenceLogic.decrypt(cipher, key)

        self.ui.plainTextEdit.setPlainText(plain)

        QMessageBox.information(
            self,
            "Success",
            "Decrypted Successfully"
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = RailFenceApp()
    window.show()

    sys.exit(app.exec_())