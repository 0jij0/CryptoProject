from Crypto.Cipher import AES
import base64

def pad(data):
    return data + (16 - len(data) % 16) * ' '

def encrypt(msg, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(pad(msg).encode())).decode()

def decrypt(ciphertext, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    return cipher.decrypt(base64.b64decode(ciphertext)).decode().rstrip()
