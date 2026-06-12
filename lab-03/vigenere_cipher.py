import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# Đảm bảo đường dẫn import này đúng với cấu trúc thư mục của bạn
from ui.vigenere import Ui_MainWindow 

class VigenereLogic:
    @staticmethod
    def _validate_key(key):
        key = key.strip()
        if not key:
            raise ValueError("Key không được rỗng")
        if not key.isalpha():
            raise ValueError("Key chỉ được chứa chữ cái A-Z")
        return key.upper()

    @staticmethod
    def encrypt(text, key):
        key = VigenereLogic._validate_key(key)
        result = []
        j = 0
        for c in text:
            if c.isalpha():
                # Lấy độ dời từ ký tự tương ứng của key
                k = ord(key[j % len(key)]) - ord('A')
                base = ord('A') if c.isupper() else ord('a')
                result.append(chr((ord(c) - base + k) % 26 + base))
                j += 1
            else:
                result.append(c)
        return "".join(result)

    @staticmethod
    def decrypt(text, key):
        key = VigenereLogic._validate_key(key)
        result = []
        j = 0
        for c in text:
            if c.isalpha():
                k = ord(key[j % len(key)]) - ord('A')
                base = ord('A') if c.isupper() else ord('a')
                # +26 để đảm bảo không bị số âm trước khi chia lấy dư
                result.append(chr((ord(c) - base - k + 26) % 26 + base))
                j += 1
            else:
                result.append(c)
        return "".join(result)

class VigenereApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối sự kiện (Tên pushButton phải khớp với file ui/vigenere.py)
        self.ui.pushButton.clicked.connect(self.handle_encrypt)
        self.ui.pushButton_2.clicked.connect(self.handle_decrypt)

    def handle_encrypt(self):
        text = self.ui.plainTextEdit.toPlainText()
        key = self.ui.plainTextEdit_2.toPlainText()
        
        if not text:
            QMessageBox.warning(self, "Warning", "Vui lòng nhập Plain Text")
            return

        try:
            cipher = VigenereLogic.encrypt(text, key)
            self.ui.plainTextEdit_3.setPlainText(cipher)
            QMessageBox.information(self, "Success", "Mã hóa thành công!")
        except ValueError as e:
            QMessageBox.warning(self, "Warning", str(e))

    def handle_decrypt(self):
        cipher = self.ui.plainTextEdit_3.toPlainText()
        key = self.ui.plainTextEdit_2.toPlainText()

        if not cipher:
            QMessageBox.warning(self, "Warning", "Vui lòng nhập Cipher Text")
            return

        try:
            plain = VigenereLogic.decrypt(cipher, key)
            self.ui.plainTextEdit.setPlainText(plain)
            QMessageBox.information(self, "Success", "Giải mã thành công!")
        except ValueError as e:
            QMessageBox.warning(self, "Warning", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VigenereApp()
    window.show()
    sys.exit(app.exec_())