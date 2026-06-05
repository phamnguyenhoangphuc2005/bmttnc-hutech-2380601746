class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        # Chuẩn hoá khoá: viết hoa, gộp J -> I
        key = key.upper().replace("J", "I")
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # 25 chữ cái, I dùng chung cho J
        # Loại bỏ ký tự trùng lặp trong khoá (giữ thứ tự xuất hiện), chỉ nhận chữ cái hợp lệ
        seen = []
        for ch in key:
            if ch in alphabet and ch not in seen:
                seen.append(ch)
        # Thêm các chữ cái còn lại để đủ đúng 25 ký tự khác nhau
        for ch in alphabet:
            if ch not in seen:
                seen.append(ch)
        playfair_matrix = [seen[i:i+5] for i in range(0, 25, 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col

    def playfair_encrypt(self, plain_text, matrix):
        # Chuyển "J" thành "I" trong văn bản đầu vào
        plain_text = plain_text.upper().replace("J", "I")
        encrypted_text = ""

        for i in range(0, len(plain_text), 2):
            pair = plain_text[i:i+2]
            if len(pair) == 1:  # Xử lý nếu số lượng ký tự lẻ
                pair += "X"
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
        cipher_text = cipher_text.upper().replace("J", "I")
        decrypted_text = ""
        decrypted_text1 = ""

        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]

        # Loại bỏ ký tự 'X' nếu nó là ký tự cuối cùng và ký tự được thêm vào
        banro = ""
        for i in range(0, len(decrypted_text)-2, 2):
            if decrypted_text[i] == decrypted_text[i+2]:
                banro += decrypted_text[i]
            else:
                banro += decrypted_text[i] + "" + decrypted_text[i+1]

        if decrypted_text[-1] == "X":
            banro += decrypted_text[-2]
        else:
            banro += decrypted_text[-2]
            banro += decrypted_text[-1] 

        return banro