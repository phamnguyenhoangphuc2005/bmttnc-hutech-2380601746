class RailFenceCipher:
    def __init__(self):
        pass

    def validate_text(self, text, text_name):
        if text is None or text.strip() == "":
            raise ValueError(f"{text_name} không được rỗng")
        return text

    def validate_key(self, key, text_length, mode):
        if key is None or str(key).strip() == "":
            raise ValueError("Key không được rỗng")

        try:
            key = int(key)
        except ValueError:
            raise ValueError("Số rail phải là số nguyên dương >= 2!")

        if key < 2:
            raise ValueError("Số rail phải là số nguyên dương >= 2!")

        if key >= text_length:
            if mode == "encrypt":
                raise ValueError(f"Key phải < độ dài Text ({text_length})")
            else:
                raise ValueError(f"Key phải < độ dài Cipher Text ({text_length})")

        return key

    def rail_fence_encrypt(self, plain_text, num_rails):
        plain_text = self.validate_text(plain_text, "Text")
        num_rails = self.validate_key(num_rails, len(plain_text), "encrypt")

        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1

        for char in plain_text:
            rails[rail_index].append(char)

            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1

            rail_index += direction
            cipher_text = ''.join(''.join(rail) for rail in rails)
        return cipher_text

    def rail_fence_decrypt(self, cipher_text, num_rails):
        cipher_text = self.validate_text(cipher_text, "Cipher Text")
        num_rails = self.validate_key(num_rails, len(cipher_text), "decrypt")

        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1

            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1

            rail_index += direction
            rails = []
        start = 0

        for length in rail_lengths:
            rails.append(list(cipher_text[start:start + length]))
            start += length
            plain_text = ""
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            plain_text += rails[rail_index].pop(0)

            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1

            rail_index += direction

        return plain_text