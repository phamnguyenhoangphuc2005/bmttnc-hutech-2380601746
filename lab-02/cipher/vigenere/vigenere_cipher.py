class VigenereCipher:
    def __init__(self):
        pass

    def _is_ascii_letter(self, char):
        return ('A' <= char <= 'Z') or ('a' <= char <= 'z')

    def _shift_char(self, char, shift):
        if 'A' <= char <= 'Z':
            return chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        if 'a' <= char <= 'z':
            return chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        return char

    def vig_encrypt(self, plain_text, key):
        # Không ràng buộc plaintext: chỉ mã hóa chữ cái A-Z/a-z, ký tự khác giữ nguyên.
        encrypted_text = ""
        key_index = 0
        key = key.upper()
        for char in plain_text:
            if self._is_ascii_letter(char):
                key_shift = ord(key[key_index % len(key)]) - ord('A')
                encrypted_text += self._shift_char(char, key_shift)
                key_index += 1
            else:
                encrypted_text += char
        return encrypted_text

    def vig_decrypt(self, encrypted_text, key):
        # Không ràng buộc ciphertext: chỉ giải mã chữ cái A-Z/a-z, ký tự khác giữ nguyên.
        decrypted_text = ""
        key_index = 0
        key = key.upper()
        for char in encrypted_text:
            if self._is_ascii_letter(char):
                key_shift = ord(key[key_index % len(key)]) - ord('A')
                decrypted_text += self._shift_char(char, -key_shift)
                key_index += 1
            else:
                decrypted_text += char
        return decrypted_text
