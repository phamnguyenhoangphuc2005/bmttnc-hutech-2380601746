import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.playfair import Ui_MainWindow


class PlayfairLogic:

    @staticmethod
    def prepare_text(text):
        text = text.upper().replace("J", "I")
        text = "".join(text.split())

        result = ""
        i = 0

        while i < len(text):
            a = text[i]

            if i + 1 < len(text):
                b = text[i + 1]

                if a == b:
                    result += a + "X"
                    i += 1
                else:
                    result += a + b
                    i += 2
            else:
                result += a + "X"
                i += 1

        if len(result) % 2 != 0:
            result += "X"

        return result

    @staticmethod
    def get_matrix(key):
        key = key.upper().replace("J", "I")

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

        combined = ""

        for ch in key:
            if ch.isalpha() and ch not in combined:
                combined += ch

        for ch in alphabet:
            if ch not in combined:
                combined += ch

        matrix = []

        for i in range(0, 25, 5):
            matrix.append(list(combined[i:i + 5]))

        return matrix

    @staticmethod
    def find_position(matrix, char):
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == char:
                    return i, j

    @staticmethod
    def encrypt(text, key):

        text = PlayfairLogic.prepare_text(text)
        matrix = PlayfairLogic.get_matrix(key)

        result = ""

        for i in range(0, len(text), 2):

            a = text[i]
            b = text[i + 1]

            r1, c1 = PlayfairLogic.find_position(matrix, a)
            r2, c2 = PlayfairLogic.find_position(matrix, b)

            if r1 == r2:

                result += matrix[r1][(c1 + 1) % 5]
                result += matrix[r2][(c2 + 1) % 5]

            elif c1 == c2:

                result += matrix[(r1 + 1) % 5][c1]
                result += matrix[(r2 + 1) % 5][c2]

            else:

                result += matrix[r1][c2]
                result += matrix[r2][c1]

        return result

    @staticmethod
    def decrypt(cipher_text, key):

        cipher_text = cipher_text.upper().replace(" ", "")
        matrix = PlayfairLogic.get_matrix(key)

        result = ""

        for i in range(0, len(cipher_text), 2):

            a = cipher_text[i]
            b = cipher_text[i + 1]

            r1, c1 = PlayfairLogic.find_position(matrix, a)
            r2, c2 = PlayfairLogic.find_position(matrix, b)

            if r1 == r2:

                result += matrix[r1][(c1 - 1) % 5]
                result += matrix[r2][(c2 - 1) % 5]

            elif c1 == c2:

                result += matrix[(r1 - 1) % 5][c1]
                result += matrix[(r2 - 1) % 5][c2]

            else:

                result += matrix[r1][c2]
                result += matrix[r2][c1]

        return result


class PlayfairApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.encrypt)
        self.ui.pushButton_2.clicked.connect(self.decrypt)

    def encrypt(self):

        plain_text = self.ui.plainTextEdit.toPlainText().strip()
        key = self.ui.plainTextEdit_2.toPlainText().strip()

        if not plain_text or not key:
            QMessageBox.warning(
                self,
                "Warning",
                "Vui lòng nhập Plain Text và Key"
            )
            return

        if not re.fullmatch(r"[A-Za-z]+", key):
            QMessageBox.warning(
                self,
                "Warning",
                "Key chỉ được chứa chữ cái A-Z hoặc a-z"
            )
            return

        if not re.fullmatch(r"[A-Za-z ]+", plain_text):
            QMessageBox.warning(
                self,
                "Warning",
                "Plain Text chỉ được chứa chữ cái và khoảng trắng"
            )
            return

        cipher = PlayfairLogic.encrypt(plain_text, key)

        self.ui.plainTextEdit_3.setPlainText(cipher)

        QMessageBox.information(
            self,
            "Success",
            "Encrypted Successfully"
        )

    def decrypt(self):

        cipher_text = self.ui.plainTextEdit_3.toPlainText().strip()
        key = self.ui.plainTextEdit_2.toPlainText().strip()

        if not cipher_text or not key:
            QMessageBox.warning(
                self,
                "Warning",
                "Vui lòng nhập Cipher Text và Key"
            )
            return

        if not re.fullmatch(r"[A-Za-z]+", key):
            QMessageBox.warning(
                self,
                "Warning",
                "Key chỉ được chứa chữ cái A-Z hoặc a-z"
            )
            return

        if not re.fullmatch(r"[A-Za-z]+", cipher_text):
            QMessageBox.warning(
                self,
                "Warning",
                "Cipher Text chỉ được chứa chữ cái"
            )
            return

        plain = PlayfairLogic.decrypt(cipher_text, key)

        self.ui.plainTextEdit.setPlainText(plain)

        QMessageBox.information(
            self,
            "Success",
            "Decrypted Successfully"
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = PlayfairApp()
    window.show()

    sys.exit(app.exec_())