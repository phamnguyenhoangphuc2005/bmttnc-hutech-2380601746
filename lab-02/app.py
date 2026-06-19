from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

FULL_NAME = "PHẠM NGUYỄN HOÀNG PHÚC"
MSSV = "2380601746"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# =========================
# Helpers
# =========================
def success_result(result):
    return jsonify({"ok": True, "result": result})


def error_result(message, status=400):
    return jsonify({"ok": False, "error": message}), status


def only_letters(value):
    return bool(re.fullmatch(r"[A-Za-z]+", value or ""))


def normalize_letters(value):
    return re.sub(r"[^A-Za-z]", "", value or "").upper()


def is_ascii_upper(ch):
    return "A" <= ch <= "Z"


def is_ascii_lower(ch):
    return "a" <= ch <= "z"


def shift_ascii_letter(ch, shift):
    if is_ascii_upper(ch):
        return chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))
    if is_ascii_lower(ch):
        return chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
    return ch


# =========================
# Caesar Cipher
# Key: số nguyên 1 - 25
# Text: chỉ chữ cái A-Z
# =========================
def caesar_encrypt(text, key):
    # Không ràng buộc plaintext: chỉ mã hóa chữ cái A-Z/a-z, ký tự khác giữ nguyên.
    return "".join(shift_ascii_letter(ch, key) for ch in text)


def caesar_decrypt(text, key):
    # Không ràng buộc ciphertext: chỉ giải mã chữ cái A-Z/a-z, ký tự khác giữ nguyên.
    return "".join(shift_ascii_letter(ch, -key) for ch in text)


def validate_caesar(text, key):
    # Chỉ ràng buộc KEY, không ràng buộc plaintext/ciphertext.
    try:
        key = int(key)
    except (TypeError, ValueError):
        return None, None, "Key Caesar phải là số nguyên từ 1 đến 25."
    if key < 1 or key > 25:
        return None, None, "Key Caesar phải nằm trong khoảng 1 đến 25."
    return text, key, None


# =========================
# Vigenere Cipher
# Key: chuỗi chữ cái A-Z và không dài hơn văn bản
# Text: chỉ chữ cái A-Z
# =========================
def vigenere_encrypt(text, key):
    # Không ràng buộc plaintext: chỉ mã hóa chữ cái A-Z/a-z, ký tự khác giữ nguyên.
    key = key.upper()
    output = []
    key_index = 0
    for ch in text:
        if is_ascii_upper(ch) or is_ascii_lower(ch):
            shift = ALPHABET.index(key[key_index % len(key)])
            output.append(shift_ascii_letter(ch, shift))
            key_index += 1
        else:
            output.append(ch)
    return "".join(output)


def vigenere_decrypt(text, key):
    # Không ràng buộc ciphertext: chỉ giải mã chữ cái A-Z/a-z, ký tự khác giữ nguyên.
    key = key.upper()
    output = []
    key_index = 0
    for ch in text:
        if is_ascii_upper(ch) or is_ascii_lower(ch):
            shift = ALPHABET.index(key[key_index % len(key)])
            output.append(shift_ascii_letter(ch, -shift))
            key_index += 1
        else:
            output.append(ch)
    return "".join(output)


def validate_vigenere(text, key):
    # Chỉ ràng buộc KEY, không ràng buộc plaintext/ciphertext.
    # Riêng Vigenere: key phải là chữ cái A-Z và không được dài hơn văn bản nhập vào.
    if not key:
        return None, None, "Vui lòng nhập key."
    if not only_letters(key):
        return None, None, "Key Vigenere chỉ được chứa chữ cái A-Z, không chứa số/khoảng trắng/ký tự đặc biệt."
    if len(key) > len(text):
        return None, None, f"Key Vigenere không được dài hơn văn bản hiện tại ({len(text)} ký tự)."
    return text, key.upper(), None


# =========================
# Rail Fence Cipher
# Key: số rail nguyên >= 2 và < độ dài văn bản
# Text: không rỗng
# =========================
def railfence_encrypt(text, rails):
    fence = [[] for _ in range(rails)]
    row = 0
    direction = 1
    for ch in text:
        fence[row].append(ch)
        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1
        row += direction
    return "".join("".join(line) for line in fence)


