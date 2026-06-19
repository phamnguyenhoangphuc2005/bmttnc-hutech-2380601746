from flask import Flask, request, jsonify
import re
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher

app = Flask(__name__)


def ok(data):
    return jsonify(data)


def error(message, status=400):
    return jsonify({"ok": False, "error": message}), status


def only_letters(value):
    return bool(re.fullmatch(r"[A-Za-z]+", value or ""))


def get_json_data():
    return request.get_json(silent=True) or {}


def validate_caesar_key(key):
    try:
        key = int(key)
    except (TypeError, ValueError):
        return None, "Key Caesar phải là số nguyên từ 1 đến 25."
    if key < 1 or key > 25:
        return None, "Key Caesar phải nằm trong khoảng 1 đến 25."
    return key, None


def validate_letters_key(key, name):
    key = (key or "").strip()
    if not key:
        return None, f"Vui lòng nhập key {name}."
    if not only_letters(key):
        return None, f"Key {name} phải là chuỗi chữ cái A-Z."
    return key.upper(), None


def validate_vigenere_key(key, text):
    key, err = validate_letters_key(key, 'Vigenere')
    if err:
        return None, "Key Vigenere chỉ được chứa chữ cái A-Z, không chứa số/khoảng trắng/ký tự đặc biệt và không được để trống."
    if len(key) > len(text):
        return None, f"Key Vigenere không được dài hơn văn bản hiện tại ({len(text)} ký tự)."
    return key, None


def validate_railfence_key(key, text):
    try:
        key = int(key)
    except (TypeError, ValueError):
        return None, "Key Rail Fence phải là số nguyên."
    if key < 2:
        return None, "Key Rail Fence phải >= 2."
    if key >= len(text):
        return None, f"Key Rail Fence phải nhỏ hơn số ký tự văn bản hiện tại ({len(text)})."
    return key, None


# =========================
# Caesar Cipher
# =========================
caesar_cipher = CaesarCipher()

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = get_json_data()
    plain_text = data.get('plain_text', '')
    key, err = validate_caesar_key(data.get('key'))
    if err:
        return error(err)
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return ok({'ok': True, 'encrypted_message': encrypted_text})


@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = get_json_data()
    cipher_text = data.get('cipher_text', '')
    key, err = validate_caesar_key(data.get('key'))
    if err:
        return error(err)
    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return ok({'ok': True, 'decrypted_message': decrypted_text})


# =========================
# Vigenere Cipher
# =========================
vigenere_cipher = VigenereCipher()

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = get_json_data()
    plain_text = data.get('plain_text', '')
    key, err = validate_vigenere_key(data.get('key'), plain_text)
    if err:
        return error(err)
    encrypted_text = vigenere_cipher.vig_encrypt(plain_text, key)
    return ok({'ok': True, 'encrypted_text': encrypted_text})


@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = get_json_data()
    cipher_text = data.get('cipher_text', '')
    key, err = validate_vigenere_key(data.get('key'), cipher_text)
    if err:
        return error(err)
    decrypted_text = vigenere_cipher.vig_decrypt(cipher_text, key)
    return ok({'ok': True, 'decrypted_text': decrypted_text})


# =========================
# Rail Fence Cipher
# =========================
railfence_cipher = RailFenceCipher()

@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    data = get_json_data()
    plain_text = data.get('plain_text', '')
    key, err = validate_railfence_key(data.get('key'), plain_text)
    if err:
        return error(err)
    encrypted_text = railfence_cipher.rail_fence_encrypt(plain_text, key)
    return ok({'ok': True, 'encrypted_text': encrypted_text})


@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    data = get_json_data()
    cipher_text = data.get('cipher_text', '')
    key, err = validate_railfence_key(data.get('key'), cipher_text)
    if err:
        return error(err)
    decrypted_text = railfence_cipher.rail_fence_decrypt(cipher_text, key)
    return ok({'ok': True, 'decrypted_text': decrypted_text})


# =========================
# PlayFair Cipher
# =========================
playfair_cipher = PlayFairCipher()

@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():
    data = get_json_data()
    key, err = validate_letters_key(data.get('key'), 'Playfair')
    if err:
        return error(err)
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    return ok({'ok': True, "playfair_matrix": playfair_matrix})


@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = get_json_data()
    plain_text = data.get('plain_text', '')
    key, err = validate_letters_key(data.get('key'), 'Playfair')
    if err:
        return error(err)
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(plain_text, playfair_matrix)
    return ok({'ok': True, 'encrypted_text': encrypted_text})


@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = get_json_data()
    cipher_text = data.get('cipher_text', '')
    key, err = validate_letters_key(data.get('key'), 'Playfair')
    if err:
        return error(err)
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, playfair_matrix)
    return ok({'ok': True, 'decrypted_text': decrypted_text})


# =========================
# Run Flask
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
