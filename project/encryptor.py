from Crypto.Cipher import AES
import base64

def pad(data):
    # Pads the input string with spaces so its length is a multiple of 16 (AES block size)
    return data + (16 - len(data) % 16) * ' '

def encrypt(msg, key):
    # Encrypts the message using AES (ECB mode) and encodes the result in base64
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(pad(msg).encode())).decode()

def decrypt(ciphertext, key):
    # Decrypts the base64-encoded ciphertext using AES (ECB mode) and removes padding
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    return cipher.decrypt(base64.b64decode(ciphertext)).decode().rstrip()