def railfence_decrypt(cipher_text, rails):
    pattern = []
    row = 0
    direction = 1
    for _ in cipher_text:
        pattern.append(row)
        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1
        row += direction

    counts = [pattern.count(i) for i in range(rails)]
    fence = []
    start = 0
    for count in counts:
        fence.append(list(cipher_text[start:start + count]))
        start += count

    output = []
    for row in pattern:
        output.append(fence[row].pop(0))
    return "".join(output)


def validate_railfence(text, key):
    # Chỉ ràng buộc KEY. Text được nhập tự do, nhưng key phải phù hợp độ dài văn bản để thuật toán chạy đúng.
    try:
        key = int(key)
    except (TypeError, ValueError):
        return None, None, "Key Rail Fence phải là số nguyên."
    if key < 2:
        return None, None, "Key Rail Fence phải >= 2."
    if key >= len(text):
        return None, None, f"Key Rail Fence phải nhỏ hơn số ký tự của văn bản hiện tại ({len(text)})."
    return text, key, None


# =========================
# Playfair Cipher
# Key: chữ cái A-Z, J được gộp thành I
# Text: chỉ chữ cái A-Z
# =========================
def playfair_matrix(key):
    key = normalize_letters(key).replace("J", "I")
    base = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    seen = []
    for ch in key + base:
        if ch in base and ch not in seen:
            seen.append(ch)
    return [seen[i:i + 5] for i in range(0, 25, 5)]


def playfair_position(matrix, letter):
    letter = "I" if letter == "J" else letter
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == letter:
                return r, c
    raise ValueError(f"Không tìm thấy ký tự {letter} trong ma trận Playfair")


def playfair_prepare_plain(text):
    text = normalize_letters(text).replace("J", "I")
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else "X"
        if a == b:
            pairs.append(a + "X")
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    if pairs and len(pairs[-1]) == 1:
        pairs[-1] += "X"
    return pairs


def playfair_encrypt(text, key):
    matrix = playfair_matrix(key)
    output = []
    for pair in playfair_prepare_plain(text):
        a, b = pair[0], pair[1]
        r1, c1 = playfair_position(matrix, a)
        r2, c2 = playfair_position(matrix, b)
        if r1 == r2:
            output.append(matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5])
        elif c1 == c2:
            output.append(matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2])
        else:
            output.append(matrix[r1][c2] + matrix[r2][c1])
    return "".join(output)


def playfair_decrypt(text, key):
    matrix = playfair_matrix(key)
    text = normalize_letters(text).replace("J", "I")
    if len(text) % 2 != 0:
        text += "X"
    output = []
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        r1, c1 = playfair_position(matrix, a)
        r2, c2 = playfair_position(matrix, b)
        if r1 == r2:
            output.append(matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5])
        elif c1 == c2:
            output.append(matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2])
        else:
            output.append(matrix[r1][c2] + matrix[r2][c1])
    result = "".join(output)
    if result.endswith("X"):
        result = result[:-1]
    return result


def validate_playfair(text, key, mode):
    # Chỉ ràng buộc KEY, không ràng buộc plaintext/ciphertext.
    # Text nhập tự do; thuật toán tự lấy chữ cái A-Z, bỏ ký tự khác và gộp J thành I.
    if not key:
        return None, None, "Vui lòng nhập key Playfair."
    if not only_letters(key):
        return None, None, "Key Playfair phải là chuỗi chữ cái A-Z."
    clean_text = normalize_letters(text).replace("J", "I")
    if mode == "decrypt" and len(clean_text) % 2 != 0:
        clean_text += "X"
    return clean_text, key.upper(), None


# =========================
# Web routes
# =========================
@app.route("/")
def home():
    return render_template("index.html", full_name=FULL_NAME, mssv=MSSV)


@app.route("/caesar")
def caesar_page():
    return render_template("caesar.html")


@app.route("/vigenere")
def vigenere_page():
    return render_template("vigenere.html")


@app.route("/railfence")
def railfence_page():
    return render_template("railfence.html")


@app.route("/playfair")
def playfair_page():
    return render_template("playfair.html")


