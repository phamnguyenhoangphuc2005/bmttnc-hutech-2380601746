from cipher.caesar import ALPHABET


class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    def _shift_char(self, char: str, key: int) -> str:
        if 'A' <= char <= 'Z':
            return chr((ord(char) - ord('A') + key) % 26 + ord('A'))
        if 'a' <= char <= 'z':
            return chr((ord(char) - ord('a') + key) % 26 + ord('a'))
        return char

    def encrypt_text(self, text: str, key: int) -> str:
        # Không ràng buộc plaintext: chỉ mã hóa chữ cái A-Z/a-z, ký tự khác giữ nguyên.
        return ''.join(self._shift_char(char, key) for char in text)

    def decrypt_text(self, text: str, key: int) -> str:
        # Không ràng buộc ciphertext: chỉ giải mã chữ cái A-Z/a-z, ký tự khác giữ nguyên.
        return ''.join(self._shift_char(char, -key) for char in text)
