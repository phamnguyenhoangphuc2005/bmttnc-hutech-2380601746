import re


class PlayFairCipher:
    def __init__(self):
        pass

    def _normalize_text(self, text):
        # Không ràng buộc plaintext/ciphertext: tự lấy A-Z, bỏ ký tự khác và gộp J thành I.
        return re.sub(r"[^A-Za-z]", "", text or "").upper().replace("J", "I")

    def create_playfair_matrix(self, key):
        key = self._normalize_text(key)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        seen = []
        for ch in key:
            if ch in alphabet and ch not in seen:
                seen.append(ch)
        for ch in alphabet:
            if ch not in seen:
                seen.append(ch)
        return [seen[i:i + 5] for i in range(0, 25, 5)]

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        raise ValueError(f"Không tìm thấy ký tự {letter} trong ma trận Playfair")

    def _prepare_plain_text(self, plain_text):
        plain_text = self._normalize_text(plain_text)
        pairs = []
        i = 0
        while i < len(plain_text):
            a = plain_text[i]
            b = plain_text[i + 1] if i + 1 < len(plain_text) else "X"
            if a == b:
                pairs.append(a + "X")
                i += 1
            else:
                pairs.append(a + b)
                i += 2
        return pairs

    def playfair_encrypt(self, plain_text, matrix):
        encrypted_text = ""
        for pair in self._prepare_plain_text(plain_text):
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = self._normalize_text(cipher_text)
        if len(cipher_text) % 2 != 0:
            cipher_text += "X"
        decrypted_text = ""
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i + 2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]
        if decrypted_text.endswith("X"):
            decrypted_text = decrypted_text[:-1]
        return decrypted_text