@app.route("/crypto/<algorithm>/<mode>", methods=["POST"])
def crypto_process(algorithm, mode):
    if mode not in ("encrypt", "decrypt"):
        return error_result("Chế độ không hợp lệ. Chỉ dùng encrypt hoặc decrypt.")

    data = request.get_json(silent=True) or request.form
    text = data.get("text") or ""
    key = (data.get("key") or "").strip()

    if algorithm == "caesar":
        text, key, err = validate_caesar(text, key)
        if err:
            return error_result(err)
        result = caesar_encrypt(text, key) if mode == "encrypt" else caesar_decrypt(text, key)
        return success_result(result)

    if algorithm == "vigenere":
        text, key, err = validate_vigenere(text, key)
        if err:
            return error_result(err)
        result = vigenere_encrypt(text, key) if mode == "encrypt" else vigenere_decrypt(text, key)
        return success_result(result)

    if algorithm == "railfence":
        text, key, err = validate_railfence(text, key)
        if err:
            return error_result(err)
        result = railfence_encrypt(text, key) if mode == "encrypt" else railfence_decrypt(text, key)
        return success_result(result)

    if algorithm == "playfair":
        text, key, err = validate_playfair(text, key, mode)
        if err:
            return error_result(err)
        result = playfair_encrypt(text, key) if mode == "encrypt" else playfair_decrypt(text, key)
        return jsonify({
            "ok": True,
            "result": result,
            "matrix": playfair_matrix(key)
        })

    return error_result("Thuật toán không tồn tại.", 404)


# =========================
# Backward-compatible old form routes
# =========================
def html_response(label, text, key, result):
    return f"text: {text}<br/>key: {key}<br/>{label}: {result}"


@app.route("/encrypt", methods=["POST"])
def old_caesar_encrypt():
    text = request.form.get("inputPlainText", "")
    key = request.form.get("inputKeyPlain", "")
    text2, key2, err = validate_caesar(text, key)
    if err:
        return err, 400
    return html_response("encrypted text", text2, key2, caesar_encrypt(text2, key2))


@app.route("/decrypt", methods=["POST"])
def old_caesar_decrypt():
    text = request.form.get("inputCipherText", "")
    key = request.form.get("inputKeyCipher", "")
    text2, key2, err = validate_caesar(text, key)
    if err:
        return err, 400
    return html_response("decrypted text", text2, key2, caesar_decrypt(text2, key2))


@app.route("/vigenere/encrypt", methods=["POST"])
def old_vigenere_encrypt():
    text = request.form.get("inputPlainText", "")
    key = request.form.get("inputKeyPlain", "")
    text2, key2, err = validate_vigenere(text, key)
    if err:
        return err, 400
    return html_response("encrypted text", text2, key2, vigenere_encrypt(text2, key2))


@app.route("/vigenere/decrypt", methods=["POST"])
def old_vigenere_decrypt():
    text = request.form.get("inputCipherText", "")
    key = request.form.get("inputKeyCipher", "")
    text2, key2, err = validate_vigenere(text, key)
    if err:
        return err, 400
    return html_response("decrypted text", text2, key2, vigenere_decrypt(text2, key2))


@app.route("/railfence/encrypt", methods=["POST"])
def old_railfence_encrypt():
    text = request.form.get("inputPlainText", "")
    key = request.form.get("inputKeyPlain", "")
    text2, key2, err = validate_railfence(text, key)
    if err:
        return err, 400
    return html_response("encrypted text", text2, key2, railfence_encrypt(text2, key2))


@app.route("/railfence/decrypt", methods=["POST"])
def old_railfence_decrypt():
    text = request.form.get("inputCipherText", "")
    key = request.form.get("inputKeyCipher", "")
    text2, key2, err = validate_railfence(text, key)
    if err:
        return err, 400
    return html_response("decrypted text", text2, key2, railfence_decrypt(text2, key2))


@app.route("/playfair/encrypt", methods=["POST"])
def old_playfair_encrypt():
    text = request.form.get("inputPlainText", "")
    key = request.form.get("inputKeyPlain", "")
    text2, key2, err = validate_playfair(text, key, "encrypt")
    if err:
        return err, 400
    return html_response("encrypted text", text2, key2, playfair_encrypt(text2, key2))


@app.route("/playfair/decrypt", methods=["POST"])
def old_playfair_decrypt():
    text = request.form.get("inputCipherText", "")
    key = request.form.get("inputKeyCipher", "")
    text2, key2, err = validate_playfair(text, key, "decrypt")
    if err:
        return err, 400
    return html_response("decrypted text", text2, key2, playfair_decrypt(text2, key2))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
